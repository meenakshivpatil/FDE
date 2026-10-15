# Intervention Queue

Learning prototype. Not clinically validated and must not be used for real patient care decisions.

## Business problem and users

**Problem:** which recently discharged diabetes patients should the care-management team review first?
**Primary user:** a care-management coordinator with limited capacity. **Secondary user:** a manager who wants operational metrics.
**Decision improved:** who gets reviewed first, and whether follow-up work is actually progressing.

## Assumptions

- Source data is the UCI "Diabetes 130-US hospitals" CSV (`diabetic_data.csv`). Only 12 relevant columns are loaded.
- Rows with missing (`?`) or invalid values are skipped; the first row per `encounter_id` is kept.
- `number_inpatient / emergency / outpatient` are counts of the patient's prior-year visits before the encounter.
- Rule thresholds and points are a prototype heuristic, not clinically derived.
- `readmitted` is never used for scoring, only for after-the-fact evaluation.
- "Pending" interventions = queue rows not CLOSED; "completed" = CLOSED.
- No authentication; all users see all patients (acceptable only for a learning prototype).

## Architecture

```
CSV -> data_loader.py -> PostgreSQL (patient_encounters)
                              | run_scoring.py -> service.py (rules) -> repository.py
                              | run_queue.py   -> care_interventions
Client -> main.py (routes, HTTP errors) -> service.py (rules, workflow) -> repository.py (SQL) -> PostgreSQL
```

- `main.py`: routes and HTTP error mapping. `models.py`: request/response models.
- `service.py`: risk rules, status workflow, metrics. `repository.py`: all parameterized SQL.
- `database.py`: connection from `DATABASE_URL`. `schema.sql`: tables.

## API list

| Method | Path | Purpose |
|---|---|---|
| GET | `/encounters` | List encounters (paged, optional `risk_level`) |
| GET | `/encounters/{encounter_id}` | One encounter |
| GET | `/care-queue` | MEDIUM + HIGH queue (paged, `min_score`) |
| GET | `/care-queue/high` | HIGH queue (paged, `min_score`) |
| GET | `/care-queue/export` | Queue as CSV |
| PATCH | `/interventions/{encounter_id}` | Update status / owner / notes |
| GET | `/interventions/{encounter_id}/history` | Status change history |
| GET | `/operations/summary` | Operational counts |
| GET | `/operations/age-band-summary` | Risk and readmission by age band |
| GET | `/operations/rule-comparison` | Primary vs alternative rule |
| GET | `/operations/readmission-analysis` | HIGH-risk vs historical <30-day readmission |
| GET | `/management/dashboard` | Executive summary |

## Run from scratch

```powershell
pip install -r requirements.txt
python data_loader.py
python run_scoring.py
python run_queue.py
uvicorn main:app --reload
python validate_all.py        # runs all phase validators (needs the server on API_BASE, default :8000)
```

Swagger UI: http://127.0.0.1:8000/docs






Reflections:

1. What business problem did you solve?

care managers cannot review every discharged diabetes patient, so the app ranks encounters and turns the top ones into a trackable work queue.

2. Who is the primary user?

the care-management coordinator (managers use the metrics endpoints).

3. What decision does your application improve?

which patient to review first, and monitoring how follow-up is progressing.


4. What did the dataset prove?

historically, the rule's HIGH group was readmitted within 30 days at 28.58%, MEDIUM at 21.60% and LOW at 10.03% (overall 11.16%). The rule ranks patients in the right direction. It does not prove the readmissions were preventable, or that an intervention would change the outcome.

5. What assumptions did you make?

listed in the Assumptions section (prior-year utilization counts, heuristic thresholds, row cleaning, pending/completed definition, no auth).


6. What must the hospital validate before this could become a real product?

 clinical validity of the rule, which readmissions are preventable, cost of an intervention versus a readmission, care-team capacity, fairness across age and other groups, privacy/consent and access control, and fit with the real discharge workflow. Also check for repeat patients: the same patient can appear in many encounters.

7. Would you use rules, traditional ML, LLM, or another approach next — and why?

keep the rules as an explainable baseline, then compare against a traditional ML model (e.g. logistic regression or gradient boosting on tabular data) evaluated on leave one out stategy, patient-level split, since the data is structured and small enough that an LLM adds little value. An LLM would only help later for summarizing free-text notes, which this dataset doesn't have.

