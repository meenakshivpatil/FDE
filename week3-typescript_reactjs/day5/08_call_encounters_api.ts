import { toEncounter, type Encounter } from "./06_encounterInterface.ts";

async function getEncounters(limit: number, offset: number): Promise<Encounter[]> {
    const response = await fetch(`http://localhost:8000/encounters/?limit=${limit}&offset=${offset}`);
    const raw: any[] = await response.json();
    return raw.map(toEncounter);
}

console.log(await getEncounters(10, 0));
