def srtf(processes):
    processes.sort(key=lambda x: x[1])
    time = 0
    waiting_time = 0
    turnaround_time = 0
    gantt_chart = []
    ready_queue = []
    remaining_burst_times = {pid: bt for pid, _, bt, _ in processes}

    while remaining_burst_times:
        for pid, at, bt, pr in processes:
            if at <= time and pid in remaining_burst_times:
                ready_queue.append((pid, at, bt, pr))

        if ready_queue:
            ready_queue = [proc for proc in ready_queue if proc[0] in remaining_burst_times]
            ready_queue.sort(key=lambda x: (remaining_burst_times[x[0]], x[3]))
            pid, at, bt, pr = ready_queue[0]
            gantt_chart.append((pid, time, time + 1))
            remaining_burst_times[pid] -= 1

            if remaining_burst_times[pid] == 0:
                end_time = time + 1
                waiting_time += end_time - at - bt
                turnaround_time += end_time - at
                del remaining_burst_times[pid]
                ready_queue.remove((pid, at, bt, pr))
        else:
            gantt_chart.append((None, time, time + 1))
        time += 1

    n = len(gantt_chart)
    return waiting_time / n, turnaround_time / n, gantt_chart