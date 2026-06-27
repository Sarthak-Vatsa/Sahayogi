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
# This perfectly mirrors the "AI Reasoning" block from your master schema.

class ReasoningAnalysis(BaseModel):
    why_it_worked: str = Field(description="A detailed strategic explanation of why this reel performed well.")
    retention_strategy: str = Field(description="The specific technique used to keep viewers watching until the end.")
    psychological_triggers: list[str] = Field(description="List of psychological triggers used (e.g., curiosity, comfort, anticipation, empathy).")
    strongest_element: str = Field(description="The single most effective element of the reel.")
    weakest_element: str = Field(description="The element that could be most improved.")
    virality_factors: list[str] = Field(description="List of specific factors or mechanics that contributed to the reel's virality and shareability.")

class ReasoningOutput(BaseModel):
    reasoning: ReasoningAnalysis


# ==========================================
# 2. THE CORE FUNCTION
# ==========================================
def generate_strategic_reasoning(reel_path: str):
    """
    Reads a reel JSON that has already been processed by the collector and analyzer,
    and asks the AI to reverse-engineer its success.
    """
    print(f"[Strategist] Loading analyzed reel data from {reel_path}...")

    # 1. Load the existing data (which now includes metadata + vision analysis)
    with open(reel_path, "r", encoding="utf-8") as file:
        reel_data = json.load(file)

    # 2. Load the strategic prompt
    base_dir = Path(__file__).resolve().parent.parent
    prompt_path = base_dir / "prompts" / "explain_performance.txt"
    with open(prompt_path, "r", encoding="utf-8") as file:
        prompt_template = file.read()

    # Inject the ENTIRE reel_data dictionary this time, so the AI sees the vision analysis too
    final_prompt = prompt_template.replace("{reel_data}", json.dumps(reel_data, indent=2))

    # 3. Initialize Gemini
    client = genai.Client()

    print("[Strategist] Analyzing data relationships and generating strategy...")

    # 4. Make the API Call with the Reasoning schema
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=final_prompt,
        config={
            'response_mime_type': 'application/json',
            'response_schema': ReasoningOutput,
        },
    )

    # 5. Parse the JSON response
    reasoning_result = json.loads(response.text)

    # 6. Append the reasoning data to our master dictionary
    reel_data.update(reasoning_result)

    # 7. Save it back to the file
    with open(reel_path, "w", encoding="utf-8") as file:
        json.dump(reel_data, file, indent=4)

    print("[Strategist] Reasoning complete! Strategic insights successfully appended.")


# ==========================================
# 3. ISOLATED TEST BLOCK
# ==========================================
if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    test_reel_path = base_dir / "data" / "reels" / "dummy_reel_001.json"

    generate_strategic_reasoning(test_reel_path)