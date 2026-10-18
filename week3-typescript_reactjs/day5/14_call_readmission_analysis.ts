import { toReadmissionAnalysis, type readmissionAnalysis } from "./06_encounterInterface.ts";

async function getReadmissionAnalysis(): Promise<readmissionAnalysis> {
    const response = await fetch(`http://localhost:8000/operations/readmission-analysis`);
    const raw: any = await response.json();
    return toReadmissionAnalysis(raw);
}

console.log(await getReadmissionAnalysis());