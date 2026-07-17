import os
from dotenv import load_dotenv
from groq import Groq
import json
import requests 
import uuid
load_dotenv()



sample_emails=[{
    "text": "Subject: Thank You for Your Application\n\nThank you for your interest in this position. Your application is currently under review, and our team will reach out if your background is a strong match.",
    "category": "awaiting_response"
},
   {
        "text": "Subject: Update on your Deloitte Software Engineering Summer Scholar Application\n\nThank you for taking the time to apply and interview with us. After careful consideration, we have decided to move forward with other candidates whose experience more closely aligns with our current needs. We encourage you to apply for future openings.",
        "category": "rejection"
    },
    {
        "text": "Subject: Interview Invitation — DV Engineer Role at Nvidia\n\nThank you for your application. We were impressed by your background and would like to invite you to schedule a 30-minute technical screening call. Please use this link to select a time that works for you this week.",
        "category": "interview_invite"
    },
    {
        "text": "Subject: Complete Your Coding Assessment — Anthropic AI Engineer Intern\n\nAs the next step in your application, please complete the attached coding assessment within 5 business days. The assessment consists of two problems and should take approximately 60 minutes.",
        "category": "online_assessment"
    },
    {
        "text": "Subject: Exciting AI Engineering Opportunities — Let's Connect\n\nHi, I came across your profile and think you'd be a great fit for some current openings in AI/ML on my team. Would you be open to a quick chat this week to learn more?",
        "category": "recruiter_ping"
    },
    {
        "text": "Subject: Your weekly tech digest is here\n\nThis week in tech: 5 trends shaping AI in 2026, top open-source tools to watch, and more. Unsubscribe here.",
        "category": "noise"
    }]




numbered_emails = []
for i, email in enumerate(sample_emails):
    numbered_emails.append(f"Email {i}: {email['text']}")
emails_text = "\n".join(numbered_emails)

print(emails_text)


client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": f"""Here are numbered emails: {emails_text}.

Classify each email into EXACTLY one of these six categories: rejection,
interview_invite, online_assessment, recruiter_ping, awaiting_response, noise.
For each email, give a confidence score from 0 to 100. Respond with ONLY
a JSON object with exactly this shape: {{{{"classifications": [{{{{"index": 0,
"category": "...", "confidence": ...}}}}]}}}}. No other text."""}
    ],
    response_format={"type": "json_object"}
)
reply = completion.choices[0].message.content
data = json.loads(reply)
print(data)


stage_map = {
    "rejection": "rejected",
    "interview_invite": "interview",
    "online_assessment": "interview"
}

for item in data['classifications']:
    email_log = {
        "application_id": "d88a201d-0bd6-44c6-8e68-9f48a12db3dd",
        "event_type": "email_classified",
        "payload": {"category": item['category'], "confidence": item['confidence']},
        "source": "inbox_agent"
    }

    if item['confidence'] >= 70:
        requests.post("http://127.0.0.1:8000/events", json=email_log)
        print("Logged:", email_log)
        mapped_stage = stage_map.get(item['category'])
        if mapped_stage:
            stage_event = {
                "application_id": "d88a201d-0bd6-44c6-8e68-9f48a12db3dd",
                "event_type": "stage_changed",
                "payload": {"to_stage": mapped_stage},
                "source": "inbox_agent"
            }
            requests.post("http://127.0.0.1:8000/events", json=stage_event)
            print("Posted:", stage_event)

    else:
        print(sample_emails[item['index']]['text'])
        print(f"Model guess: {item['category']}, confidence {item['confidence']}")
        answer = input("Approve this classification? (y/n): ")
        if answer.lower() == "y":
            requests.post("http://127.0.0.1:8000/events", json=email_log)
            print("Logged:", email_log)
            mapped_stage = stage_map.get(item['category'])
            if mapped_stage:
                stage_event = {
                    "application_id": "d88a201d-0bd6-44c6-8e68-9f48a12db3dd",
                    "event_type": "stage_changed",
                    "payload": {"to_stage": mapped_stage},
                    "source": "inbox_agent"
                }
                requests.post("http://127.0.0.1:8000/events", json=stage_event)
                print("Posted:", stage_event)
        else:
            print("Not approved — nothing posted.")
        