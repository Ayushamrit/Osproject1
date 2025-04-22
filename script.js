let processes = [];
let processId = 1;

document.getElementById('process-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const arrival = parseInt(document.getElementById('arrival-time').value);
    const burst = parseInt(document.getElementById('burst-time').value);
    const priority = document.getElementById('priority').value ? parseInt(document.getElementById('priority').value) : null;
    processes.push({ id: processId++, arrival, burst, priority, remaining: burst });
    renderProcessList();
    this.reset();
});

document.getElementById('clear-processes').addEventListener('click', function () {
    processes = [];
    processId = 1;
    renderProcessList();
});

document.getElementById('algorithm-select').addEventListener('change', function () {
    if (this.value === 'rr') {
        document.getElementById('quantum-input').style.display = 'block';
    } else {
        document.getElementById('quantum-input').style.display = 'none';
    }
});

document.getElementById('simulate-btn').addEventListener('click', function () {
    const algorithm = document.getElementById('algorithm-select').value;
    const quantum = parseInt(document.getElementById('quantum').value) || 1;
    simulate(algorithm, quantum);
});

function renderProcessList() {
    const list = document.getElementById('process-list');
    list.innerHTML = '';
    processes.forEach(p => {
        list.innerHTML += `
            <li>
                P${p.id} - Arrival: ${p.arrival}, Burst: ${p.burst}, Priority: ${p.priority ?? '-'}
                <button onclick="editProcess(${p.id})">Edit</button>
                <button onclick="removeProcess(${p.id})">Remove</button>
            </li>
        `;
    });
}

function editProcess(id) {
    const process = processes.find(p => p.id === id);
    if (process) {
        document.getElementById('arrival-time').value = process.arrival;
        document.getElementById('burst-time').value = process.burst;
        document.getElementById('priority').value = process.priority ?? '';
        removeProcess(id); // Remove the process so it can be re-added with updated values
    }
}

function removeProcess(id) {
    processes = processes.filter(p => p.id !== id);
    renderProcessList();
}

