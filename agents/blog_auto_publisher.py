#!/usr/bin/env python3
"""
Blog Auto-Publisher — BagajPark Growth Agent
=============================================
Reads competitor trends and keyword research, generates new blog post
suggestions with SEO-optimized content. Outputs can be used to create
new entries in blog-initializer.ts for the main site.

Outputs to reports/blog-ideas-<date>.md
"""

import json
import os
import sys
import datetime

REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

# Blog post ideas organized by keyword strategy
BLOG_IDEAS = {
    "tr": [
        {
            "slug": "check-out-sonrasi-istanbul-rehberi",
            "title": "Check-Out Sonrası İstanbul'da Ne Yapılır? Bavulsuz Gezme Rehberi",
            "excerpt": "Otelinizden çıkış yaptınız ama uçağınıza daha saatler var. İşte İstanbul'da check-out sonrası valiz derdi olmadan gezebileceğiniz 5 harika rota.",
            "keywords": ["check-out sonrası İstanbul", "bavulsuz gezme", "otel çıkışı aktiviteleri"]
        },
        {
            "slug": "antalya-plaj-ucus-arasinda-bagaj",
            "title": "Antalya'da Son Gün: Plaj ile Uçuş Arasında Valizleri Nereye Bırakmalı?",
            "excerpt": "Antalya tatilinin son gününde otelden çıkıp uçağa binene kadar geçen süreyi en iyi şekilde değerlendirmenin püf noktaları.",
            "keywords": ["Antalya son gün", "plaj valiz emanet", "check-out Antalya"]
        },
        {
            "slug": "kapadokya-balon-oncesi-bagaj",
            "title": "Kapadokya'da Balon Turu Öncesi Valiz Depolama Rehberi",
            "excerpt": "Sıcak hava balonu deneyimi öncesi valizlerinizi nereye bırakacağınızı mı düşünüyorsunuz? İşte Kapadokya'da bagaj depolama için en pratik çözümler.",
            "keywords": ["Kapadokya balon turu", "Göreme valiz emanet", "Kapadokya bagaj"]
        },
        {
            "slug": "istanbul-havalimani-emanet-ucretleri-2026",
            "title": "2026 İstanbul Havalimanı Emanet Ücretleri ve Alternatif Çözümler",
            "excerpt": "İstanbul Havalimanı (IST) ve Sabiha Gökçen (SAW) 2026 bagaj emanet fiyatları. Havalimanı emanetine alternatif daha ucuz şehir merkezi çözümleri.",
            "keywords": ["İstanbul Havalimanı emanet ücreti 2026", "IST bagaj emanet fiyat"]
        },
        {
            "slug": "ingiltere-turkiye-valiz-emanet",
            "title": "İngiltere'den Türkiye'ye Seyahat: Valiz Emanet ve Depolama Rehberi",
            "excerpt": "İngiltere'den Türkiye'ye seyahat edenler için kapsamlı valiz emanet rehberi. Londra, Manchester ve İstanbul'da bagaj depolama ipuçları.",
            "keywords": ["İngiltere Türkiye seyahat", "Londra valiz emanet"]
        }
    ],
    "en": [
        {
            "slug": "istanbul-last-day-without-luggage",
            "title": "Istanbul Last Day Guide: How to Explore Luggage-Free After Check-Out",
            "excerpt": "Checked out of your hotel but your flight is hours away? Here are 5 amazing Istanbul itineraries you can enjoy without dragging your suitcase around.",
            "keywords": ["Istanbul last day", "luggage-free travel", "hotel checkout tips"]
        },
        {
            "slug": "antalya-between-beach-and-flight",
            "title": "Antalya Last Day: Where to Store Luggage Between Beach and Flight",
            "excerpt": "Make the most of your final day in Antalya. Tips on enjoying the beach and exploring the Old Town before heading to the airport.",
            "keywords": ["Antalya last day luggage", "beach bag storage", "Antalya checkout"]
        },
        {
            "slug": "cappadocia-balloon-luggage-storage",
            "title": "Cappadocia Balloon Tour Luggage Storage Guide",
            "excerpt": "Planning a hot air balloon ride in Cappadocia? Here's where to store your bags while you float above the fairy chimneys.",
            "keywords": ["Cappadocia balloon luggage", "Goreme bag storage"]
        },
        {
            "slug": "istanbul-airport-luggage-storage-prices-2026",
            "title": "Istanbul Airport Luggage Storage Prices 2026 and Cheaper Alternatives",
            "excerpt": "Complete guide to IST and SAW airport left luggage prices for 2026, plus money-saving city center alternatives.",
            "keywords": ["Istanbul Airport luggage price 2026", "IST left luggage cost"]
        },
        {
            "slug": "uk-to-turkey-luggage-guide",
            "title": "UK to Turkey Travel: Complete Luggage Storage Guide",
            "excerpt": "Traveling from the UK to Turkey? Comprehensive guide to luggage storage in London, Manchester, Istanbul, and beyond.",
            "keywords": ["UK to Turkey luggage", "London bag storage"]
        }
    ]
}

