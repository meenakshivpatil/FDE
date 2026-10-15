from psycopg2.extras import RealDictCursor, execute_values

from database import get_db_connection

BATCH_SIZE = 5000


def fetch_scoring_inputs() -> list[tuple]:
    """Return only the columns the risk rule needs. `readmitted` is deliberately excluded."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT encounter_id, number_inpatient, number_emergency, number_outpatient, "
                "time_in_hospital, num_medications FROM patient_encounters ORDER BY encounter_id"
            )
            return cur.fetchall()
    finally:
        conn.close()


_ENCOUNTER_COLUMNS = (
    "encounter_id, patient_nbr, age, time_in_hospital, number_inpatient, number_emergency, "
    "number_outpatient, num_medications, num_lab_procedures, discharge_disposition_id, "
    "admission_type_id, risk_score, risk_level "
)


def fetch_encounters(limit: int, offset: int, risk_level: str | None = None) -> list[dict]:
    """Paged encounter list. `readmitted` is not exposed."""
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT " + _ENCOUNTER_COLUMNS + "FROM patient_encounters "
                "WHERE (%s::varchar IS NULL OR risk_level = %s) ORDER BY encounter_id LIMIT %s OFFSET %s",
                (risk_level, risk_level, limit, offset),
            )
            return cur.fetchall()
    finally:
        conn.close()


def fetch_encounter(encounter_id: int) -> dict | None:
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT " + _ENCOUNTER_COLUMNS + "FROM patient_encounters WHERE encounter_id = %s",
                (encounter_id,),
            )
            return cur.fetchone()
    finally:
        conn.close()


def fetch_summary_counts() -> dict:
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT COUNT(*) AS total_encounters, "
                "COUNT(*) FILTER (WHERE risk_level = 'HIGH') AS high_risk, "
                "COUNT(*) FILTER (WHERE risk_level = 'MEDIUM') AS medium_risk, "
                "COUNT(*) FILTER (WHERE risk_level = 'LOW') AS low_risk FROM patient_encounters"
            )
            counts = cur.fetchone()
            cur.execute(
                "SELECT COUNT(*) FILTER (WHERE status <> 'CLOSED') AS pending_interventions, "
                "COUNT(*) FILTER (WHERE status = 'CLOSED') AS completed_interventions FROM care_interventions"
            )
            counts.update(cur.fetchone())
            return dict(counts)
    finally:
        conn.close()


def fetch_status_counts() -> dict:
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT status, COUNT(*) FROM care_interventions GROUP BY status")
            return {status: n for status, n in cur.fetchall()}
    finally:
        conn.close()


def fetch_readmission_by_level() -> list[dict]:
    """Evaluation only: runs after scoring and reads the stored risk_level, never feeds it."""
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT risk_level, COUNT(*) AS patients, "
                "COUNT(*) FILTER (WHERE readmitted = '<30') AS readmitted_under_30_days "
                "FROM patient_encounters WHERE risk_level IS NOT NULL GROUP BY risk_level"
            )
            return cur.fetchall()
    finally:
        conn.close()


def create_queue_rows() -> int:
    """Insert a PENDING_REVIEW row for every MEDIUM/HIGH encounter. Existing rows are left untouched."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO care_interventions (encounter_id) "
                "SELECT encounter_id FROM patient_encounters WHERE risk_level IN ('MEDIUM', 'HIGH') "
                "ON CONFLICT (encounter_id) DO NOTHING"
            )
            inserted = cur.rowcount
        conn.commit()
        return inserted
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


_INTERVENTION_SELECT = (
    "SELECT i.intervention_id, i.encounter_id, e.patient_nbr, e.age, e.risk_score, e.risk_level, "
    "i.status, i.assigned_to, i.notes, i.created_at, i.updated_at "
    "FROM care_interventions i JOIN patient_encounters e ON e.encounter_id = i.encounter_id "
)


