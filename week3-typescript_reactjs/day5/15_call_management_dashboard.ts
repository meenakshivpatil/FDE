import { toManagementDashboard, type managementDashboard } from "./06_encounterInterface.ts";

async function getManagementDashboard(): Promise<managementDashboard> {
    const response = await fetch(`http://localhost:8000/management/dashboard`);
    const raw: any = await response.json();
    return toManagementDashboard(raw);
}

console.log(await getManagementDashboard());