import repository
from models import HistoryItem, Intervention, Patient

# Status moves forward one step at a time; CLOSED may be reopened to PENDING_REVIEW
ALLOWED_TRANSITIONS = {
    "PENDING_REVIEW": ["ASSIGNED"],
    "ASSIGNED": ["CONTACTED"],
    "CONTACTED": ["FOLLOW_UP_SCHEDULED"],
    "FOLLOW_UP_SCHEDULED": ["CLOSED"],
    "CLOSED": ["PENDING_REVIEW"],
}


class InterventionNotFound(Exception):
    pass


class InvalidStatusTransition(Exception):
    pass


def get_Patients(limit, offset, min_score, patient_nbr, risk_level):
    patient_encounters = repository.get_Patients(limit, offset, min_score, patient_nbr, risk_level)
    return [Patient(**encounter) for encounter in patient_encounters]


def get_intervention(encounter_id):
    row = repository.get_intervention(encounter_id)
    if row is None:
        raise InterventionNotFound(f"No care intervention found for encounter {encounter_id}")
    return Intervention(**row)


def update_intervention(encounter_id, status, assigned_to, notes):
    current = get_intervention(encounter_id)
    if status is not None and status != current.status and status not in ALLOWED_TRANSITIONS[current.status]:
        raise InvalidStatusTransition(
            f"Cannot move from {current.status} to {status}. "
            f"Allowed next: {', '.join(ALLOWED_TRANSITIONS[current.status])}"
        )
    return Intervention(**repository.update_intervention(encounter_id, status, assigned_to, notes))


def get_history(encounter_id):
    get_intervention(encounter_id)   # 404 if the encounter has no intervention
    return [HistoryItem(**row) for row in repository.get_history(encounter_id)]
