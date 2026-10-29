import { useState } from 'react'
import PatientsTable from './PatientsTable'

export default function PatientSearchCriteria() {
  const [patientNbr, setPatientNbr] = useState('')
  const [riskLevel, setRiskLevel] = useState('')
  const [riskScore, setRiskScore] = useState('')

// search submit event handler , use useEffect to call API to get search results
//usestate to store search results
  const [patients, setPatients] = useState([]) 
  
  const handleSearch = (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault()
    // call API to get search results
    const params = new URLSearchParams()
    // Append only non-empty parameters
    if (riskScore !== '') params.append('min_score', riskScore);
    if (patientNbr !== '') params.append('patient_nbr', patientNbr);
    if (riskLevel !== '') params.append('risk_level', riskLevel);   // "All" sends nothing
    fetch(`http://localhost:8000/getPatients?${params}`)
      .then(response => response.json())
      .then(data => setPatients(data))
  }

  
  return (
    <div>
        <form onSubmit={handleSearch}>
      <label>
        Patient Number:
        <input
          type="text"
          value={patientNbr}
          onChange={(e) => setPatientNbr(e.target.value)}
        />
      </label>
      <label htmlFor="riskLevel">Risk Level</label>
                <select id="riskLevel" value={riskLevel} onChange={(e) => setRiskLevel(e.target.value)}>
                    <option value="">All</option>
                    <option value="HIGH">HIGH</option>
                    <option value="MEDIUM">MEDIUM</option>
                    <option value="LOW">LOW</option>
                </select>

                <label htmlFor="RiskScore">Risk Score</label>
                <input
                  type="text"
                  id="RiskScore"
                  name="RiskScore"
                  value={riskScore}
                  onChange={(e) => setRiskScore(e.target.value)}
                />
        <div className="form-actions">
                    <button type="submit" className="btn">Search &gt;</button>
        </div>
        </form>

        <PatientsTable patients={patients}     
        />
       
    </div>
  )
}