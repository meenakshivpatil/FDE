// JavaScript for handling the search form calling the backend API and displaying results
// API http://localhost:8000/getPatients?limit=10&offset=0&min_score=0&risk_level=HIGH'


document.getElementById('searchForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const patientNumber = document.getElementById('patientNumber').value.trim();
    const riskLevel = document.getElementById('riskLevel').value;
    const riskScore = document.getElementById('RiskScore').value.trim();
    const limit = 10;
    const offset = 0;

    // Only send filters the user filled in; an empty value like "min_score=" fails with 422
    const params = new URLSearchParams({ limit: limit, offset: offset });
    if (riskScore !== '') params.append('min_score', riskScore);
    if (patientNumber !== '') params.append('patient_nbr', patientNumber);
    if (riskLevel !== '') params.append('risk_level', riskLevel);   // "All" sends nothing
    const url = `http://localhost:8000/getPatients?${params}`;

    const resultsBody = document.getElementById('resultsBody');
    const response = await fetch(url);
    const data = await response.json();
    if (!response.ok) {
        // e.g. 422 when a field is not a number; show the API's message instead of crashing
        const message = Array.isArray(data.detail) ? data.detail.map(d => `${d.loc.at(-1)}: ${d.msg}`).join('; ') : data.detail;
        resultsBody.innerHTML = `<tr><td colspan="4" class="empty">Error ${response.status}: ${message}</td></tr>`;
        return;
    }

    resultsBody.innerHTML = '';
    if (data.length === 0) {
        resultsBody.innerHTML = '<tr><td colspan="4" class="empty">No results found.</td></tr>';
    } else {
        data.forEach(patient => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><a class="encounter-link" href="update2.html?encounter_id=${patient.encounter_id}">${patient.encounter_id}</a></td>
                <td>${patient.patient_nbr}</td>
                <td>${patient.risk_score}</td>
                <td>${patient.risk_level}</td>
            `;
            resultsBody.appendChild(row);
        });
    }
});
    