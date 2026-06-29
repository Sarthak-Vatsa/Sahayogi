import os
import json
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv
from apify_client import ApifyClient

# Load the API keys from .env
load_dotenv()

def fetch_reel_metadata(url: str) -> dict:
    """
    Scrapes a live Instagram reel using Apify's dedicated Reel Scraper
    and maps the deep raw data into our strict Sahayogi reel_schema.
    """
    print(f"[Collector] Initializing LIVE scrape for URL: {url}")

    apify_token = os.getenv("APIFY_API_TOKEN")
    if not apify_token:
        print("[Error] APIFY_API_TOKEN not found in .env file.")
        return {}

    # 1. Initialize the Apify Client
    client = ApifyClient(apify_token)

    # 2. Configure the Scraper Input
    # Using 'directUrls' to target exactly one reel for our Stage 1 test
    run_input = {
        "username": [url]  # Apify calls this 'username' even when you pass a direct reel URL
    }

    print("[Collector] Contacting Apify servers using 'instagram-reel-scraper'...")

    try:
        # 3. Run the Dedicated Reel Scraper Actor
        run = client.actor("apify/instagram-reel-scraper").call(run_input=run_input)

        # 4. Fetch the results from the dataset
        dataset_items = client.dataset(run.default_dataset_id).list_items().items

        if not dataset_items:
            print(f"[Error] Apify returned no data for {url}")
            return {}

        raw_data = dataset_items[0]

        print("[Collector] Data retrieved! Mapping to Sahayogi schema...")

        # 5. THE TRANSLATOR: Map Apify's deep Reel data to our clean schema.
        # This scraper has slightly different (and better) key names than the generic one.
        mapped_reel = {
            # Safely grab the ID, defaulting to unknown
            "reel_id": raw_data.get("id", raw_data.get("shortCode", "unknown_id")),
            "url": url,
            "creator": raw_data.get("ownerUsername", "unknown_creator"),
            "collection_time": datetime.now(timezone.utc).isoformat(),
            "source": "instagram",
            "metadata": {
                "posted_at": raw_data.get("timestamp", ""),
                # The Reel scraper outputs videoDuration directly
                "duration_seconds": raw_data.get("videoDuration", 0),

                # Views on Reels are technically "plays". We check both just in case.
                "views": raw_data.get("videoPlayCount", raw_data.get("playsCount", 0)),
                "likes": raw_data.get("likesCount", 0),
                "comments": raw_data.get("commentsCount", 0),

                "caption": raw_data.get("caption", ""),

                # Extract hashtags directly
                "hashtags": raw_data.get("hashtags", []),

                # Extracting deep audio metadata that the generic scraper often misses
                "audio_name": raw_data.get("musicInfo", {}).get("musicName", "Original/Unknown Audio"),
                "audio_original": raw_data.get("musicInfo", {}).get("isOriginalSound", True)
            }
        }

        print("[Collector] Successfully mapped live data!")
        return mapped_reel

    except Exception as e:
        print(f"[Error] The scraper failed: {str(e)}")
        return {}


# ==========================================
# ISOLATED TEST BLOCK
# ==========================================
if __name__ == "__main__":
    # Test it with a real URL!
    test_url = "https://www.instagram.com/reel/DZUooz3Tvio/?igsh=MWVrY2ZpandkdmE0MQ=="

    result = fetch_reel_metadata(test_url)

    if result:
        print("\n--- Live Scrape Output ---")
        print(json.dumps(result, indent=4))

        # Save it to prove it works
        base_dir = Path(__file__).resolve().parent.parent
        out_path = base_dir / "data" / "reels" / f"{result['reel_id']}.json"

        # Ensure directory exists
        out_path.parent.mkdir(parents=True, exist_ok=True)

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)
            print(f"\n[Success] Live reel saved to {out_path}")