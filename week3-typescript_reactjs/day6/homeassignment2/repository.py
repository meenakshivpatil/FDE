#open database connection and fetch patient encounters
from psycopg2.extras import RealDictCursor, execute_values

from database import get_db_connection

BATCH_SIZE = 5000

def get_Patients(limit, offset, min_score, patient_nbr, risk_level):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = "SELECT encounter_id, patient_nbr, risk_score, risk_level FROM patient_encounters WHERE risk_score >= %s"
    params = [min_score]
    if patient_nbr is not None:
        query += " AND patient_nbr = %s"
        params.append(patient_nbr)
    if risk_level is not None:
        query += " AND risk_level = %s"
        params.append(risk_level)
    query += " ORDER BY encounter_id LIMIT %s OFFSET %s"
    params.extend([limit, offset])
    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


# Join of patient_encounters and care_interventions for one encounter (None if it has no intervention)
INTERVENTION_SELECT = (
    "SELECT i.intervention_id, e.encounter_id, e.patient_nbr, e.age, e.risk_score, e.risk_level, "
    "i.status, i.assigned_to, i.notes, i.created_at, i.updated_at "
    "FROM patient_encounters e JOIN care_interventions i ON i.encounter_id = e.encounter_id "
    "WHERE e.encounter_id = %s"
)


def get_intervention(encounter_id):
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(INTERVENTION_SELECT, (encounter_id,))
            return cursor.fetchone()
    finally:
        conn.close()


def update_intervention(encounter_id, status, assigned_to, notes):
    """Update care_interventions and log the change in intervention_history in one transaction.
    None keeps the stored value."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT status FROM care_interventions WHERE encounter_id = %s FOR UPDATE",
                           (encounter_id,))
            old_status = cursor.fetchone()[0]
            cursor.execute(
                "UPDATE care_interventions SET status = COALESCE(%s, status), "
                "assigned_to = COALESCE(%s, assigned_to), notes = COALESCE(%s, notes), updated_at = NOW() "
                "WHERE encounter_id = %s RETURNING status, assigned_to, notes",
                (status, assigned_to, notes, encounter_id),
            )
            new_status, new_assigned_to, new_notes = cursor.fetchone()
            cursor.execute(
                "INSERT INTO intervention_history (encounter_id, old_status, new_status, assigned_to, notes) "
                "VALUES (%s, %s, %s, %s, %s)",
                (encounter_id, old_status, new_status, new_assigned_to, new_notes),
            )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    return get_intervention(encounter_id)


def get_history(encounter_id):
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT history_id, encounter_id, old_status, new_status, assigned_to, notes, changed_at "
                "FROM intervention_history WHERE encounter_id = %s ORDER BY changed_at DESC, history_id DESC",
                (encounter_id,),
            )
            return cursor.fetchall()
    finally:
        conn.close()