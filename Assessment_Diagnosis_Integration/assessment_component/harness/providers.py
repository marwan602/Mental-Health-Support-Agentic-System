"""Model clients.

ChatClient calls compatible /chat/completions endpoints using the standard library.
LLMCaller wraps a client for one interview: it builds messages, calls the model,
parses and validates JSON, asks once for a corrected object when the output is
invalid, caches every response for exact replay, and logs everything.
"""
import json
import os
import random
import re
import threading
import time
import urllib.error
import urllib.request
from collections import deque
from dataclasses import dataclass, field

from .util import parse_json_loose, sha256_obj, Stopwatch


class ProviderError(Exception):
    pass


class QuotaExhausted(ProviderError):
    """Daily or long-window quota is used up; the runner pauses this model and resumes later."""

    def __init__(self, msg, model_key=None):
        super().__init__(msg)
        self.model_key = model_key


@dataclass
class Response:
    text: str
    usage: dict = field(default_factory=dict)
    model_returned: str = None
    response_id: str = None
    finish_reason: str = None
    latency_ms: int = 0
    http_attempts: int = 1
    note: str = None
    reasoning: str = None   # the model's visible thinking, when the provider returns it


class RateLimiter:
    """Thread-safe requests-per-minute and (estimated) tokens-per-minute limiter."""

    def __init__(self, rpm=None, tpm=None):
        self.rpm = rpm
        self.tpm = tpm
        self.lock = threading.Lock()
        self.calls = deque()
        self.tokens = deque()

    def wait(self, est_tokens):
        while True:
            with self.lock:
                now = time.monotonic()
                while self.calls and now - self.calls[0] > 60:
                    self.calls.popleft()
                while self.tokens and now - self.tokens[0][0] > 60:
                    self.tokens.popleft()
                ok_r = not self.rpm or len(self.calls) < self.rpm
                used = sum(t for _, t in self.tokens)
                ok_t = not self.tpm or used + est_tokens <= self.tpm or not self.tokens
                if ok_r and ok_t:
                    self.calls.append(now)
                    self.tokens.append((now, est_tokens))
                    return
                waits = []
                if not ok_r:
                    waits.append(60 - (now - self.calls[0]))
                if not ok_t:
                    waits.append(60 - (now - self.tokens[0][0]))
                delay = max(0.5, min(waits))
            time.sleep(delay)


_RETRY_IN = re.compile(r"(?:retry|try again)[^0-9]{0,20}([0-9]+(?:\.[0-9]+)?)\s*(ms|s|sec|seconds|m|min)", re.I)
_DAILY = re.compile(r"per[ _-]?day|daily|\bRPD\b|\bTPD\b", re.I)


