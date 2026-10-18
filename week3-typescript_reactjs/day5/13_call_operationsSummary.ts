import { toOperationsSummary, type operationsSummary } from "./06_encounterInterface.ts";

async function getOperationsSummary(): Promise<operationsSummary> {
    const response = await fetch(`http://localhost:8000/operations/summary`);
    const raw: any = await response.json();
    return toOperationsSummary(raw);
}

console.log(await getOperationsSummary());