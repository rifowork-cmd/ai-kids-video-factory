import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from generate import TOPICS, generate

class StoryboardTests(unittest.TestCase):
    def test_all_languages_and_topics(self):
        for topic in TOPICS:
            for language in ("ja", "en"):
                draft = generate(topic, language)
                self.assertEqual(len(draft["scenes"]), 3)
                self.assertTrue(draft["made_for_kids"])
                self.assertEqual(draft["status"], "human_review_required")
                self.assertTrue(all(s["seconds"] > 0 for s in draft["scenes"]))

if __name__ == "__main__":
    unittest.main()
