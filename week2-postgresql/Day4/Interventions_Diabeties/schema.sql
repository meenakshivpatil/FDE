CREATE TABLE IF NOT EXISTS patient_encounters (
    encounter_id             BIGINT PRIMARY KEY,
    patient_nbr              BIGINT NOT NULL,
    age                      VARCHAR(10) NOT NULL,
    time_in_hospital         INTEGER NOT NULL,
    number_inpatient         INTEGER NOT NULL,
    number_emergency         INTEGER NOT NULL,
    number_outpatient        INTEGER NOT NULL,
    num_medications          INTEGER NOT NULL,
    num_lab_procedures       INTEGER NOT NULL,
    discharge_disposition_id INTEGER NOT NULL,
    admission_type_id        INTEGER NOT NULL,
    readmitted               VARCHAR(5) NOT NULL CHECK (readmitted IN ('NO', '>30', '<30')),
    risk_score               INTEGER,
    risk_level               VARCHAR(6) CHECK (risk_level IN ('LOW', 'MEDIUM', 'HIGH'))
);

CREATE INDEX IF NOT EXISTS idx_encounters_patient ON patient_encounters (patient_nbr);
CREATE INDEX IF NOT EXISTS idx_encounters_risk_level ON patient_encounters (risk_level);

CREATE TABLE IF NOT EXISTS care_interventions (
    intervention_id SERIAL PRIMARY KEY,
    encounter_id    BIGINT NOT NULL UNIQUE REFERENCES patient_encounters (encounter_id) ON DELETE CASCADE,
    status          VARCHAR(30) NOT NULL DEFAULT 'PENDING_REVIEW'
                    CHECK (status IN ('PENDING_REVIEW', 'ASSIGNED', 'CONTACTED', 'FOLLOW_UP_SCHEDULED', 'CLOSED')),
    assigned_to     VARCHAR(100),
    notes           TEXT,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS intervention_history (
    history_id   SERIAL PRIMARY KEY,
    encounter_id BIGINT NOT NULL REFERENCES patient_encounters (encounter_id) ON DELETE CASCADE,
    old_status   VARCHAR(30) NOT NULL,
    new_status   VARCHAR(30) NOT NULL,
    assigned_to  VARCHAR(100),
    notes        TEXT,
    changed_at   TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_history_encounter ON intervention_history (encounter_id);