def fetch_queue(levels: list[str], limit: int | None = 100, offset: int = 0, min_score: int = 0) -> list[dict]:
    """Queue ordered by risk_score DESC, then encounter_id. limit=None returns all rows (CSV export).
    `readmitted` is not selected."""
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                _INTERVENTION_SELECT + "WHERE e.risk_level = ANY(%s) AND e.risk_score >= %s "
                "ORDER BY e.risk_score DESC, i.encounter_id LIMIT %s OFFSET %s",
                (levels, min_score, limit, offset),
            )
            return cur.fetchall()
    finally:
        conn.close()


def fetch_intervention(encounter_id: int) -> dict | None:
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(_INTERVENTION_SELECT + "WHERE i.encounter_id = %s", (encounter_id,))
            return cur.fetchone()
    finally:
        conn.close()


def update_intervention(encounter_id: int, status: str | None, assigned_to: str | None,
                        notes: str | None) -> dict | None:
    """Update only the supplied fields; None keeps the stored value. Every update is also
    appended to intervention_history in the same transaction."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT status FROM care_interventions WHERE encounter_id = %s FOR UPDATE",
                        (encounter_id,))
            row = cur.fetchone()
            if row is None:
                return None
            old_status = row[0]
            cur.execute(
                "UPDATE care_interventions SET status = COALESCE(%s, status), "
                "assigned_to = COALESCE(%s, assigned_to), notes = COALESCE(%s, notes), updated_at = NOW() "
                "WHERE encounter_id = %s "
                "RETURNING status, assigned_to, notes",
                (status, assigned_to, notes, encounter_id),
            )
            new_status, new_owner, new_notes = cur.fetchone()
            cur.execute(
                "INSERT INTO intervention_history (encounter_id, old_status, new_status, assigned_to, notes) "
                "VALUES (%s, %s, %s, %s, %s)",
                (encounter_id, old_status, new_status, new_owner, new_notes),
            )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    return fetch_intervention(encounter_id)


def fetch_history(encounter_id: int) -> list[dict]:
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT history_id, encounter_id, old_status, new_status, assigned_to, notes, changed_at "
                "FROM intervention_history WHERE encounter_id = %s ORDER BY history_id",
                (encounter_id,),
            )
            return cur.fetchall()
    finally:
        conn.close()


def fetch_age_band_summary() -> list[dict]:
    """Evaluation view: uses readmitted after scoring, never feeds scoring."""
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT age AS age_band, COUNT(*) AS patients, "
                "COUNT(*) FILTER (WHERE risk_level = 'HIGH') AS high_risk, "
                "COUNT(*) FILTER (WHERE risk_level = 'MEDIUM') AS medium_risk, "
                "COUNT(*) FILTER (WHERE risk_level = 'LOW') AS low_risk, "
                "COUNT(*) FILTER (WHERE readmitted = '<30') AS readmitted_under_30_days "
                "FROM patient_encounters GROUP BY age ORDER BY age"
            )
            return cur.fetchall()
    finally:
        conn.close()


def fetch_comparison_rows() -> list[tuple]:
    """(risk_level, inpatient, emergency, outpatient, readmitted<30?) for evaluating rule sets."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT risk_level, number_inpatient, number_emergency, number_outpatient, "
                "(readmitted = '<30') FROM patient_encounters"
            )
            return cur.fetchall()
    finally:
        conn.close()


def bulk_update_risk(scores: list[tuple[int, int, str]]) -> int:
    """Persist (encounter_id, risk_score, risk_level) tuples in one transaction."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            execute_values(
                cur,
                "UPDATE patient_encounters AS e SET risk_score = v.risk_score, risk_level = v.risk_level "
                "FROM (VALUES %s) AS v (encounter_id, risk_score, risk_level) "
                "WHERE e.encounter_id = v.encounter_id",
                scores,
                template="(%s::bigint, %s::integer, %s::varchar)",
                page_size=BATCH_SIZE,
            )
        conn.commit()
        return len(scores)
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
