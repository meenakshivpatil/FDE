from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel

Status = Literal["PENDING_REVIEW", "ASSIGNED", "CONTACTED", "FOLLOW_UP_SCHEDULED", "CLOSED"]
RiskLevel = Literal["LOW", "MEDIUM", "HIGH"]


class Encounter(BaseModel):
    encounter_id: int
    patient_nbr: int
    age: str
    time_in_hospital: int
    number_inpatient: int
    number_emergency: int
    number_outpatient: int
    num_medications: int
    num_lab_procedures: int
    discharge_disposition_id: int
    admission_type_id: int
    risk_score: Optional[int] = None
    risk_level: Optional[RiskLevel] = None


class QueueItem(BaseModel):
    intervention_id: int
    encounter_id: int
    patient_nbr: int
    age: str
    risk_score: int
    risk_level: RiskLevel
    status: Status
    assigned_to: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class OperationsSummary(BaseModel):
    total_encounters: int
    high_risk: int
    medium_risk: int
    low_risk: int
    pending_interventions: int
    completed_interventions: int


class ReadmissionAnalysis(BaseModel):
    high_risk_patients: int
    high_risk_readmitted_under_30_days: int
    high_risk_readmission_rate: float


class LevelOutcome(BaseModel):
    patients: int
    readmitted_under_30_days: int
    readmission_rate: float


class ManagementDashboard(BaseModel):
    summary: OperationsSummary
    queue_size: int
    queue_share_of_encounters: float
    completion_rate: float
    interventions_by_status: dict[Status, int]
    overall_readmission_under_30_rate: float
    readmission_rate_by_risk_level: dict[RiskLevel, LevelOutcome]


class AgeBandSummary(BaseModel):
    age_band: str
    patients: int
    high_risk: int
    medium_risk: int
    low_risk: int
    readmitted_under_30_days: int
    readmission_rate: float


class HistoryItem(BaseModel):
    history_id: int
    encounter_id: int
    old_status: Status
    new_status: Status
    assigned_to: Optional[str] = None
    notes: Optional[str] = None
    changed_at: datetime


class RuleResult(BaseModel):
    rule: str
    flagged_patients: int
    flagged_readmitted_under_30_days: int
    precision: float
    recall: float
    lift: float


class RuleComparison(BaseModel):
    total_encounters: int
    base_readmission_under_30_rate: float
    rules: list[RuleResult]


class InterventionUpdate(BaseModel):
    status: Optional[Status] = None
    assigned_to: Optional[str] = None
    notes: Optional[str] = None
