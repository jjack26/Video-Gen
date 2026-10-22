"""Offline, deterministic pipeline scaffold. No external API calls."""
from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone

STAGES = ("research", "strategy", "script", "storyboard", "generation", "quality", "analytics")


def create_run(goal: str, root: str = "data") -> dict:
    if not goal.strip():
        raise ValueError("goal must not be empty")
    run = {
        "goal": goal.strip(),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "awaiting_research",
        "stages": {stage: "pending" for stage in STAGES},
        "approval": {"publish": False},
    }
    folder = Path(root)
    folder.mkdir(parents=True, exist_ok=True)
    filename = folder / "latest_run.json"
    filename.write_text(json.dumps(run, indent=2), encoding="utf-8")
    return run


def memory_path(agent: str, root: str = "data/memory") -> Path:
    if agent not in STAGES and agent != "coordinator":
        raise ValueError("unknown agent")
    path = Path(root) / f"{agent}.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def record_memory(agent: str, event: dict, root: str = "data/memory") -> None:
    path = memory_path(agent, root)
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps({"at": datetime.now(timezone.utc).isoformat(), "event": event}) + "\n")
