import os
from dotenv import load_dotenv
from groq import Groq
import json
load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Define your desired schema
event_schema = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "job_title": {"type": "string"},
        "found_from": {"type": "string"}
    },
    "required": ["company_name", "job_title", "found_from"],
    "additionalProperties": False
}

completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", 
        "content": " Extract the job details from the posting below. "
        "Respond with ONLY a JSON object with exactly these keys: company_name, job_title, found_from. No other text."
        " Posting: [We're hiring! Nvidia's silicon engineering group is looking for a CPU Design Verification Engineer to join the Grace team in Santa Clara. Saw this role trending on LinkedIn this week. Competitive comp, hybrid schedule...]   "}
    ],
    # Enforce the strict schema
    response_format={"type": "json_object"}
)

reply=completion.choices[0].message.content
data=json.loads(reply)
print(data)
print("Company: ", data["company_name"] )