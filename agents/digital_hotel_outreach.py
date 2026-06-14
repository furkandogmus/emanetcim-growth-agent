#!/usr/bin/env python3
"""
Digital Hotel Outreach Strategy — BagajPark Growth Agent
==========================================================
No physical contact needed. Pure digital pipeline to acquire hotel partners.

Channels:
1. Booking.com / Expedia host messaging
2. Google Maps hotel reviews + contact
3. Hotel WhatsApp Business API
4. LinkedIn hotel groups
5. Travel agency partnerships
6. Email outreach via hotelfinder tools
"""

import json
import os
import datetime

REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

DIGITAL_STRATEGIES = [
    {
        "id": "booking-messages",
        "name": "Booking.com / Expedia Misafir Yorumlarına Cevap",
        "emoji": "🏨",
        "difficulty": "Düşük",
        "impact": "🔥 Yüksek",
        "description": "Booking.com ve Expedia'da İstanbul otellerinin yorumlarına bak. 'Check-out erken, valizle gezmek zorunda kaldık' gibi şikayetleri bul. Otele BagajPark çözümünü anlatan kısa bir mesaj gönder. Otel zaten bu sorunu yaşıyor, çözüm sunuyorsun.",
        "steps": [
            "Booking.com'da Sultanahmet otellerini ara",
            "Düşük puanlı yorumları tara (özellikle 'check-out', 'bagaj', 'valiz' geçenler)",
            "Otel WhatsApp/email'ini bul (genelde sitelerinde var)",
            "Şu mesajı gönder: 'Merhaba, misafir yorumlarınızda check-out sonrası valiz sorunundan bahsedildiğini gördük. BagajPark ile bu sorunu çözüp %10 komisyon kazanabilirsiniz. Detay: bagajpark.com/tr/hotels'"
        ],
        "tools": ["Booking.com", "Google Maps", "Otel websitesi"]
    },
    {
        "id": "google-maps",
        "name": "Google Maps Otel Keşfi + Otomatik Mesaj",
        "emoji": "📍",
        "difficulty": "Düşük",
        "impact": "🔥 Yüksek",
        "description": "Google Maps'te 'Sultanahmet otel', 'Taksim otel' diye ara. Çıkan otellerin web sitelerini ziyaret et. İletişim sayfasından WhatsApp/email bul. Her gün 10 otele mesaj at. Hedef: Ayda 300 otel.",
        "steps": [
            "Google Maps → 'Sultanahmet otel' ara",
            "Her otelin web sitesine gir, WhatsApp numarasını bul",
            "Toplu bir WhatsApp listesi oluştur",
            "Günde 10 otele mesaj at (kişisel, spam değil)"
        ],
        "tools": ["Google Maps", "WhatsApp", "Otel websitesi"]
    },
    {
        "id": "linkedin-hotels",
        "name": "LinkedIn Otel Grupları + Hotel Manager Outreach",
        "emoji": "💼",
        "difficulty": "Orta",
        "impact": "🟡 Orta",
        "description": "LinkedIn'de 'Hotel Manager Istanbul', 'Otel Müdürü', 'Hospitality Turkey' gruplarına katıl. Her gün 1 değerli post paylaş (BagajPark'ın otellere faydası hakkında). Direkt satış yapma, önce değer ver.",
        "steps": [
            "LinkedIn'de 'Otel Müdürü İstanbul', 'Hotel Managers Turkey' ara",
            "Gruplara katıl",
            "Haftada 2 post: 'Check-out sonrası misafir memnuniyetini artırmanın 3 yolu' gibi",
            "Profiline bagajpark.com linkini ekle"
        ],
        "tools": ["LinkedIn"]
    },
    {
        "id": "whatsapp-broadcast",
        "name": "WhatsApp Business Broadcast Listesi",
        "emoji": "📱",
        "difficulty": "Düşük",
        "impact": "🔥 Yüksek",
        "description": "Topladığın otel WhatsApp numaralarını bir broadcast listesine ekle. Haftada bir kısa bir duyuru gönder: 'Yeni şehir eklendi: [şehir adı]' veya 'Bu ay otel partnerlerimize özel %5 ek komisyon'. Alıcılar birbirini görmez, gizlilik korunur.",
        "steps": [
            "WhatsApp Business indir",
            "Broadcast list oluştur: 'BagajPark Otel Partnerleri'",
            "Haftada 1 mesaj gönder (değerli içerik, satış değil)"
        ],
        "tools": ["WhatsApp Business"]
    },
    {
        "id": "travel-agencies",
        "name": "Seyahat Acenteleri ve Tur Operatörleri",
        "emoji": "✈️",
        "difficulty": "Orta",
        "impact": "🟡 Orta",
        "description": "İstanbul'daki tur operatörlerine ve seyahat acentelerine ulaş. Onlar zaten müşterilerine 'valiz emanet' öneriyor. BagajPark'ı resmi öneri olarak ekleyelim. Acente, müşterisine link gönderir, senden komisyon alır.",
        "steps": [
            "İstanbul seyahat acenteleri listesi çıkar (Google'da)",
            "Her birine email at: 'Müşterilerinize valiz emanet öneriyor musunuz?'",
            "Partnerlik teklif et (acente özel indirim kodu)"
        ],
        "tools": ["Google", "Email"]
    },
    {
        "id": "tripadvisor-claim",
        "name": "TripAdvisor Otel Mesajlaşma",
        "emoji": "📝",
        "difficulty": "Düşük",
        "impact": "🟡 Orta",
        "description": "TripAdvisor'da otel sayfalarına gir. 'Management' bölümünden otele mesaj gönderebilirsin (otel sahibi olduğunu iddia etmeden). Kısa ve net: 'BagajPark ile check-out sonrası valiz sorununu çözün.'",
        "steps": [
            "TripAdvisor → İstanbul otelleri",
            "Her otelin sayfasında 'Send message to management'",
            "Kısa tanıtım mesajı gönder"
        ],
        "tools": ["TripAdvisor"]
    }
]

