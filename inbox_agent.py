import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
from groq import Groq
import json, requests
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

creds = None
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
        token.write(creds.to_json())

service = build("gmail", "v1", credentials=creds)

results = service.users().messages().list(userId="me", labelIds=["INBOX"], maxResults=3).execute()
messages = results.get("messages", [])

stage_map = {
    "rejection": "rejected",
    "interview_invite": "interview",
    "online_assessment": "interview"
}

for message in messages:
    full_message = service.users().messages().get(userId="me", id=message["id"], format="full").execute()

    subject = ""
    for header in full_message["payload"]["headers"]:
        if header["name"] == "Subject":
            subject = header["value"]

    body = ""
    for part in full_message["payload"]["parts"]:
        if part["mimeType"] == "text/plain":
            encoded_data = part["body"]["data"]
            decoded_bytes = base64.urlsafe_b64decode(encoded_data)
            body = decoded_bytes.decode("utf-8")

    email_text = f"Subject: {subject}\n\n{body}"

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": f"""Here is an email: {email_text}.

Classify it into EXACTLY one of these six categories: rejection,
interview_invite, online_assessment, recruiter_ping, awaiting_response, noise.
Give a confidence score from 0 to 100. Respond with ONLY a JSON object
with exactly this shape: {{"category": "...", "confidence": ...}}. No other text."""}
        ],
        response_format={"type": "json_object"}
    )
    reply = completion.choices[0].message.content
    data = json.loads(reply)

    email_log = {
        "application_id": "d88a201d-0bd6-44c6-8e68-9f48a12db3dd",
        "event_type": "email_classified",
        "payload": {"category": data['category'], "confidence": data['confidence']},
        "source": "inbox_agent"
    }

    if data['confidence'] >= 70:
        requests.post("http://127.0.0.1:8000/events", json=email_log)
        print("Logged:", email_log)
        mapped_stage = stage_map.get(data['category'])
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
        print(email_text)
        print(f"Model guess: {data['category']}, confidence {data['confidence']}")
        answer = input("Approve this classification? (y/n): ")
        if answer.lower() == "y":
            requests.post("http://127.0.0.1:8000/events", json=email_log)
            print("Logged:", email_log)
            mapped_stage = stage_map.get(data['category'])
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