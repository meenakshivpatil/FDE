import repository

# (field, threshold, points) from the prototype prioritization rule
RISK_RULES = [
    ("number_inpatient", 3, 3),
    ("number_emergency", 2, 2),
    ("number_outpatient", 3, 1),
    ("time_in_hospital", 7, 1),
    ("num_medications", 20, 1),
]


STATUS_FLOW = ["PENDING_REVIEW", "ASSIGNED", "CONTACTED", "FOLLOW_UP_SCHEDULED", "CLOSED"]
# Forward one step at a time; CLOSED may be reopened to PENDING_REVIEW.
ALLOWED_TRANSITIONS = {
    status: {STATUS_FLOW[i + 1]} for i, status in enumerate(STATUS_FLOW[:-1])
}
ALLOWED_TRANSITIONS["CLOSED"] = {"PENDING_REVIEW"}


class InterventionNotFound(Exception):
    pass


class InvalidStatusTransition(Exception):
    pass


class EncounterNotFound(Exception):
    pass


def list_encounters(limit: int = 100, offset: int = 0, risk_level: str | None = None) -> list[dict]:
    return repository.fetch_encounters(limit, offset, risk_level)


def get_encounter(encounter_id: int) -> dict:
    row = repository.fetch_encounter(encounter_id)
    if row is None:
        raise EncounterNotFound(f"Encounter {encounter_id} not found")
    return row


def _rate(part: int, whole: int) -> float:
    return round(100 * part / whole, 2) if whole else 0.0


def get_operations_summary() -> dict:
    return repository.fetch_summary_counts()


def _analysis_by_level() -> dict:
    by_level = {r["risk_level"]: r for r in repository.fetch_readmission_by_level()}
    return {
        level: {
            "patients": by_level.get(level, {}).get("patients", 0),
            "readmitted_under_30_days": by_level.get(level, {}).get("readmitted_under_30_days", 0),
        }
        for level in ("HIGH", "MEDIUM", "LOW")
    }


def get_readmission_analysis() -> dict:
    high = _analysis_by_level()["HIGH"]
    return {
        "high_risk_patients": high["patients"],
        "high_risk_readmitted_under_30_days": high["readmitted_under_30_days"],
        "high_risk_readmission_rate": _rate(high["readmitted_under_30_days"], high["patients"]),
    }


def get_management_dashboard() -> dict:
    summary = repository.fetch_summary_counts()
    levels = _analysis_by_level()
    queue_size = summary["high_risk"] + summary["medium_risk"]
    total_interventions = summary["pending_interventions"] + summary["completed_interventions"]
    status_counts = repository.fetch_status_counts()
    overall_readmitted = sum(v["readmitted_under_30_days"] for v in levels.values())
    return {
        "summary": summary,
        "queue_size": queue_size,
        "queue_share_of_encounters": _rate(queue_size, summary["total_encounters"]),
        "completion_rate": _rate(summary["completed_interventions"], total_interventions),
        "interventions_by_status": {s: status_counts.get(s, 0) for s in STATUS_FLOW},
        "overall_readmission_under_30_rate": _rate(overall_readmitted, summary["total_encounters"]),
        "readmission_rate_by_risk_level": {
            level: {**v, "readmission_rate": _rate(v["readmitted_under_30_days"], v["patients"])}
            for level, v in levels.items()
        },
    }


def build_queue() -> dict:
    return {"created": repository.create_queue_rows()}


def get_care_queue(limit: int | None = 100, offset: int = 0, min_score: int = 0) -> list[dict]:
    return repository.fetch_queue(["MEDIUM", "HIGH"], limit, offset, min_score)


def get_high_risk_queue(limit: int | None = 100, offset: int = 0, min_score: int = 0) -> list[dict]:
    return repository.fetch_queue(["HIGH"], limit, offset, min_score)


CSV_COLUMNS = ["encounter_id", "patient_nbr", "age", "risk_score", "risk_level", "status",
               "assigned_to", "notes", "updated_at"]


def export_queue_csv(min_score: int = 0) -> str:
    import csv
    import io
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=CSV_COLUMNS, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(repository.fetch_queue(["MEDIUM", "HIGH"], None, 0, min_score))
    return buf.getvalue()


def get_intervention_history(encounter_id: int) -> list[dict]:
    get_intervention(encounter_id)
    return repository.fetch_history(encounter_id)


