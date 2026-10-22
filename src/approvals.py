"""External actions are blocked unless explicitly approved."""
from dataclasses import dataclass, field

EXTERNAL_ACTIONS = frozenset({"publish_video", "reply_comment", "send_dm", "create_account", "deploy_store", "charge_provider"})

@dataclass
class ApprovalGate:
    approved: set[str] = field(default_factory=set)
    killed: bool = False

    def approve(self, action_id: str) -> None:
        if not action_id:
            raise ValueError("action ID required")
        self.approved.add(action_id)

    def check(self, action_id: str, action_type: str) -> None:
        if self.killed:
            raise PermissionError("system stopped")
        if action_type not in EXTERNAL_ACTIONS:
            raise ValueError("unknown action")
        if action_id not in self.approved:
            raise PermissionError("human approval required")
        self.approved.remove(action_id)
