# 🐾 Animal Chatter — Ecological & Animal Welfare Journalism Hub

> An automated news aggregation and policy tracking portal monitoring wildlife conservation, domestic animal welfare (ABC rules), and farmed animal regulations across India.

🌐 **Live Website:** [shubhamraaj.github.io/Project-for-Future-Kind](https://shubhamraaj.github.io/Project-for-Future-Kind/)

---

## 📌 Overview

**Animal Chatter** bridges the gap between grassroots animal welfare, institutional policy shifts, and ecological journalism. The platform aggregates curated news, tracks regulatory updates (such as Supreme Court directives and local municipality guidelines), and provides an instant client-side search archive.

### Key Features
* 🌓 **Universal Dark/Light Mode:** Seamless theme switching with persistent state across all pages via `localStorage`.
* ⚡ **Client-Side Real-Time Search:** Instant indexing and full-text search powered by `Lunr.js` across thousands of news records without requiring a heavy server backend.
* 🤖 **Automated News Scraping:** Python-driven aggregation pipeline that fetches, cleans, and structures regional and national news streams into structured JSON/HTML feeds.
* 📩 **Seamless Contact & Subscriptions:** Serverless form submissions powered by `Web3Forms`.
* 📱 **Fully Responsive Layout:** Clean, accessible design optimized for modern desktop and mobile browsers.

---

## 🛠️ Tech Stack

| Domain | Technologies Used |
| :--- | :--- |
| **Frontend** | HTML5, CSS3 (CSS Variables, Flexbox, CSS Grid), Vanilla JavaScript (ES6+) |
| **Search Engine** | [Lunr.js](https://lunrjs.com/) (Browser-based inverted search index) |
| **Backend & Scraping** | Python 3, `requests`, `BeautifulSoup4` |
| **Automation & CI/CD** | GitHub Actions (Daily automated scraper workflows) |
| **Form Handling** | Web3Forms API |
| **Hosting & Deployment**| GitHub Pages |

---

## 📂 Project Structure

```text
Project-for-Future-Kind/
├── .github/
│   └── workflows/          # GitHub Actions CI/CD workflows
├── categories/             # Stream category pages
│   ├── wildlife.html       # Wildlife & Forest Conservation
│   ├── domestic.html       # Domestic & Campus Animal Welfare
│   └── poultry.html        # Farmed Animals & Livestock Policy
├── 404.html                # Custom 404 Error page
├── about.html              # Mission, editorial goals & team overview
├── contact.html            # Web3Forms powered contact interface
├── curate_news.py          # Python web scraper & data curator
├── index.html              # Main news aggregator portal
├── news-data.json          # Formatted JSON store for client search
├── robots.txt              # Search engine crawler directives
├── search.html             # Real-time search UI using Lunr.js
└── sitemap.xml             # XML sitemap for Google indexing
