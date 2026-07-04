from fastapi import FastAPI
from database import supabase
from pydantic import BaseModel
app = FastAPI()

class CreateEvent(BaseModel):
    application_id :str
    event_type : str
    payload: dict 
    source:str

@app.get("/health")
def health():
    return {"status": "ok"}



@app.get("/db_events")
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
