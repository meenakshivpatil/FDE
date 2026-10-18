import { toCareQueue, type CareQueue} from "./06_encounterInterface.ts";


async function getCareQueue(limit: number, offset: number, min_score: number): Promise<CareQueue[]> {
    const response = await fetch(`http://localhost:8000/care-queue/?limit=${limit}&offset=${offset}&min_score=${min_score}`);
    const raw: any[] = await response.json();
    return raw.map(toCareQueue);
}

console.log(await getCareQueue(10, 0,8));