class ChatClient:
    def __init__(self, provider_cfg, model_cfg, limiter=None, timeout=180, max_http_retries=6, max_wait_s=120):
        base = os.environ.get(provider_cfg["base_url_env"]) if provider_cfg.get("base_url_env") else None
        self.base_url = (base or provider_cfg["base_url"]).rstrip("/")
        self.auth_header = provider_cfg.get("auth_header", "bearer")  # "bearer" or "api-key" (Azure)
        env = provider_cfg.get("api_key_env")
        self.api_key = os.environ.get(env) if env else None
        if env and not self.api_key:
            raise ProviderError(f"environment variable {env} is not set for provider {model_cfg['provider']}")
        self.model_cfg = model_cfg
        self.limiter = limiter or RateLimiter(model_cfg.get("rpm"), model_cfg.get("tpm"))
        self.timeout = model_cfg.get("timeout_s", timeout)
        self.max_http_retries = model_cfg.get("max_http_retries", max_http_retries)
        self.max_wait_s = max_wait_s
        self.stop_event = None
        self.json_mode = model_cfg.get("json_mode", True)

    def wait_or_stop(self, seconds):
        if self.stop_event is None:
            if seconds:
                time.sleep(seconds)
        elif self.stop_event.wait(seconds):
            raise ProviderError("Stopped by the operator; resume to finish.")

    def _auth(self):
        if not self.api_key:
            return {}
        return {"api-key": self.api_key} if self.auth_header == "api-key" else {"Authorization": f"Bearer {self.api_key}"}

    def _post(self, payload):
        req = urllib.request.Request(
            self.base_url + "/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", **self._auth()},
            method="POST")
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            return json.loads(r.read().decode("utf-8"))

    def list_models(self):
        req = urllib.request.Request(self.base_url + "/models", headers=self._auth())
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read().decode("utf-8"))
        return sorted(m.get("id") for m in data.get("data", []))

    def complete(self, messages, params):
        if self.model_cfg.get("system_as_user"):
            # some models (e.g. older Gemma) reject a system role: send the same text as the first user turn
            sys_txt = "\n\n".join(m["content"] for m in messages if m["role"] == "system")
            rest = [m for m in messages if m["role"] != "system"]
            if rest and rest[0]["role"] == "user":
                rest = [{"role": "user", "content": sys_txt + "\n\n" + rest[0]["content"]}] + rest[1:]
            messages = rest
        payload = {"model": self.model_cfg["model_id"], "messages": messages}
        for k in ("temperature", "max_tokens", "seed", "top_p"):
            if params.get(k) is not None:
                payload[k] = params[k]
        payload.update(self.model_cfg.get("extra", {}))
        for k in getattr(self, "dropped", []):
            payload.pop(k, None)
        if getattr(self, "use_max_completion", False) and "max_tokens" in payload:
            payload["max_completion_tokens"] = payload.pop("max_tokens")
        if self.json_mode:
            payload["response_format"] = {"type": "json_object"}
        est = sum(len(m["content"]) for m in messages) // 4 + (params.get("max_tokens") or 1500)
        tpm = self.model_cfg.get("tpm")
        if tpm and est > tpm:
            raise ProviderError(f"{self.model_cfg['key']}: request needs about {est} tokens (prompt + max_tokens) but the "
                                f"configured tokens-per-minute limit is {tpm}; this model cannot run here on this tier. "
                                f"Use a paid tier or another provider (see the protocol, Models).")
        attempts, sw, note = 0, Stopwatch(), None
        while True:
            attempts += 1
            self.limiter.wait(est)
            self.wait_or_stop(0)
            try:
                data = self._post(payload)
                break
            except urllib.error.HTTPError as e:
                body = e.read().decode("utf-8", "replace")[:2000]
                if e.code == 400 and "response_format" in payload and re.search(r"response_format|json_object|json mode", body, re.I):
                    payload.pop("response_format")
                    self.json_mode = False
                    note = "response_format unsupported; retried without it"
                    continue
                if e.code == 400 and "max_tokens" in payload and "max_completion_tokens" in body:
                    # Some endpoints accept max_completion_tokens as the output limit.
                    payload["max_completion_tokens"] = payload.pop("max_tokens")
                    self.use_max_completion = True
                    note = "max_tokens renamed to max_completion_tokens"
                    continue
                if e.code == 400 and "temperature" in payload and re.search(r"temperature", body, re.I) \
                        and re.search(r"unsupported|does not support|only the default", body, re.I):
                    payload.pop("temperature")
                    self.dropped = getattr(self, "dropped", []) + ["temperature"]
                    note = "model only allows its default temperature; retried without it"
                    continue
                if e.code in (400, 422):
                    # some free endpoints reject optional settings (seed, reasoning_effort, top_p): drop the one named and retry
                    m = re.search(r'Unknown name \\?"(\w+)\\?"', body) or re.search(r"\b(seed|reasoning_effort|top_p|response_format)\b", body)
                    if m and m.group(1) in payload:
                        payload.pop(m.group(1))
                        self.model_cfg.setdefault("extra", {}).pop(m.group(1), None)
                        self.dropped = getattr(self, "dropped", []) + [m.group(1)]
                        note = f"provider rejected '{m.group(1)}'; retried without it"
                        continue
                if e.code == 429:
                    wait = self._retry_after(e, body)
                    if _DAILY.search(body) or (wait is not None and wait > self.max_wait_s):
                        raise QuotaExhausted(f"{self.model_cfg['key']}: quota exhausted: {body}", self.model_cfg["key"])
                    if attempts > self.max_http_retries:
                        raise QuotaExhausted(f"{self.model_cfg['key']}: still rate-limited after {attempts} tries: {body}", self.model_cfg["key"])
                    self.wait_or_stop(min(wait or 2 ** attempts + random.random(), self.max_wait_s))
                    continue
                if e.code == 413 or re.search(r"request too large|context length|maximum context|too many tokens", body, re.I):
                    raise ProviderError(f"{self.model_cfg['key']}: request too large for this provider or tier: {body[:300]}")
                if e.code >= 500 and attempts <= self.max_http_retries:
                    self.wait_or_stop(min(2 ** attempts + random.random(), 60))
                    continue
                raise ProviderError(f"HTTP {e.code}: {body[:500]}")
            except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
                if attempts <= self.max_http_retries:
                    self.wait_or_stop(min(2 ** attempts + random.random(), 60))
                    continue
                raise ProviderError(f"network error: {e}")
        choice = (data.get("choices") or [{}])[0]
        msg = choice.get("message") or {}
        text = msg.get("content")
        if isinstance(text, list):  # some providers return content parts
            text = "".join(p.get("text", "") for p in text if isinstance(p, dict))
        usage = data.get("usage") or {}
        sent = sum(len(m["content"]) for m in messages) // 4
        if self.model_cfg.get("provider") == "ollama" and usage.get("prompt_tokens") and usage["prompt_tokens"] < 0.6 * sent:
            # Ollama silently cuts prompts longer than its context window; the answer would then be garbage
            raise ProviderError(f"{self.model_cfg['key']}: Ollama read only {usage['prompt_tokens']} of about {sent} prompt "
                                f"tokens, so the prompt was cut. Restart Ollama with OLLAMA_CONTEXT_LENGTH=32768 "
                                f"(see RUN_ON_YOUR_LAPTOP.md).")
        reasoning = msg.get("reasoning_content") or msg.get("reasoning") or msg.get("_thoughts")
        if not reasoning and isinstance(text, str) and "<think>" in text:
            # some open models put their thinking inside <think>...</think> in the answer itself
            m = re.search(r"<think>(.*?)</think>", text, re.S)
            if m:
                reasoning = m.group(1).strip()
                text = text[:m.start()] + text[m.end():]
        if reasoning and not isinstance(reasoning, str):
            reasoning = json.dumps(reasoning, ensure_ascii=False)
        return Response(text=text or "", usage=usage, model_returned=data.get("model"),
                        response_id=data.get("id"), finish_reason=choice.get("finish_reason"),
                        latency_ms=sw.ms(), http_attempts=attempts, note=note, reasoning=reasoning or None)

    @staticmethod
    def _retry_after(e, body):
        ra = e.headers.get("Retry-After") if e.headers else None
        if ra:
            try:
                return float(ra)
            except ValueError:
                pass
        m = _RETRY_IN.search(body)
        if m:
            v = float(m.group(1))
            unit = m.group(2).lower()
            return v / 1000 if unit == "ms" else v * 60 if unit.startswith("m") and unit != "ms" else v
        return None


