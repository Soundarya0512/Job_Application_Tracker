import os
from dotenv import load_dotenv
from groq import Groq
import json
import requests 
import uuid
load_dotenv()


client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", 
        "content": " Extract the job details from the posting below. "
        "Respond with ONLY a JSON object with exactly these keys: company_name, job_title, found_from. No other text."
        " Posting: [ We're looking for professional Bus Drivers who take pride in delivering a first-class experience for every passenger. If you're passionate about safe driving, enjoy working with people, and want to join a company that values its employees through competitive pay, modern equipment, comprehensive benefits, and opportunities for career growth, we'd love to have you on our team.Unlike many school transportation companies, Bauer's offers year-round employment, giving our drivers consistent work and dependable income throughout the year—not just during the school calendar..]   "}
    ],
    # Enforce the strict schema
    response_format={"type": "json_object"}
)

reply=completion.choices[0].message.content
data=json.loads(reply)
#print(data)
#print("Company: ", data["company_name"] )

def helper_fun(value):
    if value is None:
        return True
    clean=value.strip().lower()

    if clean in ["not specified", "unknown", "n/a", ""]:
        return True
    return False

if helper_fun(data["company_name"]) or helper_fun(data["job_title"]):
    print("Required details missing. Skipping this post.")
else:
    event = {
        "application_id": str(uuid.uuid4()),     # a fresh unique id — Python's uuid, as a string
        "event_type": "application_created",         # the EXACT string your board filters on
        "payload": data,            # you already have this whole dict
        "source": "ingestion_agent"             # the AI's signature
    }
    requests.post("http://127.0.0.1:8000/events", json=event)
    print("Posted:", event)