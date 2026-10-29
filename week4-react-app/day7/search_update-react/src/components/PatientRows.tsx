import type { Patient } from '../types_Patient'


export default function PatientRows({ Patient }: { Patient: Patient }) {
  return (
    <tr>
      <td>{Patient.patient_nbr}</td>
      <td>{Patient.risk_level}</td>
      <td>{Patient.risk_score}</td>
    </tr>
  )
}