function simulate(algorithm, quantum) {
    let resultProcesses = JSON.parse(JSON.stringify(processes));
    resultProcesses.sort((a, b) => a.arrival - b.arrival);
    let time = 0;
    let completed = 0;
    let gantt = [];
    let processStatus = []; // Array to store process status at each time step

    if (algorithm === 'fcfs') {
        resultProcesses.forEach(p => {
            if (time < p.arrival) {
                gantt.push({ id: 'idle', start: time, end: p.arrival });
                processStatus.push({ range: `${time}-${p.arrival}`, process: 'Idle' });
                time = p.arrival;
            }
            gantt.push({ id: p.id, start: time, end: time + p.burst });
            processStatus.push({ range: `${time}-${time + p.burst}`, process: `P${p.id}` });
            p.waitingTime = time - p.arrival;
            p.turnaroundTime = p.waitingTime + p.burst;
            time += p.burst;
        });
    } else if (algorithm === 'sjf') {
        while (completed < resultProcesses.length) {
            let readyQueue = resultProcesses.filter(p => p.arrival <= time && !p.completed).sort((a, b) => a.burst - b.burst);
            if (readyQueue.length === 0) {
                let nextArrival = resultProcesses.find(p => !p.completed)?.arrival || time;
                gantt.push({ id: 'idle', start: time, end: nextArrival });
                processStatus.push({ range: `${time}-${nextArrival}`, process: 'Idle' });
                time = nextArrival;
                continue;
            }
            let p = readyQueue[0];
            gantt.push({ id: p.id, start: time, end: time + p.burst });
            processStatus.push({ range: `${time}-${time + p.burst}`, process: `P${p.id}` });
            p.waitingTime = time - p.arrival;
            p.turnaroundTime = p.waitingTime + p.burst;
            time += p.burst;
            p.completed = true;
            completed++;
        }
    } else if (algorithm === 'srtf') {
        while (completed < resultProcesses.length) {
            let readyQueue = resultProcesses.filter(p => p.arrival <= time && p.remaining > 0).sort((a, b) => a.remaining - b.remaining);
            if (readyQueue.length === 0) {
                let nextArrival = resultProcesses.find(p => p.remaining > 0)?.arrival || time;
                gantt.push({ id: 'idle', start: time, end: nextArrival });
                processStatus.push({ range: `${time}-${nextArrival}`, process: 'Idle' });
                time = nextArrival;
                continue;
            }
            let p = readyQueue[0];
            gantt.push({ id: p.id, start: time, end: time + 1 });
            processStatus.push({ range: `${time}-${time + 1}`, process: `P${p.id}` });
            p.remaining -= 1;
            time += 1;
            if (p.remaining === 0) {
                p.completed = true;
                p.waitingTime = time - p.arrival - p.burst;
                p.turnaroundTime = p.waitingTime + p.burst;
                completed++;
            }
        }
    } else if (algorithm === 'priority') {
        while (completed < resultProcesses.length) {
            let readyQueue = resultProcesses.filter(p => p.arrival <= time && !p.completed).sort((a, b) => a.priority - b.priority);
            if (readyQueue.length === 0) {
                let nextArrival = resultProcesses.find(p => !p.completed)?.arrival || time;
                gantt.push({ id: 'idle', start: time, end: nextArrival });
                processStatus.push({ range: `${time}-${nextArrival}`, process: 'Idle' });
                time = nextArrival;
                continue;
            }
            let p = readyQueue[0];
            gantt.push({ id: p.id, start: time, end: time + p.burst });
            processStatus.push({ range: `${time}-${time + p.burst}`, process: `P${p.id}` });
            p.waitingTime = time - p.arrival;
            p.turnaroundTime = p.waitingTime + p.burst;
            time += p.burst;
            p.completed = true;
            completed++;
        }
    } else if (algorithm === 'priority-pre') {
        while (completed < resultProcesses.length) {
            let readyQueue = resultProcesses.filter(p => p.arrival <= time && p.remaining > 0).sort((a, b) => a.priority - b.priority);
            if (readyQueue.length === 0) {
                let nextArrival = resultProcesses.find(p => p.remaining > 0)?.arrival || time;
                gantt.push({ id: 'idle', start: time, end: nextArrival });
                processStatus.push({ range: `${time}-${nextArrival}`, process: 'Idle' });
                time = nextArrival;
                continue;
            }
            let p = readyQueue[0];
            gantt.push({ id: p.id, start: time, end: time + 1 });
            processStatus.push({ range: `${time}-${time + 1}`, process: `P${p.id}` });
            p.remaining -= 1;
            time += 1;
            if (p.remaining === 0) {
                p.completed = true;
                p.waitingTime = time - p.arrival - p.burst;
                p.turnaroundTime = p.waitingTime + p.burst;
                completed++;
            }
        }
    } else if (algorithm === 'rr') {
        let queue = [];
        let idx = 0;
        while (completed < resultProcesses.length) {
            queue = resultProcesses.filter(p => p.arrival <= time && p.remaining > 0);
            if (queue.length === 0) {
                let nextArrival = resultProcesses.find(p => p.remaining > 0)?.arrival || time;
                gantt.push({ id: 'idle', start: time, end: nextArrival });
                processStatus.push({ range: `${time}-${nextArrival}`, process: 'Idle' });
                time = nextArrival;
                continue;
            }
            let p = queue[idx % queue.length];
            let execTime = Math.min(p.remaining, quantum);
            gantt.push({ id: p.id, start: time, end: time + execTime });
            processStatus.push({ range: `${time}-${time + execTime}`, process: `P${p.id}` });
            p.remaining -= execTime;
            time += execTime;
            if (p.remaining === 0) {
                p.completed = true;
                p.waitingTime = time - p.arrival - p.burst;
                p.turnaroundTime = p.waitingTime + p.burst;
                completed++;
            }
            idx++;
        }
    }

    drawGanttChart(gantt);
    renderProcessStatusTable(processStatus);
    showResults(resultProcesses);
}

function renderProcessStatusTable(status) {
    const table = document.getElementById('process-status-table');
    table.innerHTML = `
        <tr>
            <th>Time Range</th>
            <th>Process</th>
        </tr>
    `;
    status.forEach(entry => {
        table.innerHTML += `
            <tr>
                <td>${entry.range}</td>
                <td>${entry.process}</td>
            </tr>
        `;
    });
}

function drawGanttChart(gantt) {
    const canvas = document.getElementById('gantt-chart');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const scale = 20;
    let x = 0;
    gantt.forEach(item => {
        ctx.fillStyle = item.id === 'idle' ? '#d3d3d3' : `hsl(${item.id * 60}, 70%, 70%)`;
        let width = (item.end - item.start) * scale;
        ctx.fillRect(x, 30, width, 40);
        ctx.strokeRect(x, 30, width, 40);
        ctx.fillStyle = "black";
        ctx.fillText(item.id === 'idle' ? 'Idle' : `P${item.id}`, x + width / 2 - 10, 55);
        ctx.fillText(`${item.start}`, x, 80);
        x += width;
    });
    ctx.fillText(`${gantt[gantt.length - 1].end}`, x, 80);
}

function showResults(procs) {
    const resultsDiv = document.getElementById('results');
    let avgWaiting = procs.reduce((sum, p) => sum + p.waitingTime, 0) / procs.length;
    let avgTurnaround = procs.reduce((sum, p) => sum + p.turnaroundTime, 0) / procs.length;

    resultsDiv.innerHTML = `
        <h3>Results</h3>
        <p>Average Waiting Time: ${avgWaiting.toFixed(2)}</p>
        <p>Average Turnaround Time: ${avgTurnaround.toFixed(2)}</p>
    `;
}
