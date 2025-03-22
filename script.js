function createProcessInputs() {
    const numProcesses = document.getElementById('numProcesses').value;
    const processInputsDiv = document.getElementById('processInputs');
    processInputsDiv.innerHTML = '';

    for (let i = 0; i < numProcesses; i++) {
        processInputsDiv.innerHTML += `
            <h3>Process ${i + 1}</h3>
            <label for="arrivalTime${i}">Arrival Time:</label>
            <input type="number" id="arrivalTime${i}" required>
            <label for="burstTime${i}">Burst Time:</label>
            <input type="number" id="burstTime${i}" required>
            <label for="priority${i}">Priority (if applicable):</label>
            <input type="number" id="priority${i}">
        `;
    }
}

function runSimulation() {
    const numProcesses = document.getElementById('numProcesses').value;
    const algorithm = document.getElementById('algorithm').value;
    const processes = [];

    for (let i = 0; i < numProcesses; i++) {
        const arrivalTime = parseInt(document.getElementById(`arrivalTime${i}`).value);
        const burstTime = parseInt(document.getElement