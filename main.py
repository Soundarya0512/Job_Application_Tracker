from fastapi import FastAPI
from database import supabase
from pydantic import BaseModel
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CreateEvent(BaseModel):
    application_id :str
    event_type : str
    payload: dict 
    source:str

@app.get("/health")
def health():
    return {"status": "ok"}



@app.get("/events")
def get_events():
    response = supabase.table("events").select("*").execute()
    return response.data

@app.post("/events")
def db_insert(event: CreateEvent):
    response = supabase.table("events").insert({
        "application_id": event.application_id,
        "event_type": event.event_type,
        "payload": event.payload,
        "source": event.source
    }).execute()
    return response.data    

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

@app.get("/applications/{application_id}/stage")
def get_stage(application_id: str):
    return {"stage": get_current_stage(application_id)}