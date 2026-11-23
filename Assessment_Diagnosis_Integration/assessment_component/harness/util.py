"""Small shared helpers: hashing, JSON parsing, text normalisation, paths."""
import hashlib
import json
import re
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_obj(obj):
    return sha256_text(json.dumps(obj, sort_keys=True, ensure_ascii=False))


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_text_atomically(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    # A sync or preview process can briefly hold the destination file.
    for attempt in range(9):
        try:
            tmp.replace(path)
            return
        except PermissionError:
            if attempt == 8:
                raise
            time.sleep(min(0.05 * 2**attempt, 1))


def dump_json(path, obj):
    write_text_atomically(path, json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE)


def parse_json_loose(text):
    """Parse a model reply that should be one JSON object.

    Accepts code fences and leading/trailing prose, but returns (obj, None) only
    when exactly one top-level JSON object can be decoded. Returns (None, error)
    otherwise. The raw text is always logged by the caller, so nothing is lost.
    """
    if text is None:
        return None, "empty response"
    s = text.strip()
    s = _FENCE.sub("", s).strip()
    try:
        obj = json.loads(s)
        if isinstance(obj, dict):
            return obj, None
        return None, "top-level JSON is not an object"
    except json.JSONDecodeError:
        pass
    start = s.find("{")
    if start < 0:
        return None, "no JSON object found"
    dec = json.JSONDecoder()
    try:
        obj, end = dec.raw_decode(s[start:])
    except json.JSONDecodeError as e:
        return None, f"invalid JSON: {e.msg} at {e.pos}"
    if not isinstance(obj, dict):
        return None, "top-level JSON is not an object"
    rest = s[start + end:].strip()
    if "{" in rest:
        return None, "more than one JSON object in response"
    return obj, None


def norm_text(s):
    """Normalise for quote matching: Unicode NFKC, straight quotes, collapsed spaces, case-folded."""
    if s is None:
        return ""
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"\s+", " ", s).strip()
    return s.casefold()


class Stopwatch:
    def __init__(self):
        self.t0 = time.monotonic()

    def ms(self):
        return int((time.monotonic() - self.t0) * 1000)