def get_age_band_summary() -> list[dict]:
    result = []
    for r in repository.fetch_age_band_summary():
        result.append({**r, "readmission_rate": _rate(r["readmitted_under_30_days"], r["patients"])})
    return result


# Alternative rule: simple weighted prior-visit count, flag when >= ALT_THRESHOLD.
# Ignores stay length and medication count, unlike the primary rule.
ALT_THRESHOLD = 4


def alt_score(inpatient: int, emergency: int, outpatient: int) -> int:
    return 2 * inpatient + emergency + outpatient


def _evaluate(name: str, flagged: int, flagged_readmitted: int, total: int, total_readmitted: int) -> dict:
    base_rate = _rate(total_readmitted, total)
    precision = _rate(flagged_readmitted, flagged)
    return {
        "rule": name,
        "flagged_patients": flagged,
        "flagged_readmitted_under_30_days": flagged_readmitted,
        "precision": precision,
        "recall": _rate(flagged_readmitted, total_readmitted),
        "lift": round(precision / base_rate, 2) if base_rate else 0.0,
    }


def compare_rules() -> dict:
    """Evaluation only (uses readmitted after scoring). Compares the primary rule's queue
    (MEDIUM+HIGH) and HIGH group with the alternative rule at the same data."""
    total = total_readmitted = 0
    counts = {"queue": [0, 0], "high": [0, 0], "alt": [0, 0]}
    for level, inpatient, emergency, outpatient, readmitted in repository.fetch_comparison_rows():
        total += 1
        total_readmitted += readmitted
        if level in ("MEDIUM", "HIGH"):
            counts["queue"][0] += 1
            counts["queue"][1] += readmitted
        if level == "HIGH":
            counts["high"][0] += 1
            counts["high"][1] += readmitted
        if alt_score(inpatient, emergency, outpatient) >= ALT_THRESHOLD:
            counts["alt"][0] += 1
            counts["alt"][1] += readmitted
    return {
        "total_encounters": total,
        "base_readmission_under_30_rate": _rate(total_readmitted, total),
        "rules": [
            _evaluate("primary (MEDIUM+HIGH, score>=3)", *counts["queue"], total, total_readmitted),
            _evaluate("primary (HIGH only, score>=5)", *counts["high"], total, total_readmitted),
            _evaluate(f"alternative (2*inpatient+emergency+outpatient >= {ALT_THRESHOLD})",
                      *counts["alt"], total, total_readmitted),
        ],
    }


def get_intervention(encounter_id: int) -> dict:
    row = repository.fetch_intervention(encounter_id)
    if row is None:
        raise InterventionNotFound(f"No intervention found for encounter {encounter_id}")
    return row


def update_intervention(encounter_id: int, status: str | None = None,
                        assigned_to: str | None = None, notes: str | None = None) -> dict:
    current = get_intervention(encounter_id)
    if status is not None:
        if status not in STATUS_FLOW:
            raise InvalidStatusTransition(f"Unknown status '{status}'. Allowed: {STATUS_FLOW}")
        if status != current["status"] and status not in ALLOWED_TRANSITIONS[current["status"]]:
            allowed = sorted(ALLOWED_TRANSITIONS[current["status"]])
            raise InvalidStatusTransition(
                f"Cannot move from {current['status']} to {status}. Allowed next: {allowed}"
            )
    return repository.update_intervention(encounter_id, status, assigned_to, notes)


def risk_level_for(score: int) -> str:
    if score >= 5:
        return "HIGH"
    if score >= 3:
        return "MEDIUM"
    return "LOW"


def calculate_risk(number_inpatient: int, number_emergency: int, number_outpatient: int,
                   time_in_hospital: int, num_medications: int) -> tuple[int, str]:
    values = {
        "number_inpatient": number_inpatient,
        "number_emergency": number_emergency,
        "number_outpatient": number_outpatient,
        "time_in_hospital": time_in_hospital,
        "num_medications": num_medications,
    }
    score = sum(points for field, threshold, points in RISK_RULES if values[field] >= threshold)
    return score, risk_level_for(score)


def score_all_encounters() -> dict:
    scores = []
    counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
    for encounter_id, inpatient, emergency, outpatient, days, meds in repository.fetch_scoring_inputs():
        score, level = calculate_risk(inpatient, emergency, outpatient, days, meds)
        scores.append((encounter_id, score, level))
        counts[level] += 1
    updated = repository.bulk_update_risk(scores)
    return {"scored": updated, **counts}
