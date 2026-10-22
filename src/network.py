"""Multi-account local coordination with bounded event routing."""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque
from typing import Callable
from .agent_bus import Event

@dataclass(frozen=True)
class Account:
    account_id: str
    niche: str
    platform: str = "tiktok"
    strategy: str = "audience_first"
    monetization: str = "undecided"
    authorized: bool = False

@dataclass(frozen=True)
class Agent:
    agent_id: str
    channels: frozenset[str]
    handler: Callable[[Event], list[Event]]

@dataclass
class Network:
    agents: dict[str, Agent] = field(default_factory=dict)
    accounts: dict[str, Account] = field(default_factory=dict)
    transcript: list[Event] = field(default_factory=list)
    max_events: int = 50
    max_hops: int = 5

    def register(self, agent: Agent) -> None:
        if agent.agent_id in self.agents:
            raise ValueError("duplicate agent")
        self.agents[agent.agent_id] = agent

    def add_account(self, account: Account) -> None:
        if not account.account_id or account.account_id in self.accounts:
            raise ValueError("invalid or duplicate account")
        self.accounts[account.account_id] = account

    def dispatch(self, first: Event) -> list[Event]:
        queue = deque([first])
        seen: set[str] = set()
        emitted = 0
        while queue:
            if emitted >= self.max_events:
                raise RuntimeError("event budget exceeded")
            event = queue.popleft()
            if event.event_id in seen:
                continue
            if event.hops > self.max_hops:
                raise RuntimeError("hop limit exceeded")
            seen.add(event.event_id)
            self.transcript.append(event)
            emitted += 1
            for agent in self.agents.values():
                if event.channel not in agent.channels or event.agent_id == agent.agent_id:
                    continue
                for child in agent.handler(event):
                    if child.agent_id != agent.agent_id or child.run_id != event.run_id:
                        raise ValueError("invalid emitted event origin")
                    if child.hops != event.hops + 1:
                        raise ValueError("invalid hop count")
                    if child.hops > self.max_hops:
                        raise RuntimeError("hop limit exceeded")
                    queue.append(child)
        return self.transcript[-emitted:]
