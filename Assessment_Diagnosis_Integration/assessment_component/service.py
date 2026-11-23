"""Persisted turn-level API. A session ID is an identifier, not an access token."""
import os
import re
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

from .harness.util import ROOT, dump_json, load_json
from .run import EXCLUDED_TOPICS, build_client, interview


@contextmanager
def session_lock(folder):
    with (folder / ".lock").open("a+b") as handle:
        handle.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            raise RuntimeError("This session is busy. Retry the same request.") from error
        yield


class AssessmentService:
    def __init__(self, storage, *, mock=False):
        self.storage = Path(storage).resolve()
        self.mock = mock
        self.cfg = load_json(ROOT / "config.json")
        self.model = self.cfg["interviewers"]["nemotron_ultra"]
        self.client = build_client(self.cfg, self.model, mock)
        roles = ("extractor","planner","conversation","synthesis","care_context","final_review")
        self.prompts = {r:(ROOT/"prompts"/(r+".txt")).read_text(encoding="utf8") for r in roles}

    def _folder(self, session_id):
        if not isinstance(session_id, str) or not re.fullmatch(r"[0-9a-f]{32}", session_id):
            raise ValueError("Invalid session ID.")
        folder = self.storage / session_id
        if not (folder/"inputs.json").is_file():
            raise KeyError("Unknown session.")
        return folder

    def start_session(self, *, fictional_name, age):
        if type(age) is not int or age < 18 or not isinstance(fictional_name, str) or not fictional_name.strip():
            raise ValueError("Supply a fictional adult's name and age in whole years (18 or older).")
        folder = self.storage / uuid4().hex
        folder.mkdir(parents=True)
        with session_lock(folder):
            data = {"name":fictional_name.strip(),"age":age,"mock":self.mock,"replies":{}}
            dump_json(folder/"inputs.json", data)
            return self._advance(folder, data)

    def get_session(self, session_id):
        folder = self._folder(session_id)
        with session_lock(folder):
            return self._current(folder, load_json(folder/"inputs.json"))

    def _current(self, folder, data):
        if data["mock"] != self.mock:
            raise ValueError("Use the same live or mock mode as the original session.")
        path = folder/"current.json"
        if path.exists():
            result = load_json(path)
            if result["accepted_replies"] == len(data["replies"]):
                return result
        return self._advance(folder, data)

    def submit_reply(self, session_id, *, question_id, text):
        folder = self._folder(session_id)
        if not isinstance(text, str) or not text.strip() or not isinstance(question_id, str):
            raise ValueError("Supply the displayed question ID and a nonempty reply.")
        if EXCLUDED_TOPICS.search(text):
            raise ValueError("Input is outside this fictional study's scope.")
        text = text.strip()
        with session_lock(folder):
            data = load_json(folder/"inputs.json")
            if question_id in data["replies"]:
                if data["replies"][question_id] != text:
                    raise ValueError("A different reply was already accepted for this question.")
                return self._current(folder, data)
            result = self._current(folder, data)
            if result["state"] != "awaiting_reply" or question_id != result["question_id"]:
                raise ValueError("Reply to the currently displayed question.")
            data["replies"][question_id] = text
            dump_json(folder/"inputs.json", data)
            return self._advance(folder, data)

    def _advance(self, folder, data):
        status = interview(folder, data["name"], data["replies"], self.cfg, self.client, self.prompts, self.model, self.mock)
        if status["state"] not in ("awaiting_reply","complete"):
            raise RuntimeError(f"Assessment {status['state']}. Inspect status.json and retry the same session.")
        last = load_json(folder/"transcript.json")[-1]
        complete = status["state"] == "complete"
        result = {"session_id":folder.name,"state":status["state"],"question_id":None if complete else last["message_id"],
                  "text":last["text"],"accepted_replies":len(data["replies"]),
                  "end_reason":status.get("end_reason"),
                  "handoff":load_json(folder/"assessment_handoff.json") if complete else None}
        dump_json(folder/"current.json", result)
        return result
