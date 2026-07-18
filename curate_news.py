import os
import feedparser
from bs4 import BeautifulSoup

def fetch_latest_news():
    print("📡 Fetching external ecological news...")
    # Using the animal & wildlife news stream
    feed_url = "https://www.sciencedaily.com/rss/plants_animals/wildlife.xml"
    feed = feedparser.parse(feed_url)
    
    if not feed.entries:
        print("❌ No articles found.")
        return None
        
    # Get the latest article
    latest_item = feed.entries[0]
    
    # Clean the summary text (remove HTML tags if any)
    clean_summary = BeautifulSoup(latest_item.summary, "html.parser").get_text()
    
    # Keep it short and simple (first two sentences)
    short_summary = ". ".join(clean_summary.split(". ")[:2]) + "."

    article_data = {
        "title": latest_item.title,
        "link": latest_item.link,
        "summary": short_summary,
        "image": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=600&q=80" # Default elegant fallback
    }
    return article_data

def inject_into_website(article):
    if not article:
        return

    html_file = "index.html"
    if not os.path.exists(html_file):
        print("❌ index.html not found in this directory!")
        return

    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()

    # The exact marker matching the new ID tag inside your Welfare News page view
    target_marker = '<div id="automated-welfare-feed">'
    
    if target_marker not in content:
        print("❌ Error: Could not find '<div id=\"automated-welfare-feed\">' inside your index.html file!")
        return
    
    # Create the new HTML card layout matching your custom .article-deep-dive styles
    new_card_html = f"""
            <!-- Automated Animal Insight Card -->
            <div class="article-deep-dive" style="border-left: 5px solid var(--secondary); margin-top: 1.5rem;">
                <span class="card-tag">Latest Live Feed Update</span>
                <h2 style="font-size: 1.5rem; margin-bottom: 0.5rem;">{article['title']}</h2>
                <p style="color:var(--muted-text); font-style:italic; margin-bottom:1rem;">Live Curated Wire | ScienceDaily</p>
                <p>{article['summary']}</p>
                <a href="{article['link']}" target="_blank" style="display: inline-block; margin-top: 1rem; color: var(--primary); font-weight: 700; text-decoration: none;">Read Full Report →</a>
            </div>
    """

    # Insert the card right below the wrapper marker
    updated_content = content.replace(target_marker, target_marker + new_card_html)

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(updated_content)
        
    print(f"🚀 Successfully automated: Added '{article['title']}' to your Welfare News feed!")

if __name__ == "__main__":
    latest_article = fetch_latest_news()
    inject_into_website(latest_article)
