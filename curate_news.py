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
    
    # 2. Search Queries accessing hundreds of Indian Outlets via Google News Wire
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

def fetch_all_news(target_count=50):
    """Collects up to target_count articles from across all feeds."""
    print(f"📡 Connecting to Indian Animal Welfare Network (Fetching up to {target_count} articles)...")
    sources = generate_expanded_indian_sources()
    
    collected_articles = []
    seen_titles = set()

    for source in sources:
        if len(collected_articles) >= target_count:
            break

        try:
            print(f"🔄 Scanning: {source['name']}")
            feed = feedparser.parse(source["url"])
            
            if feed.entries:
                # Take up to 10 entries per feed source
                for item in feed.entries[:10]:
                    if len(collected_articles) >= target_count:
                        break

                    title = item.title if hasattr(item, "title") else ""
                    if not title or title in seen_titles:
                        continue

                    seen_titles.add(title)

                    raw_text = ""
                    if hasattr(item, "summary") and item.summary:
                        raw_text = item.summary
                    elif hasattr(item, "description") and item.description:
                        raw_text = item.description
                    elif hasattr(item, "content") and item.content:
                        raw_text = item.content[0].value

                    clean_summary = BeautifulSoup(raw_text, "html.parser").get_text().strip() if raw_text else ""
                    
                    if len(clean_summary) < 80:
                        clean_summary = "Breaking updates and policy insights regarding animal welfare and ecological protection in India. Read the complete publication directly on the source site."

                    sentences = [s.strip() for s in clean_summary.split(". ") if s.strip()]
                    short_summary = ". ".join(sentences[:2]) + "." if sentences else "Click full report link to read analysis overview."

                    collected_articles.append({
                        "title": title,
                        "link": item.link if hasattr(item, "link") else "#",
                        "summary": short_summary,
                        "source": source["name"]
                    })
        except Exception as e:
            print(f"⚠️ Channel {source['name']} issue: {e}")
            continue

    print(f"✅ Successfully collected {len(collected_articles)} articles!")
    return collected_articles

def inject_into_website(articles):
    if not articles:
        print("❌ No articles fetched to inject.")
        return

    html_file = "index.html"
    if not os.path.exists(html_file):
        print("❌ System Error: index.html not found!")
        return

    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()

    target_marker = '<div id="automated-welfare-feed"></div>'
    if target_marker not in content:
        # Fallback search if div isn't empty
        target_marker = '<div id="automated-welfare-feed">'
        if target_marker not in content:
            print("❌ Integration Error: Missing '<div id=\"automated-welfare-feed\">' target.")
            return

    # Build HTML blocks for ALL fetched articles
    cards_html_list = []
    for article in articles:
        cards_html_list.append(f"""
            <div class="article-deep-dive" style="border-left: 5px solid var(--secondary); margin-top: 1.5rem;">
                <span class="card-tag">India Update &bull; {article['source']}</span>
                <h2 style="font-size: 1.5rem; margin-bottom: 0.5rem;">{article['title']}</h2>
                <p style="color:var(--muted-text); font-style:italic; margin-bottom:1rem;">Live Curated India Network</p>
                <p>{article['summary']}</p>
                <a href="{article['link']}" target="_blank" style="display: inline-block; margin-top: 1rem; color: var(--primary); font-weight: 700; text-decoration: none;">Read Full Report on Source Site →</a>
            </div>""")

    all_cards_html = f'<div id="automated-welfare-feed">\n' + "\n".join(cards_html_list) + "\n</div>"

    # Replace the target div container with all the generated cards
    if '<div id="automated-welfare-feed"></div>' in content:
        updated_content = content.replace('<div id="automated-welfare-feed"></div>', all_cards_html)
    else:
        # Replace existing div and any previous cards inside it cleanly
        start_idx = content.find('<div id="automated-welfare-feed">')
        # Find closing tag after target div
        end_marker = '</div>'
        # Perform replacement safely
        updated_content = content.replace(target_marker, target_marker + "\n".join(cards_html_list))

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(updated_content)
        
    print(f"🚀 Injected {len(articles)} cards into index.html successfully.")

if __name__ == "__main__":
    # Change 50 to 100 or 200 if you want even more articles on the page!
    articles = fetch_all_news(target_count=50)
    inject_into_website(articles)