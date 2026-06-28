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
class ReelConcept(BaseModel):
    title: str = Field(description="A catchy internal working title for this reel concept.")
    target_trend: str = Field(description="Which specific market trend this concept is adapting.")
    recommended_character: str = Field(description="Which character (e.g., Pekka, Peppo, Nibbo) is best suited for this.")
    visual_hook: str = Field(description="Detailed description of the first 3 seconds visually.")
    written_hook: str = Field(description="The on-screen text to use.")
    audio_strategy: str = Field(description="Instructions for sound design (e.g., specific ASMR, music vibe).")
    adaptation_reasoning: str = Field(description="Why this safely adapts the trend without violating brand constraints.")
    difficulty_score: int = Field(description="Score from 1-10 on how hard this would be to animate/produce.")

class StrategyReport(BaseModel):
    overview: str = Field(description="A brief motivational message to the creator about this week's strategy.")
    concepts: list[ReelConcept] = Field(description="List of 2 to 3 actionable reel concepts.")


# ==========================================
# 2. THE CORE FUNCTION
# ==========================================
def generate_recommendations():
    print("[Personalization Engine] Booting up...")
    base_dir = Path(__file__).resolve().parent.parent

    # --- STEP 1: Compile the Brand Identity ---
    print("[Personalization Engine] Loading modular brand configurations...")
    config_dir = base_dir / "config"
    brand_identity = {}

    # We load each of your split config files into one master dictionary for the AI
    config_files = ["brand_context.json", "characters.json", "content_rules.json", "content_themes.json", "creator_goals.json"]
    for filename in config_files:
        try:
            with open(config_dir / filename, "r", encoding="utf-8") as f:
                # We use the filename (without .json) as the key
                key_name = filename.replace(".json", "")
                brand_identity[key_name] = json.load(f)
        except FileNotFoundError:
            print(f"[Warning] Could not find {filename}. Skipping.")

    # --- STEP 2: Load the Market Trends ---
    print("[Personalization Engine] Loading current market trends...")
    trends_path = base_dir / "data" / "trends" / "weekly_trends.json"
    with open(trends_path, "r", encoding="utf-8") as f:
        market_trends = json.load(f)

    # --- STEP 3: Prepare the Prompt ---
    prompt_path = base_dir / "prompts" / "generate_recommendations.txt"
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    # Inject both massive JSON objects into the prompt
    final_prompt = prompt_template.replace("{brand_identity}", json.dumps(brand_identity, indent=2))
    final_prompt = final_prompt.replace("{market_trends}", json.dumps(market_trends, indent=2))

    # --- STEP 4: Call Gemini ---
    print("[Personalization Engine] Cross-referencing trends with brand constraints. Generating strategy...")
    client = genai.Client()

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=final_prompt,
        config={
            'response_mime_type': 'application/json',
            'response_schema': StrategyReport,
        },
    )

    # --- STEP 5: Save the Recommendations ---
    recommendations_data = json.loads(response.text)

    reports_out_path = base_dir / "data" / "reports" / "weekly_strategy.json"
    reports_out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(reports_out_path, "w", encoding="utf-8") as f:
        json.dump(recommendations_data, f, indent=4)

    print(f"[Personalization Engine] Success! Strategy saved to {reports_out_path}")


# ==========================================
# 3. ISOLATED TEST BLOCK
# ==========================================
if __name__ == "__main__":
    generate_recommendations()