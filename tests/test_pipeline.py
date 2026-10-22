import tempfile
import unittest
from pathlib import Path

from src.pipeline import create_run, record_memory, STAGES


class PipelineTests(unittest.TestCase):
    def test_run_requires_goal(self):
        with self.assertRaises(ValueError):
            create_run(" ")

    def test_run_defaults_to_manual_approval(self):
        with tempfile.TemporaryDirectory() as root:
            run = create_run("Create a product explainer", root)
            self.assertFalse(run["approval"]["publish"])
            self.assertEqual(len(run["stages"]), len(STAGES))
            self.assertTrue((Path(root) / "latest_run.json").exists())

    def test_agent_memory_is_separate(self):
        with tempfile.TemporaryDirectory() as root:
            record_memory("script", {"lesson": "shorter hook"}, root)
            record_memory("research", {"lesson": "check source dates"}, root)
            self.assertEqual(len(list(Path(root).glob("*.jsonl"))), 2)

    def test_invalid_agent_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(ValueError):
                record_memory("../other", {}, root)


if __name__ == "__main__":
    unittest.main()