# Pre-written message templates
MESSAGE_TEMPLATES = {
    "tr": {
        "whatsapp_short": (
            "Merhaba [Otel Adı] ekibi,\n\n"
            "Ben BagajPark'tan [İsmin]. Oteliniz için bir iş birliği teklifimiz var:\n\n"
            "🔹 Misafirleriniz check-out sonrası valizlerini en yakın BagajPark noktasına bırakır\n"
            "🔹 Siz ön büroda bagaj biriktirmekten kurtulursunuz\n"
            "🔹 Her yönlendirmede %10 komisyon kazanırsınız\n\n"
            "Detay: bagajpark.com/tr/hotels\n\n"
            "10 dakikalık bir görüşmeye ne dersiniz?"
        ),
        "email_short": (
            "Merhaba,\n\n"
            "BagajPark olarak otel misafirlerinizin check-out sonrası valiz sorununa "
            "pratik bir çözüm sunuyoruz.\n\n"
            "Misafirleriniz sizden çıkış yaptıktan sonra valizlerini en yakın "
            "BagajPark noktasına bırakıp şehri özgürce gezebilir. Siz de her "
            "yönlendirmede %10 komisyon kazanırsınız. Operasyonel yük sıfır.\n\n"
            "Detaylı bilgi: bagajpark.com/tr/hotels\n\n"
            "Gorusmek uzere,\n"
            "[İsmin]\n"
            "BagajPark"
        ),
        "booking_complaint_response": (
            "Merhaba, misafir yorumlarınızda check-out sonrası bagaj sorunundan "
            "bahsedildiğini gördük. BagajPark ile bu sorunu çözmek ister misiniz? "
            "Detay: bagajpark.com/tr/hotels"
        )
    },
    "en": {
        "whatsapp_short": (
            "Hi [Hotel Name] team,\n\n"
            "I'm [Name] from BagajPark. We have a partnership proposal:\n\n"
            "🔹 Your guests store luggage at nearby BagajPark points after checkout\n"
            "🔹 You free up lobby space\n"
            "🔹 You earn 10% commission per referral\n\n"
            "Details: bagajpark.com/en/hotels\n\n"
            "Up for a 10-minute call?"
        ),
        "email_short": (
            "Hi,\n\n"
            "BagajPark offers a practical solution for your guests' post-checkout "
            "luggage problem.\n\n"
            "Your guests drop their bags at a nearby BagajPark point after checkout "
            "and explore the city hands-free. You earn 10% commission per referral. "
            "Zero operational burden.\n\n"
            "Learn more: bagajpark.com/en/hotels\n\n"
            "Best regards,\n"
            "[Name]\n"
            "BagajPark"
        ),
        "booking_complaint_response": (
            "Hi, we noticed your guest reviews mention checkout luggage issues. "
            "Would you like to solve this with BagajPark? "
            "Details: bagajpark.com/en/hotels"
        )
    }
}

