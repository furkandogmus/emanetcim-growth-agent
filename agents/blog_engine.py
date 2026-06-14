#!/usr/bin/env python3
"""
Blog Content Engine — BagajPark Growth Agent

Generates 3 blog post ideas + SEO keyword competition check.
Uses search results to estimate competition levels.

Output: reports/blog/{date}.md
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

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports" / "blog"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def count_search_results(keyword):
    """Estimate competition by scraping result count from Google."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    }
    url = f"https://www.google.com/search?q={urllib.parse.quote(keyword)}"

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as r:
            html = r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return None, str(e)

    patterns = [
        r'About ([\d,]+) results',
        r'Aşağıda yaklaşık ([\d.]+) sonuç',
        r'Yaklaşık ([\d.]+) sonuç bulundu',
    ]

    for pattern in patterns:
        m = re.search(pattern, html)
        if m:
            count_str = m.group(1).replace(",", "").replace(".", "")
            try:
                return int(count_str), None
            except ValueError:
                pass

    return None, "Could not parse result count"


def count_competitors_on_first_page(keyword):
    """Rough check: how many competitors rank for this keyword."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36",
    }
    url = f"https://www.google.com/search?q={urllib.parse.quote(keyword)}"

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as r:
            html = r.read().decode("utf-8", errors="replace")
    except Exception:
        return None

    # Check for competitor domains
    competitors = ["bounce", "stasher", "nannybag", "luggagehero", "radicalstorage",
                   "company", "bagajpark", "emin", "emanet"]
    found = []
    for comp in competitors:
        if comp in html.lower():
            found.append(comp)

    return found


def generate_blog_ideas(month=None):
    """Generate 3 blog post ideas based on season."""
    if month is None:
        now = datetime.now(timezone.utc)
        month = now.month

    if 5 <= month <= 9:
        season_label = "Yaz / Summer"
        season_angle = "peak travel season, airport crowds, hotel check-out times"
    elif month in [10, 11]:
        season_label = "Sonbahar / Fall"
        season_angle = "shoulder season, city breaks"
    else:
        season_label = "Kış / Winter"
        season_angle = "ski trips, indoor activities"

    ideas = [
        {
            "title_tr": "İstanbul'da Valiz Emanet: 2026 Rehberi — Nerede, Kaç TL, Güvenli mi?",
            "title_en": "Luggage Storage in Istanbul: 2026 Guide — Where, How Much, Is It Safe?",
            "keyword": "luggage storage istanbul",
            "angle": f"Travelers arriving in Istanbul during {season_label} need to store bags before/after hotel check-in.",
            "type": "guide",
            "link": "https://bagajpark.com/en/blog/luggage-storage-istanbul",
        },
        {
            "title_tr": "En İyi Valiz Emanet Uygulamaları 2026: Karşılaştırma ve İnceleme",
            "title_en": "Best Luggage Storage Apps 2026: Comparison & Review",
            "keyword": "best luggage storage apps",
            "angle": "Comparison of Bounce, Stasher, Radical Storage, and BagajPark — features, pricing, coverage.",
            "type": "comparison",
            "link": "https://bagajpark.com/en/blog/best-luggage-storage-apps",
        },
        {
            "title_tr": f"{season_label} Tatilinde Bavul Derdi: Check-Out ile Uçuş Arasında Ne Yapmalı?",
            "title_en": f"No Bag Worries During {season_label} Travel: What to Do Between Check-Out and Your Flight?",
            "keyword": "luggage storage between checkout and flight",
            "angle": f"Common traveler pain point: {season_angle}. Solution: book luggage storage.",
            "type": "solution",
            "link": "https://bagajpark.com/en/blog/luggage-storage-between-checkout-and-flight",
        },
    ]

    return ideas, season_label


def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    ideas, season = generate_blog_ideas()

    lines = [
        f"# Blog Content Engine — {today}",
        f"_Season: {season}_\n",
    ]

    # --- Competition Check ---
    lines.append("---")
    lines.append("## 🔍 SEO Keyword Competition Check\n")

    count = None
    for idea in ideas:
        kw = idea["keyword"]
        count, err = count_search_results(kw)
        competitors = count_competitors_on_first_page(kw)

        if count is not None:
            if count < 200_000:
                level = "🟢 Very Low"
            elif count < 1_000_000:
                level = "🟢 Low"
            elif count < 5_000_000:
                level = "🟡 Medium"
            else:
                level = "🔴 High"

            lines.append(f"### `{kw}`")
            lines.append(f"- **Search volume:** ~{count:,} results — **{level} competition**")
            if competitors:
                lines.append(f"- **Competitors on page 1:** {', '.join(set(competitors))}")
            else:
                lines.append(f"- **Competitors on page 1:** None detected")
            lines.append(f"- **Strategy:** {'Easy to rank with good content' if count < 500_000 else 'Medium competition, focus on long-tail'}")
            lines.append("")
        else:
            lines.append(f"### `{kw}`")
            lines.append(f"- ⚠️ Could not check (will work on GitHub Actions)")
            lines.append("")

    # --- Blog Ideas ---
    lines.append("---")
    lines.append("## 📝 Suggested Blog Posts\n")

    for i, idea in enumerate(ideas, 1):
        lines.append(f"### {i}. {idea['title_en']}")
        lines.append(f"**🇹🇷 {idea['title_tr']}**\n")
        lines.append(f"**Angle:** {idea['angle']}")
        lines.append(f"**Target keyword:** `{idea['keyword']}`")
        lines.append(f"**Type:** {idea['type']}")
        lines.append(f"**Suggested URL:** {idea['link']}")
        lines.append("")

    lines.append("---")
    lines.append("_Next scan: tomorrow 07:30 TRT_")

    report = "\n".join(lines)
    print(report)

    report_path = REPORTS_DIR / f"{today}.md"
    with open(report_path, "w") as f:
        f.write(report)

    return 0 if count is not None else 1


if __name__ == "__main__":
    sys.exit(main())
