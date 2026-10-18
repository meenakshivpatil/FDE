import { toAgeBandSummary, type ageBandSummary } from "./06_encounterInterface.ts";

async function getAgeBandSummary(): Promise<ageBandSummary[]> {
    const response = await fetch(`http://localhost:8000/operations/age-band-summary`);
    const raw: any[] = await response.json();
    return raw.map(toAgeBandSummary);
}

console.log(await getAgeBandSummary());