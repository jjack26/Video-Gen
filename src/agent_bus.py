"""Local append-only event bus scaffold. No network requests."""
from __future__ import annotations
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
from uuid import uuid4

CHANNELS = frozenset({"command", "research", "creative", "publishing", "community", "commerce", "analytics", "alerts"})
MAX_HOPS = 5

@dataclass(frozen=True)
class Event:
    run_id: str
    agent_id: str
    channel: str
    topic: str
    payload: dict
    correlation_id: str = field(default_factory=lambda: str(uuid4()))
    event_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    hops: int = 0

def publish(event: Event, root: str = "data/events") -> str:
    if event.channel not in CHANNELS:
        raise ValueError("unknown channel")
    if not 0 <= event.hops <= MAX_HOPS:
        raise ValueError("event hop limit exceeded")
    if not event.run_id or not event.agent_id or not event.topic:
        raise ValueError("missing required event metadata")
    folder = Path(root)
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / "events.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(asdict(event)) + "\n")
    return event.event_id