def generate_blog_recommendations():
    """Generate blog post recommendations with SEO analysis."""
    today = datetime.date.today().isoformat()
    
    report = {
        "generated_at": today,
        "type": "blog_recommendations",
        "total_ideas": sum(len(ideas) for ideas in BLOG_IDEAS.values()),
        "languages": {}
    }
    
    for lang, ideas in BLOG_IDEAS.items():
        lang_data = []
        for idea in ideas:
            lang_data.append({
                "slug": idea["slug"],
                "title": idea["title"],
                "excerpt": idea["excerpt"],
                "keywords": idea["keywords"],
                "priority": _calculate_blog_priority(idea["keywords"])
            })
        report["languages"][lang] = lang_data
    
    # Save as markdown for easy reading
    md_lines = [
        f"# BagajPark Blog Ideas — {today}\n",
        f"_Auto-generated by Blog Auto-Publisher_",
        f"Total ideas: {report['total_ideas']}\n",
        f"## Priority Legend",
        f"- 🔴 **High Priority**: Low competition keyword, high search volume",
        f"- 🟡 **Medium Priority**: Moderate competition or seasonal",
        f"- 🟢 **Low Priority**: Niche topic, long-tail\n",
    ]
    
    for lang in ["tr", "en"]:
        lang_name = "🇹🇷 Türkçe" if lang == "tr" else "🇬🇧 English"
        md_lines.append(f"## {lang_name}\n")
        for idea in report["languages"][lang]:
            prio = idea["priority"]
            md_lines.append(f"### {prio['emoji']} {idea['title']}")
            md_lines.append(f"**Slug:** `{idea['slug']}`")
            md_lines.append(f"**Excerpt:** {idea['excerpt']}")
            md_lines.append(f"**Keywords:** {', '.join(idea['keywords'])}")
            md_lines.append(f"**Priority Score:** {prio['score']}/100\n")
    
    md_path = os.path.join(REPORTS_DIR, f"blog-ideas-{today}.md")
    with open(md_path, "w") as f:
        f.write("\n".join(md_lines))
    
    # Also save JSON
    json_path = os.path.join(REPORTS_DIR, f"blog-ideas-{today}.json")
    with open(json_path, "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Blog ideas saved to:")
    print(f"   📄 {md_path}")
    print(f"   📊 {json_path}")
    return report

def _calculate_blog_priority(keywords: list) -> dict:
    """Calculate priority score based on keyword competitiveness."""
    # Simplified scoring: long-tail = higher priority
    base_score = 70
    avg_length = sum(len(k.split()) for k in keywords) / len(keywords)
    
    # Longer, more specific keywords = lower competition = higher priority
    if avg_length >= 4:
        base_score += 20
    elif avg_length >= 3:
        base_score += 10
    
    if "2026" in " ".join(keywords):
        base_score += 10  # Timely content
    
    if "ucuz" in " ".join(keywords).lower() or "cheap" in " ".join(keywords).lower():
        base_score += 5  # Commercial intent
    
    if base_score >= 85:
        emoji = "🔴"
    elif base_score >= 70:
        emoji = "🟡"
    else:
        emoji = "🟢"
    
    return {"score": min(base_score, 100), "emoji": emoji}

def main():
    report = generate_blog_recommendations()
    
    print(f"\n{'='*50}")
    print(f"BLOG AUTO-PUBLISHER — TOP IDEAS")
    print(f"{'='*50}")
    
    for lang in ["tr", "en"]:
        lang_name = "🇹🇷 Türkçe" if lang == "tr" else "🇬🇧 English"
        print(f"\n{lang_name}:")
        for idea in report["languages"][lang][:3]:
            print(f"  {idea['priority']['emoji']} {idea['title']}")
            print(f"     Keywords: {', '.join(idea['keywords'])}")

if __name__ == "__main__":
    main()
