import tempfile
import unittest
from decimal import Decimal
from src.agent_bus import Event
from src.network import Network, Agent, Account
from src.budget import Budget
from src.memory_store import MemoryStore
from src.approvals import ApprovalGate

class NetworkTests(unittest.TestCase):
    def test_message_routing(self):
        network = Network()
        def responder(event):
            return [Event(run_id=event.run_id, agent_id="script", channel="creative", topic="draft", payload={"source":event.topic}, hops=event.hops+1)]
        network.register(Agent("script", frozenset({"research"}), responder))
        messages = network.dispatch(Event(run_id="r", agent_id="research", channel="research", topic="trend", payload={}))
        self.assertEqual([m.topic for m in messages], ["trend", "draft"])

    def test_account_registration(self):
        network = Network()
        network.add_account(Account("a", "tech"))
        with self.assertRaises(ValueError):
            network.add_account(Account("a", "other"))

    def test_budget_reservations(self):
        b = Budget(per_run_limit=Decimal("2"), monthly_limit=Decimal("3"))
        b.reserve("job1", "run1", "1.50")
        with self.assertRaises(PermissionError):
            b.reserve("job2", "run1", "1")
        b.settle("job1", "1.25")
        self.assertEqual(b.monthly_spent, Decimal("1.25"))

    def test_memory_isolation(self):
        with tempfile.TemporaryDirectory() as root:
            store = MemoryStore(root)
            store.append("a", "agent", "research", "idea", "source-url", 0.7)
            self.assertEqual(len(store.read("a", "agent", "research")), 1)
            self.assertEqual(store.read("b", "agent", "research"), [])
            with self.assertRaises(ValueError):
                store.read("../escape", "agent", "research")

    def test_approval_consumed(self):
        gate = ApprovalGate()
        with self.assertRaises(PermissionError):
            gate.check("post1", "publish_video")
        gate.approve("post1")
        gate.check("post1", "publish_video")
        with self.assertRaises(PermissionError):
            gate.check("post1", "publish_video")

if __name__ == "__main__":
    unittest.main()
