//create interface Encounter - data structure (4-5 column)
//encounter_id, patient_id, risk_score, risk_level

export interface Encounter {
    encounter_id: number;
    patient_nbr: number;
    risk_score: number;
    risk_level: string;
}

export interface CareQueue {
    intervention_id: number;
    encounter_id: number;
    patient_nbr: number;
    age: string;
    risk_score: number;
    risk_level: string;
    status: string;
    assigned_to: string | null;
    notes: string | null;
    created_at: string;
    updated_at: string;
}

export interface InterventionHistory{
    history_id: number;
    encounter_id: number;
    old_status: string;
    new_status: string;
    assigned_to: string | null;
    notes: string | null;
    changed_at: string;
}
export interface ageBandSummary {
    age_band: string;
    patients: number;
    high_risk: number;
    medium_risk: number;
    low_risk: number;
    readmitted_under_30_days: number;
    readmission_rate: number;
}

export interface operationsSummary {
    total_encounters: number;
    high_risk: number;
    medium_risk: number;
    low_risk: number;
    pending_interventions: number;
    completed_interventions: number;
}

export interface readmissionAnalysis {
    high_risk_patients: number;
    high_risk_readmitted_under_30_days: number;
    high_risk_readmission_rate: number;
}

export interface managementDashboard{
    summary: {
    total_encounters: number,
    high_risk: number,
    medium_risk: number,
    low_risk: number,
    pending_interventions: number,
    completed_interventions: number,
  },
  queue_size: number,
  queue_share_of_encounters: number,
  completion_rate: number,
  interventions_by_status: {
    PENDING_REVIEW: number,
    ASSIGNED: number,
    CONTACTED: number,
    FOLLOW_UP_SCHEDULED: number,
    CLOSED: number,
  },
  overall_readmission_under_30_rate: number,
  readmission_rate_by_risk_level: {
    HIGH: {
      patients: number,
      readmitted_under_30_days: number,
      readmission_rate: number,
    },
    MEDIUM: {
      patients: number,
      readmitted_under_30_days: number,
      readmission_rate: number,
    },
    LOW: {
      patients: number,
      readmitted_under_30_days: number,
      readmission_rate: number,
    }
  }
}

export function toManagementDashboard(raw: any): managementDashboard {
    return {
        summary: {
            total_encounters: raw.summary.total_encounters,
            high_risk: raw.summary.high_risk,
            medium_risk: raw.summary.medium_risk,
            low_risk: raw.summary.low_risk,
            pending_interventions: raw.summary.pending_interventions,
            completed_interventions: raw.summary.completed_interventions,
        },
        queue_size: raw.queue_size,
        queue_share_of_encounters: raw.queue_share_of_encounters,
        completion_rate: raw.completion_rate,
        interventions_by_status: {
            PENDING_REVIEW: raw.interventions_by_status.PENDING_REVIEW,
            ASSIGNED: raw.interventions_by_status.ASSIGNED,
            CONTACTED: raw.interventions_by_status.CONTACTED,
            FOLLOW_UP_SCHEDULED: raw.interventions_by_status.FOLLOW_UP_SCHEDULED,
            CLOSED: raw.interventions_by_status.CLOSED,
        },
        overall_readmission_under_30_rate: raw.overall_readmission_under_30_rate,
        readmission_rate_by_risk_level: {
            HIGH: {
                patients: raw.readmission_rate_by_risk_level.HIGH.patients,
                readmitted_under_30_days: raw.readmission_rate_by_risk_level.HIGH.readmitted_under_30_days,
                readmission_rate: raw.readmission_rate_by_risk_level.HIGH.readmission_rate,
            },
            MEDIUM: {
                patients: raw.readmission_rate_by_risk_level.MEDIUM.patients,
                readmitted_under_30_days: raw.readmission_rate_by_risk_level.MEDIUM.readmitted_under_30_days,
                readmission_rate: raw.readmission_rate_by_risk_level.MEDIUM.readmission_rate,
            },
            LOW: {
                patients: raw.readmission_rate_by_risk_level.LOW.patients,
                readmitted_under_30_days: raw.readmission_rate_by_risk_level.LOW.readmitted_under_30_days,
                readmission_rate: raw.readmission_rate_by_risk_level.LOW.readmission_rate,
            },
        },
    };
}

export function toReadmissionAnalysis(raw: any): readmissionAnalysis {
    return {
        high_risk_patients: raw.high_risk_patients,
        high_risk_readmitted_under_30_days: raw.high_risk_readmitted_under_30_days,
        high_risk_readmission_rate: raw.high_risk_readmission_rate,
    };
}

export function toOperationsSummary(raw: any): operationsSummary {
    return {
        total_encounters: raw.total_encounters,
        high_risk: raw.high_risk,
        medium_risk: raw.medium_risk,
        low_risk: raw.low_risk,
        pending_interventions: raw.pending_interventions,
        completed_interventions: raw.completed_interventions,
    };
}


export function toAgeBandSummary(raw: any): ageBandSummary {
    return {
        age_band: raw.age_band,
        patients: raw.patients,
        high_risk: raw.high_risk,
        medium_risk: raw.medium_risk,
        low_risk: raw.low_risk,
        readmitted_under_30_days: raw.readmitted_under_30_days,
        readmission_rate: raw.readmission_rate,
    };
}
export function toInterventionHistory(raw: any): InterventionHistory {
    return {
        history_id: raw.history_id,
        encounter_id: raw.encounter_id,
        old_status: raw.old_status,
        new_status: raw.new_status,
        assigned_to: raw.assigned_to,
        notes: raw.notes,
        changed_at: raw.changed_at,
    };
}

export function toCareQueue(raw: any): CareQueue {
    return {
        intervention_id: raw.intervention_id,
        encounter_id: raw.encounter_id,
        patient_nbr: raw.patient_nbr,
        age: raw.age,
        risk_score: raw.risk_score,
        risk_level: raw.risk_level,
        status: raw.status,
        assigned_to: raw.assigned_to,
        notes: raw.notes,
        created_at: raw.created_at,
        updated_at: raw.updated_at,
    };
}

export function toEncounter(raw: any): Encounter {
    return {
        encounter_id: raw.encounter_id,
        patient_nbr: raw.patient_nbr,
        risk_score: raw.risk_score,
        risk_level: raw.risk_level,
    };
}
//example usage
const encounter1: Encounter = {
    encounter_id: 2,
    patient_nbr: 456,
    risk_score: 45,
    risk_level: "Medium"
};
const encounter2: Encounter = {
    encounter_id: 1,
    patient_nbr: 123,
    risk_score: 85,
    risk_level: "High"
};

const encounters: Encounter[] = [encounter1, encounter2];

//console.log(encounters);


