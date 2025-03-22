def fcfs(processes):
    processes.sort(key=lambda x: x[1])  # Sort processes by arrival time
    time, waiting_time, turnaround_time = 0, 0, 0
    gantt_chart = []

    for pid, at, bt, _ in processes:
        start = max(time, at)
        end = start + bt
        time = end
        waiting_time += start - at
        turnaround_time += end - at
        gantt_chart.append((pid, start, end))

    n = len(processes)
    return waiting_time / n, turnaround_time / n, gantt_chart