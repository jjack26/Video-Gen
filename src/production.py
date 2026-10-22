"""Provider-neutral job contracts. No video jobs are submitted here."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class Status(str, Enum):
    PLANNED = "planned"
    AWAITING_APPROVAL = "awaiting_approval"
    SUBMITTED = "submitted"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass(frozen=True)
class VideoJob:
    account_id: str
    script: str
    storyboard: str
    aspect_ratio: str = "9:16"
    duration_seconds: int = 8
    status: Status = Status.PLANNED

    def __post_init__(self):
        if self.aspect_ratio != "9:16" or not 1 <= self.duration_seconds <= 60:
            raise ValueError("unsupported video settings")

class HiggsfieldAdapter:
    """Intentional integration boundary: subscription and API eligibility need confirmation."""
    def submit(self, job: VideoJob) -> str:
        raise NotImplementedError("Higgsfield provider API not connected. No credits charged.")
