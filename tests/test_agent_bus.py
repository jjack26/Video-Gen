import tempfile
import unittest
from pathlib import Path
from src.agent_bus import Event, publish

class BusTests(unittest.TestCase):
    def test_publish_event(self):
        with tempfile.TemporaryDirectory() as root:
            event = Event(run_id="r1", agent_id="research", channel="research", topic="idea", payload={"title": "demo"})
            self.assertEqual(publish(event, root), event.event_id)
            self.assertTrue((Path(root) / "events.jsonl").exists())

    def test_invalid_channel(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(ValueError):
                publish(Event(run_id="r", agent_id="a", channel="invalid", topic="t", payload={}), root)

    def test_hop_limit(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(ValueError):
                publish(Event(run_id="r", agent_id="a", channel="command", topic="t", payload={}, hops=6), root)
