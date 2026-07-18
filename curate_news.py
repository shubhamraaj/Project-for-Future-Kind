import os
import random
import feedparser
from bs4 import BeautifulSoup

def fetch_latest_news():
    print("📡 Connecting to global animal news aggregation network...")
    
    # List of massive international news networks for broad animal insights
    sources = [
        {"name": "World Animal News", "url": "https://worldanimalnews.com/feed/"},
        {"name": "The Guardian (Animals)", "url": "https://www.theguardian.com/environment/animals/rss"},
        {"name": "World Animal Protection", "url": "https://www.worldanimalprotection.org/latest/news/feed"}
    ]
    
    # Shuffle the list so every check looks across different networks randomly!
    random.shuffle(sources)
    
    for source in sources:
        try:
            print(f"🔄 Attempting extraction from: {source['name']}")
            feed = feedparser.parse(source["url"])
            
            if feed.entries:
                latest_item = feed.entries[0]
                
                # Strip clean the text data out of summary containers
                summary_raw = getattr(latest_item, "summary", "")
                clean_summary = BeautifulSoup(summary_raw, "html.parser").get_text() if summary_raw else "No summary available."
                
                # Keep summary text sharp and distinct (first 2 sentences)
                sentences = [s.strip() for s in clean_summary.split(". ") if s.strip()]
                short_summary = ". ".join(sentences[:2]) + "." if sentences else "Click full report link to read analysis overview."
                
                print(f"✅ Success! Extracted headline: '{latest_item.title}' from {source['name']}")
                return {
                    "title": latest_item.title,
                    "link": latest_item.link,
                    "summary": short_summary,
                    "source": source["name"]
                }
        except Exception as e:
            print(f"⚠️ Channel {source['name']} connection dropped: {e}. Moving to alternative network...")
            continue
            
    print("❌ Critical: All global feeds returned empty responses.")
    return None

def inject_into_website(article):
    if not article:
        return

    html_file = "index.html"
    if not os.path.exists(html_file):
        print("❌ System Error: index.html not found in execution tree!")
        return

    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()

    target_marker = '<div id="automated-welfare-feed">'
    
    if target_marker not in content:
        print("❌ Integration Error: Missing '<div id=\"automated-welfare-feed\">' target.")
        return
    
    # Render customized card using your modern style guides
    new_card_html = f"""
            <!-- Automated Global News Wire Card -->
            <div class="article-deep-dive" style="border-left: 5px solid var(--secondary); margin-top: 1.5rem;">
                <span class="card-tag">Global Update &bull; {article['source']}</span>
                <h2 style="font-size: 1.5rem; margin-bottom: 0.5rem;">{article['title']}</h2>
                <p style="color:var(--muted-text); font-style:italic; margin-bottom:1rem;">Live Curated Wire</p>
                <p>{article['summary']}</p>
                <a href="{article['link']}" target="_blank" style="display: inline-block; margin-top: 1rem; color: var(--primary); font-weight: 700; text-decoration: none;">Read Full Report on Source Site →</a>
            </div>
    """

    # Update buffer layout contents
    updated_content = content.replace(target_marker, target_marker + new_card_html)

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(updated_content)
        
    print("🚀 Pipeline cycle completed successfully.")

if __name__ == "__main__":
    latest_article = fetch_latest_news()
    inject_into_website(latest_article)
