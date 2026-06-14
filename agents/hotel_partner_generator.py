#!/usr/bin/env python3
"""
Hotel Partnership Generator — BagajPark Growth Agent
=====================================================
Generates outreach content for hotel partnerships:
- Value proposition summaries per city
- Commission model suggestions
- Email/DM templates for hotel outreach
- Target hotel lists per city

To run: python3 agents/hotel_partner_generator.py
"""

import json
import os
import sys
import datetime

REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

# Target hotel density per city (approximate)
TARGET_CITIES = {
    "istanbul": {
        "country": "Türkiye",
        "total_hotels_approx": 4500,
        "target_zone": "Sultanahmet, Taksim, Kadıköy, Beşiktaş, Karaköy",
        "top_districts": ["Sultanahmet", "Taksim", "Kadıköy", "Beşiktaş", "Şişli", "Beyoğlu"],
        "hotel_types": ["boutique", "chain", "hostel", "apartment"]
    },
    "antalya": {
        "country": "Türkiye",
        "total_hotels_approx": 2500,
        "target_zone": "Kaleiçi, Lara, Konyaaltı, Belek",
        "top_districts": ["Kaleiçi", "Lara", "Konyaaltı", "Belek"],
        "hotel_types": ["resort", "all-inclusive", "boutique"]
    },
    "izmir": {
        "country": "Türkiye",
        "total_hotels_approx": 800,
        "target_zone": "Alsancak, Konak, Karşıyaka, Çeşme",
        "top_districts": ["Alsancak", "Konak", "Karşıyaka"],
        "hotel_types": ["boutique", "chain", "hostel"]
    },
    "ankara": {
        "country": "Türkiye",
        "total_hotels_approx": 900,
        "target_zone": "Kızılay, Çankaya, Kavaklıdere",
        "top_districts": ["Kızılay", "Çankaya", "Kavaklıdere"],
        "hotel_types": ["business", "chain", "boutique"]
    },
    "bodrum": {
        "country": "Türkiye",
        "total_hotels_approx": 600,
        "target_zone": "Bodrum Merkez, Marina, Yalıkavak, Türkbükü",
        "top_districts": ["Merkez", "Yalıkavak", "Türkbükü", "Gümbet"],
        "hotel_types": ["resort", "boutique", "villa"]
    },
    "cappadocia": {
        "country": "Türkiye",
        "total_hotels_approx": 400,
        "target_zone": "Göreme, Ürgüp, Uçhisar, Avanos",
        "top_districts": ["Göreme", "Ürgüp", "Uçhisar"],
        "hotel_types": ["cave_hotel", "boutique", "hostel"]
    }
}

HOTEL_VALUE_PROPOSITIONS_TR = {
    "small_boutique": {
        "title": "Bagaj odası yok mu? Sorun değil!",
        "body": "Küçük butik otellerde bagaj odası olmaması büyük bir müşteri memnuniyetsizliği kaynağıdır. Misafirleriniz check-out sonrası valizlerini BagajPark iş ortağı bir dükkana bırakabilir, siz de ön büroda bagaj tutma derdinden kurtulursunuz. Komisyon modelimizle ek gelir elde edersiniz.",
        "pain_points": ["Bagaj odası yok", "Ön büroda bagaj birikiyor", "Misafir şikayetleri"]
    },
    "chain_hotel": {
        "title": "Check-out deneyimini iyileştirin",
        "body": "Zincir oteller için standart check-out sürecine entegre bir çözüm. Misafirler check-out sırasında valizlerini BagajPark'a yönlendirilir, otel %10 komisyon kazanır. Otel personeli bagajla uğraşmaz, misafir memnuniyeti artar. 11 dil desteği ile uluslararası misafirleriniz için ideal.",
        "pain_points": ["Personel bagaj taşıyor", "Check-out yoğunluğu", "Son gün şikayetleri"]
    },
    "hostel": {
        "title": "Sırtçantalı gezginler için bagaj çözümü",
        "body": "Hostel misafirleri genelde büyük sırtçantalarla seyahat eder. Check-out sonrası şehri gezmek isterler ama bagajlarını bırakacak yer bulamazlar. BagajPark ile dakikalar içinde rezervasyon yaparlar. Hostelinize özel indirim kodu ile misafir memnuniyetini artırın.",
        "pain_points": ["Büyük sırtçantalar", "Geç check-out talepleri", "Gürültü şikayetleri"]
    },
    "resort": {
        "title": "Son günü tatil olarak yaşatın",
        "body": "Resort otellerde misafirler check-out sonrası genelde lobide veya havuz başında bekler. BagajPark ile valizlerini emanet edip şehri keşfedebilirler. Özellikle Antalya ve Bodrum'daki resortlar için plaj-sonrası-valiz şeklinde bir deneyim sunuyoruz.",
        "pain_points": ["Misafir tesiste sıkışıp kalıyor", "Havuz başı bagaj güvenliği", "Geç uçuşlar"]
    }
}

