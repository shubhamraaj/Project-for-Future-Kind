import os
import json
import feedparser
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

# Define Category Keywords for Intelligent Routing
KEYWORDS = {
    "wildlife": ["tiger", "forest", "elephant", "leopard", "wildlife", "sanctuary", "cheetah", "conservation", "animal welfare"],
    "domestic": ["dog", "cat", "stray", "abc rule", "shelter", "rabies", "pet", "campus", "street dog"],
    "poultry": ["poultry", "chicken", "egg", "farmed", "slaughterhouse", "meat", "dairy", "livestock"]
}

def classify_article(title, snippet):
    text = (title + " " + snippet).lower()
    for cat, terms in KEYWORDS.items():
        if any(term in text for term in terms):
            return cat
    return "welfare"

def build_card_html(title, snippet, url, category, source="Google News Wire"):
    tag_colors = {
        "wildlife": "#059669",
        "domestic": "#0284c7",
        "poultry": "#b45309",
        "welfare": "#033666"
    }
    color = tag_colors.get(category, "#0284c7")
    
    return f"""
    <div class="card">
      <div class="card-tag" style="color: {color};">{category.upper()}</div>
      <h3 class="card-title">{title}</h3>
      <div style="font-size:0.85rem; color:#64748b; font-style:italic; margin-bottom:0.75rem;">Source: {source}</div>
      <p class="card-snippet">{snippet}</p>
      <a href="{url}" target="_blank" class="card-link">Read Full Article &rarr;</a>
    </div>
    """

def generate_rss_feed(articles, output_path="feed.xml"):
    """
    Generates an RSS 2.0 feed (feed.xml) from curated articles.
    """
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    # RSS Channel Header Information
    ET.SubElement(channel, "title").text = "Animal Chatter | Ecological & Wildlife News"
    ET.SubElement(channel, "link").text = "https://shubhamraaj.github.io/Project-for-Future-Kind/"
    ET.SubElement(channel, "description").text = "Daily curated updates on wildlife conservation, domestic animal welfare, and livestock policy."
    ET.SubElement(channel, "language").text = "en-us"
    ET.SubElement(channel, "lastBuildDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    # Add individual news items to RSS feed
    for item in articles:
        rss_item = ET.SubElement(channel, "item")
        
        ET.SubElement(rss_item, "title").text = item.get("title", "Untitled Update")
        ET.SubElement(rss_item, "link").text = item.get("url", "https://shubhamraaj.github.io/Project-for-Future-Kind/")
        ET.SubElement(rss_item, "description").text = item.get("snippet", "No description available.")
        
        category = item.get("category", "General")
        ET.SubElement(rss_item, "category").text = category
        
        ET.SubElement(rss_item, "pubDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
            
        guid = ET.SubElement(rss_item, "guid", isPermaLink="false")
        guid.text = item.get("url", item.get("title", ""))

    # Pretty format XML string
    rough_string = ET.tostring(rss, encoding="utf-8")
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    # Write feed.xml to disk
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
        
    print(f"📡 Successfully generated RSS feed at {output_path}!")

def main():
    # RSS Feeds to aggregate from
    feeds = [
        "https://news.google.com/rss/search?q=animal+welfare+india&hl=en-IN&gl=IN&ceid=IN:en",
        "https://news.google.com/rss/search?q=wildlife+conservation+india&hl=en-IN&gl=IN&ceid=IN:en",
        "https://news.google.com/rss/search?q=stray+dogs+india+policy&hl=en-IN&gl=IN&ceid=IN:en"
    ]

    all_articles = []
    welfare_cards = []
    insights_cards = []
    events_cards = []
    wildlife_cards = []
    domestic_cards = []
    poultry_cards = []

    for feed_url in feeds:
        parsed = feedparser.parse(feed_url)
        for entry in parsed.entries[:8]: # Limit per feed to keep pages clean
            title = entry.get('title', 'Untitled')
            url = entry.get('link', '#')
            raw_summary = entry.get('summary', 'Read more on original wire.')
            
            # Clean HTML tags from RSS summaries
            snippet = BeautifulSoup(raw_summary, "html.parser").get_text()
            if len(snippet) > 140:
                snippet = snippet[:137] + "..."
            
            category = classify_article(title, snippet)
            
            # Store for Lunr.js search index JSON and RSS feed
            all_articles.append({
                "title": title,
                "snippet": snippet,
                "url": url,
                "category": category
            })

            card_html = build_card_html(title, snippet, url, category)

            # Route into specific streams
            if category == "wildlife":
                wildlife_cards.append(card_html)
            elif category == "domestic":
                domestic_cards.append(card_html)
            elif category == "poultry":
                poultry_cards.append(card_html)
            else:
                welfare_cards.append(card_html)

    # Fallback default cards if feeds return empty
    if not welfare_cards:
        welfare_cards.append(build_card_html("New Municipal Guidelines Released for Community Animal Care", "Local urban bodies introduce standardized protocols for feeding and vaccination drives across regional sectors.", "#", "welfare"))
    if not insights_cards:
        insights_cards.append(build_card_html("Mapping Human-Wildlife Coexistence Corridors", "An institutional overview of ecological zoning and corridor preservation in forested districts.", "#", "insights", "Conservation Review"))
    if not events_cards:
        events_cards.append(build_card_html("National Campus Sustainability & Welfare Summit", "Join student environmental clubs and policy researchers for panel discussions on green campus infrastructure.", "#", "events", "Green Club"))

    # 1. Update index.html
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        
        containers = {
            "welfare-container": welfare_cards,
            "insights-container": insights_cards,
            "events-container": events_cards
        }

        for container_id, cards in containers.items():
            box = soup.find(id=container_id)
            if box:
                box.clear()
                for card in cards:
                    box.append(BeautifulSoup(card, "html.parser"))

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(str(soup))
        print("🚀 Successfully updated index.html!")

    # 2. Update Category Pages
    category_files = {
        "categories/wildlife.html": ("wildlife-news-grid", wildlife_cards),
        "categories/domestic.html": ("domestic-news-grid", domestic_cards),
        "categories/poultry.html": ("poultry-news-grid", poultry_cards)
    }

    for filepath, (container_id, cards) in category_files.items():
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
            
            grid = soup.find(id=container_id)
            if grid:
                grid.clear()
                if cards:
                    for card in cards:
                        grid.append(BeautifulSoup(card, "html.parser"))
                else:
                    grid.append(BeautifulSoup('<div class="card"><div class="card-tag">Stream</div><h3 class="card-title">No recent articles found in this stream.</h3><p class="card-snippet">Check back soon for automated updates.</p></div>', "html.parser"))

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(str(soup))
            print(f"🚀 Successfully updated {filepath}!")

    # 3. Export news-data.json for Lunr.js Search Engine
    with open("news-data.json", "w", encoding="utf-8") as f:
        json.dump(all_articles, f, indent=2)
    print(f"🔍 Successfully generated news-data.json with {len(all_articles)} searchable records!")

    # 4. Generate RSS feed.xml (NEW)
    generate_rss_feed(all_articles, "feed.xml")

if __name__ == "__main__":
    main()