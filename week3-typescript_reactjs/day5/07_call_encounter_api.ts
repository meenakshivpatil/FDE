import type { Encounter } from "./06_encounterInterface.ts";
import { toEncounter } from "./06_encounterInterface.ts";

async function getEncounter(encounterId: number): Promise<Encounter>{
    const response = await fetch(`http://localhost:8000/encounters/${encounterId}`);

    const data: Encounter = await response.json();
    const e: Encounter = toEncounter(data);
    
    return e;
}

const e: Encounter = await getEncounter(12522);
console.log(e);