class ResponseCache:
    """Per-interview cache of model responses, keyed by request hash and occurrence.

    Lets an interview interrupted by a quota limit restart from the beginning and
    replay every earlier response exactly, then continue live.
    """

    def __init__(self, path):
        self.path = path
        self.entries = {}
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    rec = json.loads(line)
                    self.entries[(rec["key"], rec["occurrence"])] = rec["response"]
        self.seen = {}
        self._fh = path.open("a", encoding="utf-8")

    def next_key(self, key):
        n = self.seen.get(key, 0)
        self.seen[key] = n + 1
        return (key, n)

    def get(self, k):
        return self.entries.get(k)

    def put(self, k, response):
        self.entries[k] = response
        self._fh.write(json.dumps({"key": k[0], "occurrence": k[1], "response": response}, ensure_ascii=False) + "\n")
        self._fh.flush()

    def close(self):
        self._fh.close()


class LLMCaller:
    """One model in one interview: call, parse, validate, repair once, cache, log."""

    def __init__(self, client, model_cfg, log, cache, params, max_repairs=1):
        self.client = client
        self.cfg = model_cfg
        self.log = log
        self.cache = cache
        self.params = params
        self.max_repairs = max_repairs
        self.usage = {}
        self.models_returned = set()

    def _account(self, role, resp):
        u = self.usage.setdefault(role, {"calls": 0, "prompt_tokens": 0, "completion_tokens": 0,
                                         "reasoning_tokens": 0, "latency_ms": 0, "repairs": 0, "failures": 0,
                                         "truncated": 0})
        u["calls"] += 1
        u["prompt_tokens"] += int(resp.get("usage", {}).get("prompt_tokens") or 0)
        u["completion_tokens"] += int(resp.get("usage", {}).get("completion_tokens") or 0)
        det = resp.get("usage", {}).get("completion_tokens_details") or {}
        u["reasoning_tokens"] += int(det.get("reasoning_tokens") or 0)
        u["latency_ms"] += int(resp.get("latency_ms") or 0)
        return u

    def call_json(self, role, system, user_obj, validator, context=None):
        messages = [{"role": "system", "content": system},
                    {"role": "user", "content": json.dumps(user_obj, ensure_ascii=False)}]
        errors = []
        attempt_keys = []
        for attempt in range(self.max_repairs + 1):
            key = sha256_obj({"model": self.cfg["model_id"], "provider": self.cfg["provider"],
                              "params": self.params, "messages": messages, "role": role})
            ck = self.cache.next_key(key)
            attempt_keys.append(ck)
            cached = self.cache.get(ck)
            if cached is None:
                r = self.client.complete(messages, self.params) if not hasattr(self.client, "complete_role") \
                    else self.client.complete_role(role, messages, self.params, context or {})
                resp = {"text": r.text, "usage": r.usage, "model_returned": r.model_returned,
                        "response_id": r.response_id, "finish_reason": r.finish_reason,
                        "latency_ms": r.latency_ms, "http_attempts": r.http_attempts, "note": r.note,
                        "reasoning": r.reasoning}
                self.cache.put(ck, resp)
                replayed = False
            else:
                resp, replayed = cached, True
            parsed, perr = parse_json_loose(resp["text"])
            if perr:
                errors = [perr]
            else:
                try:
                    errors = list(validator(parsed))
                except Exception as e:  # a malformed but parseable object must never crash the interview
                    errors = [f"output has the wrong structure ({type(e).__name__}: {e})"]
            if resp.get("finish_reason") == "length":
                errors = ["output was cut off at max_tokens"] + errors
            u = self._account(role, resp)
            if resp.get("finish_reason") == "length":
                u["truncated"] += 1
            if resp.get("model_returned"):
                self.models_returned.add(resp["model_returned"])
            self.log.write("llm_call", role=role, model_key=self.cfg["key"], model_id=self.cfg["model_id"],
                           provider=self.cfg["provider"], attempt=attempt, replayed=replayed, request_hash=key,
                           params=self.params, messages=messages, response=resp, parsed=parsed,
                           validation_errors=errors)
            if not errors:
                return parsed, {"attempts": attempt + 1, "errors": []}
            if attempt < self.max_repairs:
                u["repairs"] += 1
                messages = messages + [
                    {"role": "assistant", "content": resp["text"] or ""},
                    {"role": "user", "content": "Your previous output was not valid: " + "; ".join(errors)[:1500]
                     + ". Output only the corrected JSON object, following the required format exactly."}]
        self.usage[role]["failures"] += 1
        # A failed logical call was never accepted into the transcript. Permit a
        # fresh generation on resume; successful earlier calls still replay.
        for failed_key in attempt_keys:
            self.cache.put(failed_key, None)
        return None, {"attempts": self.max_repairs + 1, "errors": errors}


