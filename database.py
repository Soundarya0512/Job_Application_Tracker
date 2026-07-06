import os
from dotenv import load_dotenv
from supabase import create_client

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