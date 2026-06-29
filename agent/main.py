import os
from pathlib import Path

# Import our functional tools from our custom modules
from agent.collector import fetch_reel_metadata
from agent.analyzer import analyze_reel_data
from agent.reasoning import generate_strategic_reasoning
from agent.trend_engine import detect_market_trends
from agent.report_generator import generate_markdown_report

def run_sahayogi_pipeline():
    """
    Coordinates the execution of the entire Sahayogi content strategy engine.
    """
    print("=============================================")
    print("🤖 SAHAYOGI AI CONTENT STRATEGIST: ACCELERATING")
    print("=============================================\n")

    base_dir = Path(__file__).resolve().parent.parent

    # Simulating a list of target URLs we want to process this week
    # In Phase 2, this will be dynamically populated by your competitors list!
    target_urls = [
        "https://www.instagram.com/reel/DZUooz3Tvio/?igsh=MWVrY2ZpandkdmE0MQ=="
    ]

    print(f"[Main Pipeline] Processing a batch of {len(target_urls)} reels...")

    # --- PHASE 1: INDIVIDUAL REEL PROCESSING ---
    # We step through each reel and apply our core analysis stack
    for url in target_urls:
        print(f"\n--- Processing Reel: {url} ---")

        # Step 1: Ingest/Fetch the reel metadata
        # (Currently pointing to our local dummy file layout)
        reel_metadata = fetch_reel_metadata(url)

        if not reel_metadata:
            print(f"[Main Error] Skipping {url} due to ingestion failure.")
            continue

        # For testing, our dummy file is saved at: data/reels/dummy_reel_001.json
        target_file_path = base_dir / "data" / "reels" / "dummy_reel_001.json"

        # Step 2: Run Multimodal Analysis via Gemini
        analyze_reel_data(str(target_file_path))

        # Step 3: Run Performance Reasoning Engine
        generate_strategic_reasoning(str(target_file_path))

    # --- PHASE 2: MACRO ENGINE AGGREGATION ---
    print("\n---------------------------------------------")
    print("📊 INDIVIDUAL RUNS FINISHED. BOOTING TREND & RECOMMENDATION ENGINES")
    print("---------------------------------------------")

    # Step 4: Aggregate data blocks to identify overarching trends
    detect_market_trends()

    # Step 5: Inject trend profiles and brand files to personalize strategy
    # Note: Import inline to prevent cross-import pollution during sequential tests
    from agent.recommendation_engine import generate_recommendations
    generate_recommendations()

    # Step 6: Compile everything into the beautiful human briefing
    generate_markdown_report()

    print("\n=============================================")
    print("🎉 PIPELINE RUN COMPLETE. YOUR WEEKLY STRATEGY IS READY!")
    print("=============================================")

if __name__ == "__main__":
    run_sahayogi_pipeline()