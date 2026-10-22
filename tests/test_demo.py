import tempfile
import unittest
from src.demo import run_demo
from src.llm_provider import draft_text, ProviderDisabled
from src.production import VideoJob, HiggsfieldAdapter

class DemoTests(unittest.TestCase):
    def test_offline_workflow(self):
        with tempfile.TemporaryDirectory() as root:
            result = run_demo("technology", "tech_01", root)
            self.assertEqual([m["topic"] for m in result["messages"]], ["start", "idea_proposed", "script_drafted", "human_review_required"])
            self.assertEqual(result["monthly_spent_usd"], "0")
            self.assertFalse(result["publish_approved"])

    def test_provider_off_by_default(self):
        with self.assertRaises(ProviderDisabled):
            draft_text("You write scripts", "Write a hook")

    def test_higgsfield_not_connected(self):
        with self.assertRaises(NotImplementedError):
            HiggsfieldAdapter().submit(VideoJob("tech_01", "script", "storyboard"))

if __name__ == "__main__":
    unittest.main()
