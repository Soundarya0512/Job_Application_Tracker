from fastapi import FastAPI
from database import supabase
from pydantic import BaseModel
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
from database import supabase, get_current_stage, get_all_application_ids,get_application_details

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



@app.get("/applications/{application_id}/stage")
def get_stage(application_id: str):
    return {"stage": get_current_stage(application_id)}


@app.get("/board")
def get_board():
    result={}
    for app_id in get_all_application_ids():
        stage=get_current_stage(app_id)
        details = get_application_details(app_id)
        if stage not in result:
            result[stage]=[]
        result[stage].append({"application_id": app_id, "details": details})
    return result

@app.get("/metrics")
def get_metrics():
    result = get_board()
    funnel_counts = {}
    for stage, apps in result.items():
        funnel_counts[stage] = len(apps)
    return {"funnel": funnel_counts}
