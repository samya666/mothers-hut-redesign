import json
import datetime
import os

DISPATCH_LOG = r"G:\localpulse-ai\demos\mothers-hut-redesign\pitch_dispatch_record.json"

payload = {
    "status": "DISPATCHED_TO_QUEUE",
    "timestamp": datetime.datetime.now().isoformat(),
    "recipient": {
        "entity": "Mother's Hut (Garai Brothers / Partnership Firm)",
        "founders": ["Anath Bandhu Garai", "Kajori Garai", "Arindam Garai"],
        "primary_email": "care.mothershut@gmail.com",
        "primary_phone": "+91 9002525999",
        "address": "NH-12 (NH-34), Beside Garai Brothers IOCL Pump, Bhatjangla, Krishnanagar, Nadia, West Bengal 741102"
    },
    "subject": "Proposal & Strategic Growth Pitch: Mother's Hut Digital Redesign & Highway Expansion Memo",
    "delivery_channel": "Direct Founder Outreach & Digital Concierge Intake",
    "attachments": [
        "Mother's Hut 2.5K Walkthrough Experience (http://localhost:8080)",
        "Ananya AI Digital Concierge System",
        "Mother's Hut Investment & Commercial Expansion Pitch"
    ]
}

with open(DISPATCH_LOG, "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2)

print(f"Autonomous pitch package logged and staged for Mother's Hut leadership at {DISPATCH_LOG}")
