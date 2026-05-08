import feedparser
import json
import os
import time
import schedule
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Configure Google Generative AI
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    client = genai.Client(api_key=API_KEY)
else:
    client = None
    print("Warning: GEMINI_API_KEY not found in environment variables.")

# You can use Google News RSS or other tech/business news feeds
# For example, Google News for "technology startups"
RSS_FEED_URL = "https://news.google.com/rss/search?q=technology+startups+market+trends&hl=en-US&gl=US&ceid=US:en"

def fetch_latest_news(feed_url=RSS_FEED_URL, limit=10):
    """
    Fetches the latest news articles from the given RSS feed.
    """
    print(f"Fetching news from {feed_url}...")
    feed = feedparser.parse(feed_url)

    articles = []
    for entry in feed.entries[:limit]:
        article = {
            "title": entry.title,
            "link": entry.link,
            "published": entry.get("published", datetime.now().isoformat()),
            "summary": entry.get("summary", "")
        }
        articles.append(article)

    return articles

def analyze_market_trends(articles):
    """
    Uses Gemini API to analyze articles and extract problem statements and business ideas.
    """
    if not API_KEY:
        print("Cannot analyze market trends without API key.")
        return []

    print("Analyzing market trends using AI...")

    # Combine article titles and summaries into a single text prompt
    context = ""
    for article in articles:
        context += f"Title: {article['title']}\nSummary: {article['summary']}\n\n"

    prompt = f"""
    Based on the following recent news articles about technology, market trends, and startups:

    {context}

    Identify 3 distinct new problem statements or gaps in the market that these trends suggest.
    For each problem statement, provide a business analysis detailing:
    1. The problem statement.
    2. A potential business solution to this problem.
    3. The target market for the solution.
    4. A potential business model to monetize the solution.

    Return the result strictly as a valid JSON array of objects, where each object has the keys:
    "problem", "solution", "target_market", and "business_model".
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
        )

        # Clean up response to extract just the JSON
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]

        insights = json.loads(response_text.strip())
        return insights
    except Exception as e:
        print(f"Error during AI analysis: {e}")
        return []

def save_insights(insights, filename="market_insights.json"):
    """
    Saves the extracted insights to a JSON file.
    Appends the insights with a timestamp.
    """
    if not insights:
        print("No insights to save.")
        return

    data = []
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Could not read existing file: {e}")

    timestamp = datetime.now().isoformat()
    entry = {
        "timestamp": timestamp,
        "insights": insights
    }

    data.append(entry)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    print(f"Successfully saved {len(insights)} insights to {filename}")

def run_analysis_job():
    """
    Main job that fetches news, analyzes it, and saves insights.
    """
    print(f"\n--- Starting Market Analysis Job at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    news = fetch_latest_news(limit=10)
    print(f"Fetched {len(news)} articles.")

    if news:
        insights = analyze_market_trends(news)
        if insights:
            save_insights(insights)
    print("--- Job Complete ---\n")

if __name__ == "__main__":
    # Run once immediately
    run_analysis_job()

    # Schedule to run every 24 hours
    print("Scheduling job to run every 24 hours...")
    schedule.every(24).hours.do(run_analysis_job)

    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)
