import json
import os
from pathlib import Path
from pydantic import BaseModel, Field
from google import genai
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# 1. DEFINE THE STRICT OUTPUT SCHEMA
# ==========================================

class TrendInsight(BaseModel):
    trend_name: str = Field(description="A catchy, clear name for the trend (e.g., 'The ASMR Retention Spike').")
    pattern_description: str = Field(description="What is the actual statistical or psychological pattern you noticed?")
    evidence: str = Field(description="Cite specific examples or data points from the provided reels to prove this trend.")
    strategic_rule: str = Field(description="A one-sentence actionable rule for the creator to follow based on this trend.")

class TrendReport(BaseModel):
    trends: list[TrendInsight] = Field(description="A list of the 3 to 5 most important overarching trends.")
    market_summary: str = Field(description="A 2-sentence summary of the current state of the niche based on this data.")


# ==========================================
# 2. THE CORE FUNCTION
# ==========================================
def detect_market_trends():
    """
    Reads all analyzed reels, aggregates the data, and generates a trend report.
    """
    base_dir = Path(__file__).resolve().parent.parent
    reels_dir = base_dir / "data" / "reels"

    print("[Trend Engine] Scanning for processed reels...")

    aggregated_data = []

    # 1. Loop through all JSON files in the reels directory
    for filename in os.listdir(reels_dir):
        if filename.endswith(".json"):
            file_path = reels_dir / filename
            with open(file_path, "r", encoding="utf-8") as file:
                reel = json.load(file)

                # 2. Token Economy: We only keep the data the AI actually needs to find trends.
                # We strip out the URLs, collection times, and raw IDs.
                condensed_reel = {
                    "views": reel.get("metadata", {}).get("views"),
                    "likes": reel.get("metadata", {}).get("likes"),
                    "duration": reel.get("metadata", {}).get("duration_seconds"),
                    "audio_type": reel.get("audio", {}).get("type"),
                    "camera_angle": reel.get("visual", {}).get("camera_angle"),
                    "camera_motion": reel.get("visual", {}).get("camera_motion"),
                    "eye_contact": reel.get("visual", {}).get("eye_contact"),
                    "hook": reel.get("hook", {}),
                    "story_structure": reel.get("story", {}).get("structure"),
                    "reasoning": reel.get("reasoning", {}).get("why_it_worked")
                }
                aggregated_data.append(condensed_reel)

    print(f"[Trend Engine] Aggregated data from {len(aggregated_data)} reels.")

    # 3. Load the prompt
    prompt_path = base_dir / "prompts" / "detect_trends.txt"
    with open(prompt_path, "r", encoding="utf-8") as file:
        prompt_template = file.read()

    final_prompt = prompt_template.replace("{batch_data}", json.dumps(aggregated_data, indent=2))

    # 4. Make the API Call
    client = genai.Client()
    print("[Trend Engine] Analyzing dataset for macro-patterns...")

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=final_prompt,
        config={
            'response_mime_type': 'application/json',
            'response_schema': TrendReport,
        },
    )

    # 5. Parse and save the Trend Report
    trend_report_data = json.loads(response.text)

    # We save this to a completely new file, because it applies to the whole market, not just one video.
    trends_out_path = base_dir / "data" / "trends" / "weekly_trends.json"

    # Ensure the trends directory exists
    trends_out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(trends_out_path, "w", encoding="utf-8") as file:
        json.dump(trend_report_data, file, indent=4)

    print(f"[Trend Engine] Success! Trend report saved to {trends_out_path}")


# ==========================================
# 3. ISOLATED TEST BLOCK
# ==========================================
if __name__ == "__main__":
    detect_market_trends()