
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from models import *
import service
from typing import List, Optional
from typing_extensions import Literal


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/getPatients",response_model=List[Patient])
def get_Patients(limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0),
               min_score: int = Query(0, ge=0, le=8), patient_nbr: Optional[int] = None,
               risk_level: Optional[Literal["MEDIUM", "HIGH"]] = None):
    return service.get_Patients(limit, offset, min_score, patient_nbr, risk_level)


# Update screen: patient_encounters joined with care_interventions
@app.get("/interventions/{encounter_id}", response_model=Intervention)
def get_intervention(encounter_id: int):
    try:
        return service.get_intervention(encounter_id)
    except service.InterventionNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.patch("/interventions/{encounter_id}", response_model=Intervention)
def update_intervention(encounter_id: int, body: InterventionUpdate):
    try:
        return service.update_intervention(encounter_id, body.status, body.assigned_to, body.notes)
    except service.InterventionNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except service.InvalidStatusTransition as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/interventions/{encounter_id}/history", response_model=List[HistoryItem])
def get_history(encounter_id: int):
    try:
        return service.get_history(encounter_id)
    except service.InterventionNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
