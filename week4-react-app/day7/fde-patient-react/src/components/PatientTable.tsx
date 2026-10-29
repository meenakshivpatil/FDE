import type { Encounter } from "../types";

import PatientRow from "./PatientRow.tsx";

export default function PatientTable({ encounters }: { encounters: Encounter[] }) {     
    return (
        <div>
            <table>
                <thead>
                    <tr>
                        <th>Encounter ID</th>
                        <th>Patient Number</th>
                        <th>Age</th>
                        <th>Risk Level</th>
                    </tr>
                </thead>
                <tbody>
                    {encounters.map((encounter) => (
                        <PatientRow key={encounter.encounter_id} encounter={encounter} />
                    ))}
                </tbody>
            </table>
        </div>
    );
}