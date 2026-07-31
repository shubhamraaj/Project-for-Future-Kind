import os
import random
import feedparser
import urllib.parse
from bs4 import BeautifulSoup

def generate_expanded_indian_sources():
    # 1. Direct High-Priority Indian Animal Welfare & Conservation Feeds
    direct_sources = [
        {"name": "The Better India (Animal Welfare)", "url": "https://thebetterindia.com/animal-welfare/feed/"},
        {"name": "World Animal Protection India", "url": "https://www.worldanimalprotection.org.in/rss.xml"},
        {"name": "Wildlife Trust of India (WTI)", "url": "https://www.wti.org.in/feed/"},
        {"name": "Mongabay India (Wildlife & Ecology)", "url": "https://india.mongabay.com/feed/"},
        {"name": "Down To Earth (Forests & Wildlife)", "url": "https://www.downtoearth.org.in/rss/forests-and-wildlife"},
        {"name": "Sanctuary Asia", "url": "https://www.sanctuarynaturefoundation.org/feed"},
        {"name": "PETA India Wire", "url": "https://www.petaindia.com/feed/"},
        {"name": "Nature inFocus (India Wildlife)", "url": "https://www.natureinfocus.in/feed"},
        {"name": "WCS India (Wildlife Conservation)", "url": "https://india.wcs.org/Newsroom/Blog/rss"},
        {"name": "PIB Environment Ministry (MoEFCC)", "url": "https://pib.gov.in/RssMain.aspx?ModId=6"}
    ]
    
    # 2. Dynamic Search Queries tapping into 1,000+ Indian Media Outlets via Google News Wire
    search_terms = [
        "animal welfare India",
        "stray dog policy India",
        "wildlife rescue India",
        "elephant corridor India",
        "tiger conservation India",
        "forest department animal rescue",
        "animal birth control India",
        "prevention of cruelty to animals India",
        "cattle sanctuary India",
        "marine conservation India"
    ]
    
    google_wire_sources = []
    for term in search_terms:
        encoded = urllib.parse.quote(term)
        google_wire_sources.append({
            "name": f"Indian News Wire ({term.title()})",
            "url": f"https://news.google.com/rss/search?q={encoded}&hl=en-IN&gl=IN&ceid=IN:en"
        })
        
    all_sources = direct_sources + google_wire_sources
    random.shuffle(all_sources)
    return all_sources

def fetch_latest_news():
    print("📡 Connecting to expanded Indian Animal Welfare & Policy network (1000+ Outlets)...")
    sources = generate_expanded_indian_sources()
    
    for source in sources:
        try:
            print(f"🔄 Attempting extraction from: {source['name']}")
            feed = feedparser.parse(source["url"])
            
            if feed.entries:
                # Select a random entry from top 3 to keep content varied
                latest_item = random.choice(feed.entries[:3]) if len(feed.entries) >= 3 else feed.entries[0]
                
                raw_text = ""
                if hasattr(latest_item, "summary") and latest_item.summary:
                    raw_text = latest_item.summary
                elif hasattr(latest_item, "description") and latest_item.description:
                    raw_text = latest_item.description
                elif hasattr(latest_item, "content") and latest_item.content:
                    raw_text = latest_item.content[0].value
                
                clean_summary = BeautifulSoup(raw_text, "html.parser").get_text().strip() if raw_text else ""
                
                # Smart fallback for short/truncated descriptions
                if len(clean_summary) < 80:
                    clean_summary = "Breaking updates and policy insights regarding animal welfare and ecological protection in India. Read the complete publication directly on the source site."
                
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
            print(f"⚠️ Channel {source['name']} connection dropped: {e}. Moving to alternative Indian network...")
            continue
            
    print("❌ Critical: All feeds returned empty responses.")
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
    
    new_card_html = f"""
            <!-- Automated Indian Animal Welfare Card -->
            <div class="article-deep-dive" style="border-left: 5px solid var(--secondary); margin-top: 1.5rem;">
                <span class="card-tag">India Update &bull; {article['source']}</span>
                <h2 style="font-size: 1.5rem; margin-bottom: 0.5rem;">{article['title']}</h2>
                <p style="color:var(--muted-text); font-style:italic; margin-bottom:1rem;">Live Curated India Network</p>
                <p>{article['summary']}</p>
                <a href="{article['link']}" target="_blank" style="display: inline-block; margin-top: 1rem; color: var(--primary); font-weight: 700; text-decoration: none;">Read Full Report on Source Site →</a>
            </div>
    """

    updated_content = content.replace(target_marker, target_marker + new_card_html)

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(updated_content)
        
    print("🚀 Pipeline cycle completed successfully.")

if __name__ == "__main__":
    latest_article = fetch_latest_news()
    inject_into_website(latest_article)