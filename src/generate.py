"""Create Japanese and English educational video draft storyboards."""
import argparse
import json
from pathlib import Path

TOPICS = {
    "colors": {
        "ja": ("いろをおぼえよう", ["あかい りんご", "あおい そら", "きいろい ほし"]),
        "en": ("Let's Learn Colors", ["red apple", "blue sky", "yellow star"]),
    },
    "numbers": {
        "ja": ("かずをかぞえよう", ["ほしが ひとつ", "はなが ふたつ", "りんごが みっつ"]),
        "en": ("Let's Count", ["one star", "two flowers", "three apples"]),
    },
}

def generate(topic, language):
    title, phrases = TOPICS[topic][language]
    return {
        "title": title, "topic": topic, "language": language,
        "made_for_kids": True, "status": "human_review_required",
        "scenes": [
            {"seconds": 7, "narration": phrase, "visual_prompt": f"Original friendly pastel illustration: {phrase}. No text or real people."}
            for phrase in phrases
        ],
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", choices=TOPICS, default="colors")
    parser.add_argument("--language", choices=("ja", "en"), required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(generate(args.topic, args.language), ensure_ascii=False, indent=2), encoding="utf-8")
    print(path)
