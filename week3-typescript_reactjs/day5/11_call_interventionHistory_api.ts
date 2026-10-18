import { toInterventionHistory, type InterventionHistory } from "./06_encounterInterface.ts";

async function getInterventionHistory(interventionId: number): Promise<InterventionHistory[]> {
    const response = await fetch(`http://localhost:8000/interventions/${interventionId}/history`);
    const raw: any[] = await response.json();
    return raw.map(toInterventionHistory);
}

console.log(await getInterventionHistory(7284348));