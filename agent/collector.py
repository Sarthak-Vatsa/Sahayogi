import json
from pathlib import Path

def fetch_reel_metadata(url: str) -> dict:
    """
    Simulates scraping an Instagram reel by loading local dummy data.

    Args:
        url (str): The Instagram Reel URL.

    Returns:
        dict: A dictionary containing the Basic Info and Metadata of the reel.
    """
    print(f"[Collector] Initializing scrape for URL: {url}")

    # pathlib helps us safely build file paths regardless of Mac or Windows
    # __file__ refers to collector.py. We go up one level (parent) to 'sahayogi', then into 'data/reels'
    base_dir = Path(__file__).resolve().parent.parent
    dummy_file_path = base_dir / "data" / "reels" / "dummy_reel_001.json"

    print(f"[Collector] Simulating web request... Loading local data instead.")

    try:
        with open(dummy_file_path, "r", encoding="utf-8") as file:
            reel_data = json.load(file)
            print("[Collector] Successfully retrieved metadata!")
            return reel_data

    except FileNotFoundError:
        print(f"[Error] Could not find dummy data at {dummy_file_path}")
        return {}
    except json.JSONDecodeError:
        print("[Error] The dummy data file contains invalid JSON.")
        return {}

if __name__ == "__main__":
    # This block only runs if you execute this specific file directly.
    # It will NOT run when main.py imports this module later.

    test_url = "https://instagram.com/reel/dummy123"
    result = fetch_reel_metadata(test_url)

    print("\n--- Test Output ---")
    # json.dumps with indent=4 prints the dictionary in a highly readable, formatted way
    print(json.dumps(result, indent=4))

# later, when we fetch actual data and map it to our reel_schema, we can replace the above function with the following:

# def fetch_reel_metadata(url: str) -> dict:
#     # 1. Make the live network request to Instagram
#     raw_response = instagram_scraper.get_reel(url)
#
#     # 2. CONVERSION STEP: Map the messy live data to our strict schema
#     mapped_data = {
#         "reel_id": raw_response.media_id,
#         "url": url,
#         "creator": raw_response.owner_username,
#         "collection_time": get_current_timestamp(),
#         "source": "instagram",
#         "metadata": {
#             "posted_at": raw_response.date_utc.isoformat(),
#             "duration_seconds": raw_response.video_duration,
#             "views": raw_response.view_count,
#             "likes": raw_response.like_count,
#             "comments": raw_response.comment_count,
#             "caption": raw_response.caption,
#             "hashtags": extract_hashtags(raw_response.caption),
#             "audio_name": raw_response.audio_title,
#             "audio_original": raw_response.is_video_original_sound
#         }
#     }
#    return mapped_data