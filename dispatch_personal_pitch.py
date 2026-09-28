import json
import urllib.parse
import datetime

contacts = [
    {
        "name": "Arindam Garai",
        "designation": "Managing Partner & Proprietor",
        "phone": "+916296892007",
        "raw_phone": "916296892007",
        "type": "Personal / Primary Direct WhatsApp & Mobile"
    },
    {
        "name": "Arindam Garai (Line 2)",
        "designation": "Direct Executive / VIP Booking Line",
        "phone": "+916297235418",
        "raw_phone": "916297235418",
        "type": "Personal Direct Line"
    },
    {
        "name": "Anath Bandhu Garai & Kajori Garai (Partnership Desk)",
        "designation": "Founding Partners / Garai Brothers",
        "phone": "+917797000906",
        "raw_phone": "917797000906",
        "type": "Direct Registered Partnership Line"
    },
    {
        "name": "Mother's Hut Central Desk",
        "designation": "Central Desk & Reservation Line",
        "phone": "+919002525999",
        "raw_phone": "919002525999",
        "type": "Operational Desk Line"
    }
]

sender_details = {
    "name": "Samya",
    "email": "samya.pegusus@gmail.com",
    "phone": "+91 8617625059",
    "whatsapp": "+91 8617625059"
}

live_site = "https://samya666.github.io/mothers-hut-redesign/"

pitch_template = """Namaskar {name} Ji,

I have developed a brand-new, ultra-fast 2026 digital experience and guest acquisition platform specifically designed for **Mother's Hut Krishnanagar**:

🌐 **Live Experience Demo:**
{live_site}

**Key Enhancements Built for Mother's Hut:**
1. **Interactive 2.5K Highway & Dining Walkthrough:** High-definition virtual tour of Chowringhee, Basudha, Hut of the World, and Pergola.
2. **Ananya AI Digital Concierge:** Conversational AI trained on your exact menu, signature thalis, and highway traveler FAQs.
3. **High-Ticket Banquet & Event Funnel:** Direct one-tap booking engine for weddings, corporate retreats, and mega gatherings.
4. **Instant Highway Navigation:** Frictionless GPS routing for NH-12 / NH-34 travelers.

I would love to hand over this platform to your team and discuss how it can drive higher weekend footfall and banquet contracts.

**My Contact Details:**
• Name: Samya
• Phone / WhatsApp: +91 8617625059
• Email: samya.pegusus@gmail.com

Looking forward to speaking with you!
Warm regards,
Samya"""

dispatch_records = []

for c in contacts:
    msg = pitch_template.format(name=c["name"], live_site=live_site)
    encoded_msg = urllib.parse.quote(msg)
    wa_link = f"https://api.whatsapp.com/send?phone={c['raw_phone']}&text={encoded_msg}"
    wa_me_link = f"https://wa.me/{c['raw_phone']}?text={encoded_msg}"
    
    dispatch_records.append({
        "recipient_name": c["name"],
        "designation": c["designation"],
        "phone": c["phone"],
        "channel_type": c["type"],
        "whatsapp_api_link": wa_link,
        "whatsapp_direct_link": wa_me_link,
        "staged_message": msg,
        "status": "READY_FOR_TRANSMISSION"
    })

output_data = {
    "dispatch_id": "MOTHERS_HUT_DIRECT_OUTREACH_2026",
    "timestamp": datetime.datetime.now().isoformat(),
    "sender": sender_details,
    "live_demo_url": live_site,
    "github_repo": "https://github.com/samya666/mothers-hut-redesign",
    "contacts_count": len(dispatch_records),
    "records": dispatch_records
}

record_file = r"G:\localpulse-ai\demos\mothers-hut-redesign\pitch_dispatch_record.json"
with open(record_file, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"Successfully generated dispatch records for {len(dispatch_records)} verified personal contacts.")
