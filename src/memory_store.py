"""Local JSONL memory with account and agent isolation."""
from __future__ import annotations
import json
from pathlib import Path
import re
from datetime import datetime, timezone

SAFE_ID = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
LAYERS = frozenset({"agent", "team", "global"})

class MemoryStore:
    def __init__(self, root: str = "data/memory"):
        self.root = Path(root)

    def _path(self, account_id: str, layer: str, owner: str) -> Path:
        if layer not in LAYERS or not SAFE_ID.fullmatch(account_id) or not SAFE_ID.fullmatch(owner):
            raise ValueError("invalid memory namespace")
        return self.root / account_id / layer / f"{owner}.jsonl"

    def append(self, account_id: str, layer: str, owner: str, fact: str, source: str, confidence: float) -> None:
        if not 0 <= confidence <= 1 or not source.strip() or not fact.strip():
            raise ValueError("memory requires fact, source, and confidence")
        path = self._path(account_id, layer, owner)
        path.parent.mkdir(parents=True, exist_ok=True)
        record = {"fact": fact, "source": source, "confidence": confidence, "created_at": datetime.now(timezone.utc).isoformat()}
        with path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record) + "\n")

    def read(self, account_id: str, layer: str, owner: str) -> list[dict]:
        path = self._path(account_id, layer, owner)
        if not path.exists():
            return []
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
