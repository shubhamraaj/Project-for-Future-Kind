import os
import feedparser
from bs4 import BeautifulSoup

def fetch_latest_news():
    print("📡 Fetching external ecological news...")
    # Example: Using an environmental news RSS feed
    # You can replace this URL with any news portal's RSS feed link
    feed_url = "https://www.sciencedaily.com/rss/earth_climate/environmental_science.xml"
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

    # Define the exact marker in your HTML where new cards should live
    target_marker = '<div class="news-grid">'
    
    # Create the new HTML card layout with the source link button
    new_card_html = f"""
            <!-- Automated Curated Card -->
            <article class="card">
                <div class="card-img" style="background-image: url('{article['image']}');"></div>
                <div class="card-content">
                    <span class="card-tag">Curated Insights</span>
                    <h4 class="card-title">{article['title']}</h4>
                    <p class="card-text">{article['summary']}</p>
                    <a href="{article['link']}" target="_blank" class="btn" style="background:var(--secondary);">Visit Original Source</a>
                </div>
            </article>
    """

    # Insert the card right below the grid opening tag
    updated_content = content.replace(target_marker, target_marker + new_card_html)

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(updated_content)
        
    print(f"🚀 Successfully automated: Added '{article['title']}' to your homepage grid!")

if __name__ == "__main__":
    latest_article = fetch_latest_news()
    inject_into_website(latest_article)