def sjf(processes):
    processes.sort(key=lambda x: (x[1], x[2]))  # Sort by arrival time, then burst time
    time, waiting_time, turnaround_time = 0, 0, 0
    gantt_chart = []
    ready_queue = []

    while processes or ready_queue:
        while processes and processes[0][1] <= time:
            ready_queue.append(processes.pop(0))

        ready_queue.sort(key=lambda x: x[2])  # Sort by burst time

        if ready_queue:
            pid, at, bt, _ = ready_queue.pop(0)
            start, end = time, time + bt
            time = end
            waiting_time += start - at
            turnaround_time += end - at
            gantt_chart.append((pid, start, end))
        else:
            time += 1

    n = len(gantt_chart)
    return waiting_time / n, turnaround_time / n, gantt_chart