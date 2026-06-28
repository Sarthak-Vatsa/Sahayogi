import json
from pathlib import Path
from datetime import datetime

# ==========================================
# THE CORE FUNCTION
# ==========================================
def generate_markdown_report():
    print("[Reporter] Generating human-readable strategy document...")
    base_dir = Path(__file__).resolve().parent.parent

    # 1. Load the Trends Data
    trends_path = base_dir / "data" / "trends" / "weekly_trends.json"
    try:
        with open(trends_path, "r", encoding="utf-8") as f:
            trends_data = json.load(f)
    except FileNotFoundError:
        print("[Reporter] Error: Could not find weekly_trends.json")
        return

    # 2. Load the Strategy Data
    strategy_path = base_dir / "data" / "reports" / "weekly_strategy.json"
    try:
        with open(strategy_path, "r", encoding="utf-8") as f:
            strategy_data = json.load(f)
    except FileNotFoundError:
        print("[Reporter] Error: Could not find weekly_strategy.json")
        return

    # 3. Build the Markdown Content
    # We use f-strings (f"...") to inject the JSON variables into standard Markdown formatting
    date_str = datetime.now().strftime("%B %d, %Y")

    md_content = f"# Sahayogi Weekly Content Strategy\n"
    md_content += f"**Generated on:** {date_str}\n\n"

    md_content += f"## 🌟 Strategic Overview\n"
    md_content += f"{strategy_data.get('overview', '')}\n\n"
    md_content += f"---\n\n"

    md_content += f"## 📈 Market Trends Detected\n"
    md_content += f"*{trends_data.get('market_summary', 'Here are the key patterns across the niche this week.')}*\n\n"

    for i, trend in enumerate(trends_data.get('trends', []), 1):
        md_content += f"### {i}. {trend.get('trend_name')}\n"
        md_content += f"- **The Pattern:** {trend.get('pattern_description')}\n"
        md_content += f"- **Evidence:** {trend.get('evidence')}\n"
        md_content += f"- **Strategic Rule:** {trend.get('strategic_rule')}\n\n"

    md_content += f"---\n\n"

    md_content += f"## 🎬 Actionable Reel Concepts\n\n"
    for concept in strategy_data.get('concepts', []):
        md_content += f"### 💡 {concept.get('title')}\n"
        md_content += f"- **Starring:** {concept.get('recommended_character')}\n"
        md_content += f"- **Target Trend:** {concept.get('target_trend')}\n"
        md_content += f"- **Difficulty:** {concept.get('difficulty_score')}/10\n\n"
        md_content += f"**Visual Hook:**\n{concept.get('visual_hook')}\n\n"
        md_content += f"**Written Hook:**\n> \"{concept.get('written_hook')}\"\n\n"
        md_content += f"**Audio Strategy:**\n{concept.get('audio_strategy')}\n\n"
        md_content += f"**Why it works:**\n{concept.get('adaptation_reasoning')}\n\n"
        md_content += f"<br>\n\n"

    # 4. Save the Final Report
    # We use today's date in the filename so you keep an archive of all past reports
    file_name = f"Strategy_Report_{datetime.now().strftime('%Y-%m-%d')}.md"
    report_out_path = base_dir / "data" / "reports" / file_name

    with open(report_out_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"[Reporter] Success! Your weekly briefing is ready at: {report_out_path}")


# ==========================================
# ISOLATED TEST BLOCK
# ==========================================
if __name__ == "__main__":
    generate_markdown_report()