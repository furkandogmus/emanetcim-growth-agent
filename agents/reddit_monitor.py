#!/usr/bin/env python3
"""
Reddit Monitor — BagajPark Growth Agent

Searches for unanswered luggage storage questions on Reddit.
Output: reports/reddit/{date}.md
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports" / "reddit"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

TARGETS = [
    # (city, keyword)
    ("Istanbul", "luggage storage"),
    ("Istanbul", "store my luggage"),
    ("Istanbul", "leave my bags"),
    ("Ankara", "luggage storage"),
    ("Izmir", "luggage storage"),
    ("Antalya", "luggage storage"),
    ("Turkey", "luggage storage"),
    ("Türkiye", "valiz emanet"),
    ("Istanbul", "bag drop"),
    ("Istanbul", "saklama"),
]

EXCLUDE = ["politics", "worldnews", "news", "TurkeyMeta"]


def find_reddit_posts(city, keyword, limit=5):
    """Search Google for Reddit posts about luggage storage in a city."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml",
    }

    query = f'site:reddit.com "{city}" "{keyword}"'
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return [], str(e)

    posts = []
    # Extract Reddit post URLs from search results
    for match in re.finditer(
        r'<a\s+href="/url\?q=(https?://(?:www\.)?reddit\.com/r/[^/]+/comments/[^"&]+)[^"]*"',
        html
    ):
        url = urllib.parse.unquote(match.group(1))
        if any(ex in url.lower() for ex in EXCLUDE):
            continue
        posts.append(url)
        if len(posts) >= limit:
            break

    return posts, None


def get_post_title(post_url):
    """Fetch a Reddit post page and extract its title."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    try:
        req = urllib.request.Request(post_url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as r:
            html = r.read().decode("utf-8", errors="replace")
        m = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
        if m:
            return m.group(1).replace(" - Reddit", "").strip()
    except Exception:
        pass
    return ""


def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    all_posts = []
    seen = set()
    errors = []

    for city, keyword in TARGETS:
        posts, err = find_reddit_posts(city, keyword)
        if err:
            errors.append(f"{city}/{keyword}: {err}")
        for url in posts:
            if url not in seen:
                seen.add(url)
                title = get_post_title(url)
                all_posts.append({"title": title or "(no title)", "url": url, "city": city, "keyword": keyword})

    lines = [
        f"# Reddit Monitor — {today}\n",
    ]

    if all_posts:
        lines.append(f"## 🔍 Found {len(all_posts)} relevant posts\n")
        for i, post in enumerate(all_posts[:15], 1):
            lines.append(f"{i}. **{post['title']}**")
            lines.append(f"   📍 {post['city']} | 🏷️ `{post['keyword']}`")
            lines.append(f"   🔗 {post['url']}")
            lines.append("")
    else:
        lines.append("## 🔍 No new relevant posts found today\n")
        lines.append("_Try expanding search scope or check manually at reddit.com/r/travel_\n")

    if errors:
        lines.append("### ⚠️ Errors")
        for e in errors[:5]:
            lines.append(f"- {e}")

    lines.append("---")
    lines.append("_Next scan: tomorrow 07:30 TRT_")

    report = "\n".join(lines)
    print(report)

    report_path = REPORTS_DIR / f"{today}.md"
    with open(report_path, "w") as f:
        f.write(report)

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