WEEKLY_PLAN = [
    {"day": "Pazartesi", "task": "Booking.com'da 5 otel bul + şikayet yorumlarını tara", "duration": "30dk"},
    {"day": "Salı", "task": "WhatsApp broadcast: haftalık değer mesajı gönder", "duration": "15dk"},
    {"day": "Çarşamba", "task": "LinkedIn'de 1 değerli post paylaş + 10 hotel manager'a bağlantı isteği", "duration": "30dk"},
    {"day": "Perşembe", "task": "Google Maps'ten 10 yeni otel bul + iletişim bilgilerini topla", "duration": "30dk"},
    {"day": "Cuma", "task": "Haftalık toplu email gönderimi (toplanan tüm otellere)", "duration": "20dk"},
    {"day": "Cumartesi", "task": "Haftalık rapor: kaç otel ulaşıldı, kaçı dönüş yaptı", "duration": "15dk"},
]

def generate_digital_strategy():
    today = datetime.date.today().isoformat()

    report = {
        "generated_at": today,
        "type": "digital_hotel_outreach",
        "total_strategies": len(DIGITAL_STRATEGIES),
        "strategies": DIGITAL_STRATEGIES,
        "templates": MESSAGE_TEMPLATES,
        "weekly_plan": WEEKLY_PLAN,
        "key_principle": "Önce değer ver, sonra sat. Spam yapma, çözüm sun.",
        "estimated_hotels_per_month": 300,
        "estimated_conversion_rate": "5-10%",
        "estimated_partners_per_month": "15-30 otel"
    }

    report_path = os.path.join(REPORTS_DIR, f"digital-hotel-outreach-{today}.json")
    with open(report_path, "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # Markdown version
    md = [
        f"# Dijital Otel Stratejisi — {today}",
        "",
        "> *Fiziksel temasa gerek yok. Tamamen dijital kanallardan otel partner kazanımı.*",
        "",
        f"**Tahmini aylık erişim:** {report['estimated_hotels_per_month']} otel",
        f"**Tahmini dönüşüm:** {report['estimated_conversion_rate']}",
        f"**Tahmini partner/ay:** {report['estimated_partners_per_month']}",
        "",
        "---",
        "## 📋 Haftalık Plan",
        "",
        "| Gün | Görev | Süre |",
        "|---|---|---|",
    ]
    for item in WEEKLY_PLAN:
        md.append(f"| {item['day']} | {item['task']} | {item['duration']} |")

    md.extend([
        "",
        "---",
        "## 🎯 Stratejiler",
        "",
    ])
    for s in DIGITAL_STRATEGIES:
        md.append(f"### {s['emoji']} {s['name']}")
        md.append(f"**Zorluk:** {s['difficulty']}  \n**Etki:** {s['impact']}")
        md.append(f"")
        md.append(s['description'])
        md.append(f"")
        md.append("Adımlar:")
        for step in s['steps']:
            md.append(f"- {step}")
        md.append(f"\nAraçlar: {', '.join(s['tools'])}\n")

    md.extend([
        "---",
        "## 💬 Mesaj Şablonları",
        "",
        "### WhatsApp Kısa (TR)",
        "```",
        MESSAGE_TEMPLATES["tr"]["whatsapp_short"],
        "```",
        "",
        "### Email Kısa (TR)",
        "```",
        MESSAGE_TEMPLATES["tr"]["email_short"],
        "```",
        "",
        "### WhatsApp Short (EN)",
        "```",
        MESSAGE_TEMPLATES["en"]["whatsapp_short"],
        "```",
        "",
        "### Yorum Cevabı (TR)",
        "```",
        MESSAGE_TEMPLATES["tr"]["booking_complaint_response"],
        "```",
    ])

    md_path = os.path.join(REPORTS_DIR, f"digital-hotel-outreach-{today}.md")
    with open(md_path, "w") as f:
        f.write("\n".join(md))

    print(f"✅ Digital hotel outreach strategy saved!")
    print(f"   📄 {md_path}")
    return report

def main():
    report = generate_digital_strategy()

    print(f"\n{'='*55}")
    print(f"DİJİTAL OTEL STRATEJİSİ — ÖZET")
    print(f"{'='*55}")
    print(f"\n🎯 {len(report['strategies'])} strateji, {report['estimated_hotels_per_month']} otel/ay hedef")
    print()
    for s in report['strategies']:
        print(f"  {s['emoji']} {s['name']} — {s['impact']}")
    print()
    print("📋 Haftalık Plan (toplam ~2 saat/hafta):")
    for item in report['weekly_plan']:
        print(f"  {item['day']}: {item['task']} ({item['duration']})")
    print()
    print("💡 Temel prensip: Önce değer ver, sonra sat.")

if __name__ == "__main__":
    main()
