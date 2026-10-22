"""Run a zero-cost, offline simulated agent conversation."""
from __future__ import annotations
import argparse
import json
from .agent_bus import Event
from .network import Network, Agent, Account
from .memory_store import MemoryStore
from .budget import Budget
from .approvals import ApprovalGate

def run_demo(niche: str, account_id: str, root: str = "data") -> dict:
    network = Network(max_events=12)
    network.add_account(Account(account_id=account_id, niche=niche))
    memory = MemoryStore(root + "/memory")
    budget = Budget()
    gate = ApprovalGate()

    def research(event: Event) -> list[Event]:
        memory.append(account_id, "agent", "research", "Research hypothesis: " + niche + " explainer", "offline simulation", 0.1)
        return [Event(run_id=event.run_id, agent_id="research", channel="research", topic="idea_proposed", payload={"idea": niche + " explainer", "verified": False}, hops=event.hops+1)]

    def script(event: Event) -> list[Event]:
        memory.append(account_id, "agent", "script", "Example hook for " + niche, "offline simulation", 0.1)
        return [Event(run_id=event.run_id, agent_id="script", channel="creative", topic="script_drafted", payload={"hook": "What most people miss about " + niche, "status": "example_only"}, hops=event.hops+1)]

    def reviewer(event: Event) -> list[Event]:
        return [Event(run_id=event.run_id, agent_id="quality", channel="alerts", topic="human_review_required", payload={"publish": False, "reason": "demo contains no verified media"}, hops=event.hops+1)]

    network.register(Agent("research", frozenset({"command"}), research))
    network.register(Agent("script", frozenset({"research"}), script))
    network.register(Agent("quality", frozenset({"creative"}), reviewer))
    transcript = network.dispatch(Event(run_id="demo-1", agent_id="coordinator", channel="command", topic="start", payload={"niche": niche}))
    return {"account": account_id, "mode": "offline_demo", "messages": [{"agent": e.agent_id, "channel": e.channel, "topic": e.topic, "payload": e.payload} for e in transcript], "monthly_spent_usd": str(budget.monthly_spent), "publish_approved": bool(gate.approved)}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--niche", default="technology")
    parser.add_argument("--account", default="demo_tech")
    parser.add_argument("--root", default="data")
    args = parser.parse_args()
    print(json.dumps(run_demo(args.niche, args.account, args.root), indent=2))

if __name__ == "__main__":
    main()