COMMISSION_MODELS = [
    {
        "name": "Temel Ortaklık (Önerilen)",
        "description": "Otel, BagajPark noktasına yönlendirdiği her misafir için %10 komisyon alır. Ek gelir, sıfır operasyonel yük.",
        "otel_effort": "Düşük",
        "revenue_potential": "Orta",
        "best_for": "Butik oteller, hosteller"
    },
    {
        "name": "Premium Ortaklık",
        "description": "Otel bünyesinde BagajPark noktası açılır. Otel, kendi alanında bagaj kabul eder, her işlemden %15-20 komisyon alır.",
        "otel_effort": "Orta",
        "revenue_potential": "Yüksek",
        "best_for": "Zincir oteller, büyük hosteller"
    },
    {
        "name": "Otel Partner Ağı",
        "description": "Otel grubu ile toplu anlaşma. Tüm otellerde BagajPark yönlendirmesi + ortak pazarlama. Aylık sabit ücret + değişken komisyon.",
        "otel_effort": "Düşük",
        "revenue_potential": "Çok Yüksek",
        "best_for": "Otel zincirleri, gruplar"
    }
]

def generate_outreach_content():
    """Generate complete hotel outreach package."""
    today = datetime.date.today().isoformat()

    report = {
        "generated_at": today,
        "type": "hotel_partnership_strategy",
        "target_cities": list(TARGET_CITIES.keys()),
        "commission_models": COMMISSION_MODELS,
        "total_addressable_hotels": sum(c["total_hotels_approx"] for c in TARGET_CITIES.values()),
        "outreach_templates": generate_email_templates(),
        "city_strategies": generate_city_strategies(),
        "pitch_deck_points": [
            "Otel, bagaj odası veya personel ayırmak zorunda kalmaz",
            "Misafir check-out sonrası şehri özgürce keşfeder",
            "Otel ek gelir elde eder (%10-20 komisyon)",
            "Memnuniyet skorları artar",
            "Online rezervasyon, ön büro yükünü azaltır",
            "11 dil desteği ile uluslararası misafirlere hitap",
            "Sigortalı ve mühürlü bagaj güvenliği",
            "Rakiplerinizden (Bounce) önce davranın"
        ],
        "quick_wins": [
            "Sultanahmet'teki 10 butik otele birebir ziyaret",
            "Airbnb ev sahiplerine dijital kart dağıtımı",
            "Otel resepsiyonlarına BagajPark QR kartpostal",
            "Booking.com/Expedia mesajlarına BagajPark linki ekleme"
        ]
    }

    report_path = os.path.join(REPORTS_DIR, f"hotel-partnerships-{today}.json")
    with open(report_path, "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # Also generate a markdown summary
    md_lines = [
        f"# BagajPark Otel Partner Stratejisi — {today}",
        "",
        f"**Toplam hedef otel sayısı:** {report['total_addressable_hotels']:,}",
        f"**Hedef şehirler:** {len(TARGET_CITIES)} şehir",
        "",
        "## Hızlı Kazanımlar (Bu Hafta Yapılacaklar)",
        "",
    ]
    for qw in report["quick_wins"]:
        md_lines.append(f"- [ ] {qw}")

    md_lines.extend([
        "",
        "## Hedef Şehirler ve Potansiyel",
        "",
        "| Şehir | Toplam Otel | Hedef Bölge |",
        "|---|---|---|",
    ])
    for city_name, city_data in TARGET_CITIES.items():
        md_lines.append(f"| {city_name.title()} | ~{city_data['total_hotels_approx']:,} | {city_data['target_zone']} |")

    md_lines.extend([
        "",
        "## Misafir Değer Önerileri",
        "",
    ])
    for hotel_type, vp in HOTEL_VALUE_PROPOSITIONS_TR.items():
        md_lines.append(f"### {hotel_type.replace('_', ' ').title()}")
        md_lines.append(f"**{vp['title']}**")
        md_lines.append(vp['body'])
        md_lines.append(f"Acı noktaları: {', '.join(vp['pain_points'])}")
        md_lines.append("")

    md_lines.extend([
        "## Komisyon Modelleri",
        "",
        "| Model | Açıklama | Çaba | En Uygun |",
        "|---|---|---|---|",
    ])
    for m in COMMISSION_MODELS:
        md_lines.append(f"| **{m['name']}** | {m['description']} | {m['otel_effort']} | {m['best_for']} |")

    md_lines.extend([
        "",
        "## Satış Konuşması (Pitch) Ana Noktaları",
        "",
    ])
    for p in report["pitch_deck_points"]:
        md_lines.append(f"- ✅ {p}")

    md_lines.extend([
        "",
        "## Email/WhatsApp Template (TR)",
        "",
        "```",
        "Merhaba [Otel Adı] ekibi,",
        "",
        "İstanbul'da faaliyet gösteren BagajPark olarak, otel misafirlerinizin",
        "check-out sonrası valiz sorununa pratik bir çözüm sunuyoruz.",
        "",
        "Misafirleriniz sizden çıkış yaptıktan sonra valizlerini en yakın",
        "BagajPark noktasına bırakıp şehri özgürce gezebilir. Siz de",
        "ön büroda bagaj biriktirmekten kurtulursunuz.",
        "",
        "Üstelik her yönlendirmede %10 komisyon kazanırsınız.",
        "",
        "Detaylı bilgi için: https://bagajpark.com/tr/hotels",
        "",
        "Görüşmek üzere,",
        "BagajPark Ekibi",
        "```",
        "",
        "## Email Template (EN)",
        "",
        "```",
        "Hi [Hotel Name] team,",
        "",
        "We're BagajPark, a luggage storage network operating across Turkey.",
        "We help hotels solve the post-checkout luggage problem.",
        "",
        "Your guests can store their bags at nearby BagajPark points after",
        "checkout and explore the city hands-free. No more luggage cluttering",
        "your lobby or front desk. And you earn 10% commission per referral.",
        "",
        "Learn more: https://bagajpark.com/en/hotels",
        "",
        "Best regards,",
        "BagajPark Team",
        "```",
    ])

    md_path = os.path.join(REPORTS_DIR, f"hotel-partnerships-{today}.md")
    with open(md_path, "w") as f:
        f.write("\n".join(md_lines))

    print(f"✅ Hotel partnership strategy saved to:")
    print(f"   📄 {md_path}")
    print(f"   📊 {report_path}")
    return report

def generate_email_templates():
    return {
        "tr": {
            "subject": "Otel misafirleriniz için bagaj çözümü",
            "body": "Merhaba, misafirlerinizin check-out sonrası valiz sorununa pratik bir çözüm sunuyoruz..."
        },
        "en": {
            "subject": "Luggage solution for your hotel guests",
            "body": "Hi, we offer a practical solution for your guests' post-checkout luggage problem..."
        }
    }

def generate_city_strategies():
    strategies = {}
    for city, data in TARGET_CITIES.items():
        strategies[city] = {
            "estimated_hotels": data["total_hotels_approx"],
            "priority_district": data["top_districts"][0],
            "best_approach": f"Visit {data['top_districts'][0]} district hotels in person with flyers"
        }
    return strategies

def main():
    report = generate_outreach_content()

    print(f"\n{'='*50}")
    print(f"HOTEL PARTNERSHIP GENERATOR — SUMMARY")
    print(f"{'='*50}")
    print(f"Total addressable hotels: {report['total_addressable_hotels']:,}")
    print(f"\n📋 Quick Wins (Do this week):")
    for qw in report["quick_wins"]:
        print(f"  ☐ {qw}")
    print(f"\n💰 Commission Models:")
    for m in report["commission_models"]:
        print(f"  • {m['name']}: {m['description'][:60]}...")

if __name__ == "__main__":
    main()
