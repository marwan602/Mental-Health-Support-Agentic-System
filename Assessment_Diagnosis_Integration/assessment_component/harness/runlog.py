"""Append-only event log for one interview (events.jsonl).

Every step of an interview writes one JSON line: stage changes, every model call
(full request, raw response, parsed output, validation errors, tokens, latency),
evidence accepted or rejected, targets offered and chosen, safety events and the
end reason. Lines carry a sequence number and a UTC timestamp, so the whole run
can be audited or replayed line by line.
"""
import json
import threading
from pathlib import Path

from .util import now_iso


class EventLog:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.seq = 0
        self._lock = threading.Lock()
        # a fresh log per attempt; earlier attempts are kept with a suffix by the runner
        self._fh = self.path.open("w", encoding="utf-8")

    def write(self, event_type, **data):
        with self._lock:
            self.seq += 1
            rec = {"seq": self.seq, "ts": now_iso(), "type": event_type, **data}
            self._fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            self._fh.flush()
            return rec

    def close(self):
        with self._lock:
            if not self._fh.closed:
                self._fh.close()


class NullLog:
    seq = 0

    def write(self, event_type, **data):
        return {"type": event_type, **data}

    def close(self):
        pass
