import os
import random
import feedparser
import urllib.parse
from bs4 import BeautifulSoup

def fetch_category_news(query_terms, target_count=50, label_name="Indian Network"):
    """Fetches articles for a specific query group across Google News & RSS feeds."""
    collected_articles = []
    seen_titles = set()

    for term in query_terms:
        if len(collected_articles) >= target_count:
            break

        encoded = urllib.parse.quote(term)
        rss_url = f"https://news.google.com/rss/search?q={encoded}&hl=en-IN&gl=IN&ceid=IN:en"

        try:
            feed = feedparser.parse(rss_url)
            if feed.entries:
                for item in feed.entries[:10]:
                    if len(collected_articles) >= target_count:
                        break

                    title = getattr(item, "title", "")
                    if not title or title in seen_titles:
                        continue

                    seen_titles.add(title)

                    raw_text = getattr(item, "summary", "") or getattr(item, "description", "")
                    clean_summary = BeautifulSoup(raw_text, "html.parser").get_text().strip() if raw_text else ""

                    if len(clean_summary) < 60:
                        clean_summary = "Detailed policy update and analytical coverage available on the source platform."

                    sentences = [s.strip() for s in clean_summary.split(". ") if s.strip()]
                    short_summary = ". ".join(sentences[:2]) + "." if sentences else "Click full report link to read analysis overview."

                    collected_articles.append({
                        "title": title,
                        "link": getattr(item, "link", "#"),
                        "summary": short_summary,
                        "source": label_name
                    })
        except Exception as e:
            print(f"⚠️ Channel issue for '{term}': {e}")
            continue

    return collected_articles


def update_html_container(content, container_id, articles, card_type="article"):
    """Replaces or injects card blocks into a specific container ID in index.html cleanly."""
    cards_html = []
    for article in articles:
        if card_type == "event":
            cards_html.append(f"""
                <div class="event-item" style="margin-bottom: 1.5rem;">
                    <div class="event-meta">COMMUNITY & POLICY EVENT &bull; LIVE WIRE</div>
                    <h3>{article['title']}</h3>
                    <p>{article['summary']}</p>
                    <a href="{article['link']}" target="_blank" style="display: inline-block; margin-top: 0.5rem; color: var(--primary); font-weight: 700; text-decoration: none;">View Event Details & Source →</a>
                </div>""")
        else:
            cards_html.append(f"""
                <div class="article-deep-dive" style="border-left: 5px solid var(--secondary); margin-top: 1.5rem;">
                    <span class="card-tag">India Update &bull; {article['source']}</span>
                    <h2 style="font-size: 1.5rem; margin-bottom: 0.5rem;">{article['title']}</h2>
                    <p style="color:var(--muted-text); font-style:italic; margin-bottom:1rem;">Live Curated Network</p>
                    <p>{article['summary']}</p>
                    <a href="{article['link']}" target="_blank" style="display: inline-block; margin-top: 1rem; color: var(--primary); font-weight: 700; text-decoration: none;">Read Full Report on Source Site →</a>
                </div>""")

    # Strictly form the full enclosed block
    full_block = f'<div id="{container_id}">\n' + "\n".join(cards_html) + "\n</div>"

    empty_tag = f'<div id="{container_id}"></div>'
    if empty_tag in content:
        return content.replace(empty_tag, full_block)

    start_tag = f'<div id="{container_id}">'
    if start_tag in content:
        start_idx = content.find(start_tag)
        end_idx = content.find('</div>', start_idx) + 6
        return content[:start_idx] + full_block + content[end_idx:]

    return content


def main():
    print("📡 Initializing Multi-Section Aggregator (Welfare, Insights, Events)...")

    # 1. Define query buckets
    welfare_queries = [
        "animal welfare policy India",
        "stray dog policy India",
        "wildlife rescue India",
        "forest department animal rescue",
        "prevention of cruelty to animals India",
        "animal birth control India"
    ]

    insights_queries = [
        "wildlife conservation research India",
        "biodiversity ecology study India",
        "elephant corridor research India",
        "marine conservation science India",
        "tiger population study India"
    ]

    events_queries = [
        "animal welfare conference India",
        "wildlife summit India",
        "conservation workshop India",
        "animal rights campaign event India"
    ]

    # 2. Collect content
    print("🔄 Fetching Welfare News...")
    welfare_articles = fetch_category_news(welfare_queries, target_count=50, label_name="Welfare Wire")

    print("🔄 Fetching Scientific Insights...")
    insights_articles = fetch_category_news(insights_queries, target_count=50, label_name="Ecology Research")

    print("🔄 Fetching Community Events...")
    events_articles = fetch_category_news(events_queries, target_count=20, label_name="Summits & Events")

    # 3. Read index.html
    html_file = "index.html"
    if not os.path.exists(html_file):
        print("❌ Error: index.html not found!")
        return

    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 4. Perform replacements
    content = update_html_container(content, "automated-welfare-feed", welfare_articles, card_type="article")
    content = update_html_container(content, "automated-insights-feed", insights_articles, card_type="article")
    content = update_html_container(content, "automated-events-feed", events_articles, card_type="event")

    # 5. Write back to index.html
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"🚀 Success! Injected Welfare ({len(welfare_articles)}), Insights ({len(insights_articles)}), and Events ({len(events_articles)}) into index.html cleanly.")


if __name__ == "__main__":
    main()