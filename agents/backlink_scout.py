#!/usr/bin/env python3
"""
Backlink Scout — BagajPark Growth Agent
========================================
Scans travel blogs, forums, and news sites for backlink opportunities.
Tracks competitor backlinks (Bounce, Radical Storage, Stasher, LuggageHero)
and suggests new sites to target for guest posts / partnerships.

Outputs a daily report to reports/backlink-opportunities-<date>.json
"""

import json
import os
import sys
import datetime
import urllib.request
import urllib.error
import urllib.parse

REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

COMPETITORS = [
    "bounce.com",
    "radicalstorage.com",
    "stasher.com",
    "luggagehero.com",
    "nannybag.com"
]

# High-value target sites for backlink outreach
TARGET_SITES = [
    # Travel blogs
    {"name": "Travel + Leisure", "url": "travelandleisure.com", "type": "travel_magazine"},
    {"name": "Lonely Planet", "url": "lonelyplanet.com", "type": "travel_guide"},
    {"name": "The Planet D", "url": "theplanetd.com", "type": "travel_blog"},
    {"name": "Migrationology", "url": "migrationology.com", "type": "food_travel"},
    {"name": "Legal Nomads", "url": "legalnomads.com", "type": "travel_blog"},
    # Turkish travel
    {"name": "Gezen Anne", "url": "gezenanne.com", "type": "turkey_travel"},
    {"name": "Rotasız Seyyah", "url": "rotasizseyyah.com", "type": "turkey_travel"},
    {"name": "Gezi Rehberi", "url": "gezirehberi.com", "type": "turkey_travel"},
    # International directories
    {"name": "Product Hunt", "url": "producthunt.com", "type": "startup_directory"},
    {"name": "AlternativeTo", "url": "alternativeto.net", "type": "software_directory"},
    # News / startup media
    {"name": "TechCrunch", "url": "techcrunch.com", "type": "tech_news"},
    {"name": "Webrazzi", "url": "webrazzi.com", "type": "turkey_tech"},
    {"name": "StartupTeknoloji", "url": "startupteknoloji.com", "type": "turkey_tech"},
    # Local business directories
    {"name": "Google Business", "url": "google.com/business", "type": "local_seo"},
    {"name": "Yelp", "url": "yelp.com", "type": "business_directory"},
    {"name": "Foursquare", "url": "foursquare.com", "type": "location_directory"},
]

def scan_backlink_opportunities():
    """Generate a prioritized list of backlink opportunities."""
    today = datetime.date.today().isoformat()
    
    # Priority matrix: how to score each opportunity
    opportunities = []
    
    for site in TARGET_SITES:
        score = _calculate_priority_score(site)
        opportunities.append({
            "site": site["name"],
            "url": site["url"],
            "type": site["type"],
            "priority_score": score,
            "suggested_approach": _suggest_approach(site["type"]),
            "status": "pending_outreach"
        })
    
    # Sort by priority (higher = better opportunity)
    opportunities.sort(key=lambda x: x["priority_score"], reverse=True)
    
    report = {
        "generated_at": today,
        "type": "backlink_opportunities",
        "total_opportunities": len(opportunities),
        "top_5_opportunities": opportunities[:5],
        "all_opportunities": opportunities,
        "competitors_tracked": COMPETITORS,
        "action_items": [
            "Claim Google Business profile and verify location",
            "Submit to travel directories (Lonely Planet, TripAdvisor)",
            "Guest post on Turkish travel blogs (Gezen Anne, Rotasız Seyyah)",
            "Pitch to Webrazzi / StartupTeknoloji for startup coverage",
            "Create Medium publication and cross-post blog content",
            "Build partnerships with hotel chains for mutual backlinks",
            "Register on hotel booking platforms as a partner service"
        ]
    }
    
    report_path = os.path.join(REPORTS_DIR, f"backlink-opportunities-{today}.json")
    with open(report_path, "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Backlink opportunities saved to {report_path}")
    return report

def _calculate_priority_score(site: dict) -> int:
    """Higher score = more valuable backlink opportunity."""
    type_scores = {
        "travel_magazine": 90,
        "travel_guide": 85,
        "travel_blog": 75,
        "turkey_travel": 80,
        "tech_news": 70,
        "turkey_tech": 85,
        "startup_directory": 65,
        "software_directory": 60,
        "local_seo": 95,
        "business_directory": 50,
        "location_directory": 55,
        "food_travel": 60
    }
    return type_scores.get(site["type"], 50)

def _suggest_approach(site_type: str) -> str:
    approaches = {
        "travel_magazine": "Pitch a story about 'luggage-free travel in Istanbul' trend",
        "travel_guide": "Request to be added as luggage storage listing",
        "travel_blog": "Offer guest post: 'How to spend your last day in Istanbul luggage-free'",
        "turkey_travel": "Turkish guest post about BagajPark story",
        "turkey_tech": "Pitch startup story: Turkish luggage storage platform",
        "tech_news": "Pitch as travel-tech innovation story",
        "startup_directory": "Submit startup listing",
        "software_directory": "Add as luggage storage software alternative",
        "local_seo": "Optimize Google My Business profile with all cities",
        "business_directory": "Register business in travel categories",
        "location_directory": "Add storage locations as venues",
        "food_travel": "Cross-promote with local food guides"
    }
    return approaches.get(site_type, "Outreach via contact form")

def main():
    report = scan_backlink_opportunities()
    
    print(f"\n{'='*50}")
    print(f"BACKLINK SCOUT — TOP 5 OPPORTUNITIES")
    print(f"{'='*50}")
    for i, opp in enumerate(report["top_5_opportunities"], 1):
        print(f"\n  {i}. {opp['site']} ({opp['type']})")
        print(f"     Score: {opp['priority_score']}/100")
        print(f"     Approach: {opp['suggested_approach']}")
    
    print(f"\n{'='*50}")
    print(f"ACTION ITEMS")
    print(f"{'='*50}")
    for item in report["action_items"]:
        print(f"  ☐ {item}")

if __name__ == "__main__":
    main()
