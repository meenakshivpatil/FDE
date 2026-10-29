// JavaScript for the update screen.
// Opened from search2.html as update2.html?encounter_id=...
//   GET   /interventions/{encounter_id}          -> fill the form (patient_encounters JOIN care_interventions)
//   PATCH /interventions/{encounter_id}          -> save status / assigned to / notes
//   GET   /interventions/{encounter_id}/history  -> fill the updates table

const API_BASE = 'http://localhost:8000';

// Same rule as ALLOWED_TRANSITIONS in service.py, so the user sees a message before calling the API
const ALLOWED_TRANSITIONS = {
    PENDING_REVIEW: ['ASSIGNED'],
    ASSIGNED: ['CONTACTED'],
    CONTACTED: ['FOLLOW_UP_SCHEDULED'],
    FOLLOW_UP_SCHEDULED: ['CLOSED'],
    CLOSED: ['PENDING_REVIEW'],
};

const encounterId = new URLSearchParams(window.location.search).get('encounter_id');
let current = null;   // the intervention currently shown in the form

// Calls the API and returns the JSON, or throws an Error with the API's message
async function callApi(path, options) {
    const response = await fetch(`${API_BASE}${path}`, options);
    const data = await response.json();
    if (!response.ok) {
        const message = Array.isArray(data.detail)
            ? data.detail.map(d => `${d.loc.at(-1)}: ${d.msg}`).join('; ')
            : data.detail;
        throw new Error(`${response.status}: ${message}`);
    }
    return data;
}

function showMessage(text, type) {
    const message = document.getElementById('message');
    message.textContent = text;
    message.className = `message full ${type}`;
}

function fillForm(intervention) {
    document.getElementById('encounterId').value = intervention.encounter_id;
    document.getElementById('patientNumber').value = intervention.patient_nbr;
    document.getElementById('status').value = intervention.status;
    document.getElementById('assignedTo').value = intervention.assigned_to ?? '';
    document.getElementById('notes').value = intervention.notes ?? '';
}

function fillUpdatesTable(history) {
    const updatesBody = document.getElementById('updatesBody');
    updatesBody.innerHTML = '';
    if (history.length === 0) {
        updatesBody.innerHTML = '<tr><td colspan="5" class="empty">No updates yet.</td></tr>';
        return;
    }
    // API returns newest first
    history.forEach(item => {
        const row = document.createElement('tr');
        for (const value of [new Date(item.changed_at).toLocaleString(), item.old_status,
                             item.new_status, item.assigned_to ?? '-', item.notes ?? '-']) {
            const cell = document.createElement('td');
            cell.textContent = value;   // textContent, so notes typed by users can't inject HTML
            row.appendChild(cell);
        }
        updatesBody.appendChild(row);
    });
}

function setButtonEnabled(enabled) {
    document.querySelector('#updateForm button').disabled = !enabled;
}

async function loadPage() {
    if (!encounterId) {
        showMessage('No encounter selected. Go back to Search and click an Encounter Id.', 'error');
        setButtonEnabled(false);
        return;
    }
    try {
        current = await callApi(`/interventions/${encounterId}`);
        fillForm(current);
        fillUpdatesTable(await callApi(`/interventions/${encounterId}/history`));
    } catch (error) {
        // 404 usually means a LOW risk encounter, which has no care_interventions row
        showMessage(`Could not load encounter ${encounterId}: ${error.message}`, 'error');
        document.getElementById('encounterId').value = encounterId;
        setButtonEnabled(false);
    }
}

document.getElementById('updateForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    if (!current) return;

    const status = document.getElementById('status').value;
    const assignedTo = document.getElementById('assignedTo').value.trim();
    const notes = document.getElementById('notes').value.trim();

    if (status !== current.status && !ALLOWED_TRANSITIONS[current.status].includes(status)) {
        showMessage(`Cannot move from ${current.status} to ${status}. ` +
                    `Allowed next: ${ALLOWED_TRANSITIONS[current.status].join(', ')}`, 'error');
        return;
    }

    setButtonEnabled(false);
    try {
        // Empty fields are sent as null, which keeps the stored value
        current = await callApi(`/interventions/${encounterId}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: status, assigned_to: assignedTo || null, notes: notes || null }),
        });
        fillForm(current);
        fillUpdatesTable(await callApi(`/interventions/${encounterId}/history`));
        showMessage('Intervention updated.', 'success');
    } catch (error) {
        showMessage(`Update failed: ${error.message}`, 'error');
    } finally {
        setButtonEnabled(true);
    }
});

loadPage();
