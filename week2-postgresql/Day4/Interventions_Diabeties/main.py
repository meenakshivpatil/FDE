from typing import Optional

from fastapi import FastAPI, HTTPException, Query, Response

import service
from models import (AgeBandSummary, Encounter, HistoryItem, InterventionUpdate, ManagementDashboard,
                    OperationsSummary, QueueItem, ReadmissionAnalysis, RiskLevel, RuleComparison)

app = FastAPI(title="Diabetes Readmission Intervention Queue")


@app.get("/encounters", response_model=list[Encounter])
def list_encounters(limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0),
                    risk_level: Optional[RiskLevel] = None):
    return service.list_encounters(limit, offset, risk_level)


@app.get("/encounters/{encounter_id}", response_model=Encounter)
def get_encounter(encounter_id: int):
    try:
        return service.get_encounter(encounter_id)
    except service.EncounterNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/care-queue", response_model=list[QueueItem])
def care_queue(limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0),
               min_score: int = Query(0, ge=0, le=8)):
    return service.get_care_queue(limit, offset, min_score)


@app.get("/care-queue/export")
def care_queue_export(min_score: int = Query(0, ge=0, le=8)):
    return Response(
        content=service.export_queue_csv(min_score),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=care_queue.csv"},
    )


@app.get("/care-queue/high", response_model=list[QueueItem])
def care_queue_high(limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0),
                    min_score: int = Query(0, ge=0, le=8)):
    return service.get_high_risk_queue(limit, offset, min_score)


@app.get("/interventions/{encounter_id}/history", response_model=list[HistoryItem])
def intervention_history(encounter_id: int):
    try:
        return service.get_intervention_history(encounter_id)
    except service.InterventionNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/operations/age-band-summary", response_model=list[AgeBandSummary])
def age_band_summary():
    return service.get_age_band_summary()


@app.get("/operations/rule-comparison", response_model=RuleComparison)
def rule_comparison():
    return service.compare_rules()


@app.get("/operations/summary", response_model=OperationsSummary)
def operations_summary():
    return service.get_operations_summary()


@app.get("/operations/readmission-analysis", response_model=ReadmissionAnalysis)
def readmission_analysis():
    return service.get_readmission_analysis()


@app.get("/management/dashboard", response_model=ManagementDashboard)
def management_dashboard():
    return service.get_management_dashboard()


@app.patch("/interventions/{encounter_id}", response_model=QueueItem)
def update_intervention(encounter_id: int, body: InterventionUpdate):
    try:
        return service.update_intervention(encounter_id, body.status, body.assigned_to, body.notes)
    except service.InterventionNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except service.InvalidStatusTransition as e:
        raise HTTPException(status_code=400, detail=str(e))
