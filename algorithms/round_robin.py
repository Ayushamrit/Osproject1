def round_robin(processes, time_quantum):
    queue = processes[:]
    queue.sort(key=lambda x: x[1])  # Sort by arrival time
    time, waiting_time, turnaround_time = 0, 0, 0
    gantt_chart = []

    while queue:
        pid, at, bt, pr = queue.pop(0)
        start = max(time, at)
        exec_time = min(bt, time_quantum)
        end = start + exec_time
        time = end
        bt -= exec_time
        gantt_chart.append((pid, start, end))

        if bt > 0:
            queue.append((pid, time, bt, pr))  # Re-add process if it needs more time
        else:
            waiting_time += start - at
            turnaround_time += end - at

    n = len(gantt_chart)
    return waiting_time / n, turnaround_time / n, gantt_chart