class GeminiNativeClient(ChatClient):
    """Google's native Gemini API (generateContent) with the x-goog-api-key header.

    Translates native requests and responses into the format used by the shared client.
    """

    def _auth(self):
        return {"x-goog-api-key": self.api_key} if self.api_key else {}

    def _post(self, payload):
        msgs = payload["messages"]
        sys_txt = "\n\n".join(m["content"] for m in msgs if m["role"] == "system")
        contents = [{"role": "model" if m["role"] == "assistant" else "user", "parts": [{"text": m["content"]}]}
                    for m in msgs if m["role"] != "system"]
        gc = {}
        if "temperature" in payload:
            gc["temperature"] = payload["temperature"]
        mt = payload.get("max_tokens") or payload.get("max_completion_tokens")
        if mt:
            gc["maxOutputTokens"] = mt
        if "top_p" in payload:
            gc["topP"] = payload["top_p"]
        if "seed" in payload:
            gc["seed"] = payload["seed"]
        if (payload.get("response_format") or {}).get("type") == "json_object":
            gc["responseMimeType"] = "application/json"
        # reasoning_effort (low/medium/high) -> Gemini 3 thinkingLevel; without it Gemini thinks at its default (slow)
        effort = payload.get("reasoning_effort")
        if effort and not getattr(self, "no_thinking_level", False):
            gc["thinkingConfig"] = {"thinkingLevel": str(effort).lower(), "includeThoughts": True}
        body = {"contents": contents, "generationConfig": gc}
        if sys_txt:
            body["systemInstruction"] = {"parts": [{"text": sys_txt}]}

        def send(b):
            req = urllib.request.Request(f"{self.base_url}/models/{payload['model']}:generateContent",
                                         data=json.dumps(b).encode("utf-8"),
                                         headers={"Content-Type": "application/json", **self._auth()}, method="POST")
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                return json.loads(r.read().decode("utf-8"))

        try:
            data = send(body)
        except urllib.error.HTTPError as e:
            if e.code != 400 or "thinkingConfig" not in gc:
                raise
            # this model does not accept thinkingLevel: remember that and resend without it
            self.no_thinking_level = True
            gc.pop("thinkingConfig")
            data = send(body)
        cand = (data.get("candidates") or [{}])[0]
        parts = (cand.get("content") or {}).get("parts") or []
        text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
        thoughts_txt = "".join(p.get("text", "") for p in parts if p.get("thought")) or None
        fr = cand.get("finishReason") or ("BLOCKED:" + str((data.get("promptFeedback") or {}).get("blockReason")))
        fr = {"STOP": "stop", "MAX_TOKENS": "length", "SAFETY": "content_filter"}.get(fr, fr)
        um = data.get("usageMetadata") or {}
        thoughts = int(um.get("thoughtsTokenCount") or 0)
        return {"choices": [{"message": {"content": text, "_thoughts": thoughts_txt}, "finish_reason": fr}],
                "usage": {"prompt_tokens": int(um.get("promptTokenCount") or 0),
                          "completion_tokens": int(um.get("candidatesTokenCount") or 0) + thoughts,
                          "completion_tokens_details": {"reasoning_tokens": thoughts}},
                "model": data.get("modelVersion"), "id": data.get("responseId")}

    def list_models(self):
        req = urllib.request.Request(self.base_url + "/models?pageSize=1000", headers=self._auth())
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read().decode("utf-8"))
        return sorted(m.get("name", "").removeprefix("models/") for m in data.get("models", []))
