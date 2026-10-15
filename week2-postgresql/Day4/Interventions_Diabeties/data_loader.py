"""Phase 1 loader: create the schema and load the selected CSV columns into PostgreSQL.

Each run truncates patient_encounters (and, via CASCADE, care_interventions) and reloads it.
"""
import csv
from pathlib import Path

from psycopg2.extras import execute_values

from database import get_db_connection

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "diabetic_data.csv"
SCHEMA_FILE = BASE_DIR / "schema.sql"

INT_COLUMNS = [
    "encounter_id", "patient_nbr", "time_in_hospital", "number_inpatient",
    "number_emergency", "number_outpatient", "num_medications",
    "num_lab_procedures", "discharge_disposition_id", "admission_type_id",
]
TEXT_COLUMNS = ["age", "readmitted"]
COLUMNS = ["encounter_id", "patient_nbr", "age", "time_in_hospital", "number_inpatient",
           "number_emergency", "number_outpatient", "num_medications", "num_lab_procedures",
           "discharge_disposition_id", "admission_type_id", "readmitted"]
MISSING = {"", "?"}
BATCH_SIZE = 5000


def clean_row(raw: dict):
    """Return a tuple in COLUMNS order, or None if any required field is missing or invalid."""
    values = {}
    for col in INT_COLUMNS:
        value = (raw.get(col) or "").strip()
        if value in MISSING:
            return None
        try:
            values[col] = int(value)
        except ValueError:
            return None
    for col in TEXT_COLUMNS:
        value = (raw.get(col) or "").strip()
        if value in MISSING:
            return None
        values[col] = value
    return tuple(values[col] for col in COLUMNS)


def read_rows(path: Path):
    stats = {"read": 0, "skipped_invalid": 0, "skipped_duplicate": 0}
    seen = set()
    rows = []
    with open(path, newline="", encoding="utf-8") as file:
        for raw in csv.DictReader(file):
            stats["read"] += 1
            row = clean_row(raw)
            if row is None:
                stats["skipped_invalid"] += 1
                continue
            if row[0] in seen:
                stats["skipped_duplicate"] += 1
                continue
            seen.add(row[0])
            rows.append(row)
    return rows, stats


def load_data():
    rows, stats = read_rows(CSV_FILE)
    insert_sql = (
        f"INSERT INTO patient_encounters ({', '.join(COLUMNS)}) VALUES %s "
        "ON CONFLICT (encounter_id) DO NOTHING"
    )
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(SCHEMA_FILE.read_text(encoding="utf-8"))
            cur.execute("TRUNCATE TABLE patient_encounters CASCADE;")
            execute_values(cur, insert_sql, rows, page_size=BATCH_SIZE)
            cur.execute("SELECT COUNT(*) FROM patient_encounters;")
            stats["loaded"] = cur.fetchone()[0]
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    return stats


if __name__ == "__main__":
    result = load_data()
    print("Load complete:")
    for key, value in result.items():
        print(f"  {key}: {value}")
