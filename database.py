import os
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime
load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_all_application_ids():
    response=supabase.table("events").select("application_id").execute()
    ids=set()

    for data in response.data:
        ids.add(data["application_id"])
    
    return list(ids)

def get_current_stage(application_id):
    response = (
        supabase.table("events")
        .select("*")
        .eq("application_id", application_id)
        .eq("event_type", "stage_changed")
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    if response.data:
        return response.data[0]["payload"]["to_stage"]
    return "discovered"


def get_application_details(application_id):
    response = (
        supabase.table("events")
        .select("*")
        .eq("application_id", application_id)
        .eq("event_type", "application_created")
        .execute()
    )
    if response.data:
        return response.data[0]["payload"]
    return {"company_name": "Unknown", "job_title": "", "found_from": ""}

def get_all_events_for_application(application_id):
    response = (
        supabase.table("events")
        .select("*")
        .eq("application_id", application_id)
        .order("created_at", desc=False)
        .execute()
    )
    return response.data

if __name__ == "__main__":
    events = get_all_events_for_application("d88a201d-0bd6-44c6-8e68-9f48a12db3dd")
    print(len(events))
    for event in events:
        print(event["event_type"], "-", event["created_at"])

stage_events = []
for event in events:
    if event["event_type"] == "application_created" or event["event_type"] == "stage_changed":
        stage_events.append(event)
print(stage_events)

def get_time_in_stage(application_id):
    all_events = get_all_events_for_application(application_id)
    
    stage_events = []
    for event in all_events:
        if event["event_type"] == "application_created" or event["event_type"] == "stage_changed":
            stage_events.append(event)
    
    durations = []
    for i in range(len(stage_events) - 1):
        current_event = stage_events[i]
        next_event = stage_events[i + 1]
        
        if current_event["event_type"] == "application_created":
            from_stage = "discovered"
        else:
            from_stage = current_event["payload"]["to_stage"]
        
        to_stage = next_event["payload"]["to_stage"]
        
        t1 = datetime.fromisoformat(current_event["created_at"])
        t2 = datetime.fromisoformat(next_event["created_at"])
        duration = t2 - t1
        
        durations.append({
            "from_stage": from_stage,
            "to_stage": to_stage,
            "duration_days": duration.total_seconds() / 86400
        })
    
    return durations
duration=get_time_in_stage("d88a201d-0bd6-44c6-8e68-9f48a12db3dd")
print(f"Durations: {duration} ")