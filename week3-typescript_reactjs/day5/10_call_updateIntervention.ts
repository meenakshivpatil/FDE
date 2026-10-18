import { toCareQueue, type CareQueue } from "./06_encounterInterface.ts";

async function updateIntervention(interventionId: number, updates: Partial<CareQueue>): Promise<CareQueue> {
    const response = await fetch(`http://localhost:8000/interventions/${interventionId}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(updates)
    });
    if (!response.ok) {
        throw new Error(`${response.status}: ${await response.text()}`);
    }
    return toCareQueue(await response.json());
}

//example usage
const updatedCareQueue = await updateIntervention(7284348, { status: "CONTACTED", assigned_to: "B team", notes: "Contact patient today" });
console.log(updatedCareQueue);
