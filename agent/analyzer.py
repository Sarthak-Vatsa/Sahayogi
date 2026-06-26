import json
import os
from pathlib import Path
from pydantic import BaseModel, Field
from google import genai
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()

# ==========================================
# 1. DEFINE THE STRICT OUTPUT SCHEMA (PYDANTIC)
# ==========================================
# These classes perfectly mirror your reel_schema.json blueprints.
# The 'Field' descriptions tell the AI exactly what to look for.

class HookAnalysis(BaseModel):
    visual_hook: str = Field(description="Description of the visual hook in the first 3 seconds")
    written_hook: str = Field(description="The on-screen text used to hook the viewer")
    spoken_hook: str = Field(description="The first thing said by the character/voiceover. If none, write 'None'.")
    hook_strength: int = Field(description="Score from 1-10 on how strong the hook is based on emotional pull")
    hook_type: str = Field(description="Type of hook (e.g., curiosity, emotional, pattern interrupt)")

class StoryAnalysis(BaseModel):
    structure: str = Field(description="The narrative structure (e.g., Problem -> Resolution)")
    payoff: str = Field(description="What is the final payoff or climax?")
    ending_type: str = Field(description="Type of ending (e.g., loop, cliffhanger, resolution)")
    surprise_present: bool = Field(description="Is there a twist or surprise?")

class VisualAnalysis(BaseModel):
    camera_angle: str = Field(description="Predominant camera angle")
    camera_motion: str = Field(description="Camera movement style")
    lighting: str = Field(description="Lighting style (e.g., soft, harsh, warm, cool)")
    color_palette: str = Field(description="Dominant colors used")
    main_subject: str = Field(description="The primary subject on screen")
    subject_count: int = Field(description="Number of subjects on screen")
    eye_contact: bool = Field(description="Does the character make direct eye contact with the camera?")
    background: str = Field(description="Description of the background setting")
    scene_changes: int = Field(description="Number of distinct scene cuts")

class EmotionAnalysis(BaseModel):
    primary: str = Field(description="Primary emotion evoked (e.g., comfort, joy, sadness)")
    secondary: str = Field(description="Secondary emotion evoked")
    intensity: int = Field(description="Score from 1-10 on emotional intensity")

class EditingAnalysis(BaseModel):
    pacing: str = Field(description="Pacing of the edit (e.g., slow, fast, dynamic)")
    average_shot_length: float = Field(description="Estimated average duration of each shot in seconds")
    transition_style: str = Field(description="Style of cuts/transitions")
    text_frequency: str = Field(description="How often text appears on screen (low, medium, high)")

class AudioAnalysis(BaseModel):
    type: str = Field(description="Primary audio type (e.g., ASMR, trending music, voiceover)")
    music: str = Field(description="Description of the music track if present")
    ambient: bool = Field(description="Are there ambient/nature sounds?")
    voiceover: bool = Field(description="Is there a voiceover narrative?")

# This is the master wrapper that holds all the blocks above
class VisionAnalysisOutput(BaseModel):
    hook: HookAnalysis
    story: StoryAnalysis
    visual: VisualAnalysis
    emotion: EmotionAnalysis
    editing: EditingAnalysis
    audio: AudioAnalysis


# ==========================================
# 2. THE CORE FUNCTION
# ==========================================
def analyze_reel_data(reel_path: str):
    """
    Reads a partially filled reel JSON, sends it to Gemini for analysis,
    and appends the structured results back to the JSON file.
    """
    print(f"[Analyzer] Loading reel data from {reel_path}...")

    # 1. Load the existing basic data (created by collector.py)
    with open(reel_path, "r", encoding="utf-8") as file:
        reel_data = json.load(file)

    # 2. Load the prompt instructions
    base_dir = Path(__file__).resolve().parent.parent
    prompt_path = base_dir / "prompts" / "analyze_reel.txt"
    with open(prompt_path, "r", encoding="utf-8") as file:
        prompt_template = file.read()

    # Inject the metadata into the prompt
    final_prompt = prompt_template.replace("{metadata}", json.dumps(reel_data.get("metadata", {})))

    # 3. Initialize the Gemini Client
    client = genai.Client()

    print("[Analyzer] Sending data to Gemini API for structural analysis...")

    # 4. Make the API Call, forcing the output to match our Pydantic schema
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=final_prompt,
        config={
            'response_mime_type': 'application/json',
            'response_schema': VisionAnalysisOutput,
        },
    )

    # 5. Parse the guaranteed JSON response
    analysis_result = json.loads(response.text)

    # 6. Append the new data to our master reel_data dictionary
    reel_data.update(analysis_result)

    # 7. Save the updated dictionary back to the file, overwriting the old one
    with open(reel_path, "w", encoding="utf-8") as file:
        json.dump(reel_data, file, indent=4)

    print("[Analyzer] Analysis complete! Data successfully appended to JSON.")


# ==========================================
# 3. ISOLATED TEST BLOCK
# ==========================================
if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    test_reel_path = base_dir / "data" / "reels" / "dummy_reel_001.json"

    # Run the function
    analyze_reel_data(test_reel_path)