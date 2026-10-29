import type { Patient } from '../types_Patient'
import PatientRows from './PatientRows'

export default function PatientsTable({ patients }: { patients: Patient[] }) {
  return (
    <table>
      <thead>
        <tr>
          <th>Patient Number</th>
          <th>Risk Level</th>
          <th>Risk Score</th>
        </tr>
      </thead>
      <tbody>
        {patients.map((patient) => (
          <PatientRows key={patient.patient_nbr} Patient={patient} />
        ))}
      </tbody>
    </table>
  )
}