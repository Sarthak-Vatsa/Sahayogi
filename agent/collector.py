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

    # 2a Configure the Scraper Input
    # Using 'directUrls' to target exactly one reel for our Stage 1 test
    # run_input = {
    #     "username": [url]  # Apify calls this 'username' even when you pass a direct reel URL
    # }

    # 2b Configure the Scraper Input for Profile + Filters
    # Instead of directUrls, we use 'username' (which accepts Profile URLs)
    # and add our time/pinned filters.
    run_input = {
        "username": [url],             # Accepts Profile URL or username
        "onlyPostsNewerThan": "5 days", # Only grab what's fresh
        "skipPinnedPosts": True         # Ensure we don't scrape old viral hits
    }

    print("[Collector] Contacting Apify servers using 'instagram-reel-scraper'...")

    try:
        # 3. Run the Dedicated Reel Scraper Actor
        run = client.actor("apify/instagram-reel-scraper").call(run_input=run_input)

        # 4. Fetch the results from the dataset
        # 4. Fetch the results from the dataset
        dataset_items = client.dataset(run.default_dataset_id).list_items().items

        if not dataset_items:
            print(f"[Warning] No reels found for {url} in the last 5 days.")
            return [] # Return an empty list instead of a dict

        print(f"[Collector] Found {len(dataset_items)} reels. Mapping all...")

        # 5. THE TRANSLATOR: Map the entire list of reels
        mapped_reels = []
        for raw_data in dataset_items:
            mapped_reel = {
                "reel_id": raw_data.get("id", raw_data.get("shortCode", "unknown_id")),
                "url": raw_data.get("url", url),
                "creator": raw_data.get("ownerUsername", "unknown_creator"),
                "collection_time": datetime.now(timezone.utc).isoformat(),
                "source": "instagram",
                "metadata": {
                    "posted_at": raw_data.get("timestamp", ""),
                    "duration_seconds": raw_data.get("videoDuration", 0),
                    "views": raw_data.get("videoPlayCount", raw_data.get("playsCount", 0)),
                    "likes": raw_data.get("likesCount", 0),
                    "comments": raw_data.get("commentsCount", 0),
                    "caption": raw_data.get("caption", ""),
                    "hashtags": raw_data.get("hashtags", []),
                    "audio_name": raw_data.get("musicInfo", {}).get("musicName", "Original Audio"),
                    "audio_original": raw_data.get("musicInfo", {}).get("isOriginalSound", True)
                }
            }
            mapped_reels.append(mapped_reel)

        return mapped_reels

    except Exception as e:
        print(f"[Error] The scraper failed: {str(e)}")
        return {}


# ==========================================
# ISOLATED TEST BLOCK
# ==========================================
if __name__ == "__main__":
    # Test it with a real URL!
    test_url = "https://www.instagram.com/kidscartoons_kc?igsh=d3kwOWE0bTdsOHow"

    results = fetch_reel_metadata(test_url)

    for result in results:
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