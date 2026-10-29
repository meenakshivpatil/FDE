from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel

Status = Literal["PENDING_REVIEW", "ASSIGNED", "CONTACTED", "FOLLOW_UP_SCHEDULED", "CLOSED"]


class Patient(BaseModel):
    encounter_id: int
    patient_nbr: int
    risk_score: float
    risk_level: str


# patient_encounters JOIN care_interventions - one row for the update screen
class Intervention(BaseModel):
    intervention_id: int
    encounter_id: int
    patient_nbr: int
    age: str
    risk_score: Optional[int] = None
    risk_level: Optional[str] = None
    status: Status
    assigned_to: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# Body of PATCH /interventions/{encounter_id}; fields left out (None) keep their stored value
class InterventionUpdate(BaseModel):
    status: Optional[Status] = None
    assigned_to: Optional[str] = None
    notes: Optional[str] = None


class HistoryItem(BaseModel):
    history_id: int
    encounter_id: int
    old_status: str
    new_status: str
    assigned_to: Optional[str] = None
    notes: Optional[str] = None
    changed_at: datetime
