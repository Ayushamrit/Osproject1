import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

# CPU Scheduling Algorithms
class CPUScheduler:
    def __init__(self, processes, time_quantum=2):
        self.processes = processes
        self.time_quantum = time_quantum
        self.gantt_chart = []

    def fcfs(self):
        self.processes.sort(key=lambda x: x[1])  # Sort processes by arrival time
        time, waiting_time, turnaround_time = 0, 0, 0
        self.gantt_chart = []

        for pid, at, bt, _ in self.processes:
            start = max(time, at)
            end = start + bt
            time = end
            waiting_time += start - at
            turnaround_time += end - at
            self.gantt_chart.append((pid, start, end))

        n = len(self.processes)
        return waiting_time / n, turnaround_time / n

    def sjf(self):
        self.processes.sort(key=lambda x: (x[1], x[2]))  # Sort by arrival time, then burst time
        time, waiting_time, turnaround_time = 0, 0, 0
        self.gantt_chart = []
        ready_queue = []

        while self.processes or ready_queue:
            while self.processes and self.processes[0][1] <= time:
                ready_queue.append(self.processes.pop(0))

            ready_queue.sort(key=lambda x: x[2])  # Sort by burst time

            if ready_queue:
                pid, at, bt, _ = ready_queue.pop(0)
                start, end = time, time + bt
                time = end
                waiting_time += start - at
                turnaround_time += end - at
                self.gantt_chart.append((pid, start, end))
            else:
                time += 1

        n = len(self.gantt_chart)
        return waiting_time / n, turnaround_time / n

    def srtf(self):
        # Sort processes by arrival time
        self.processes.sort(key=lambda x: x[1])
        time = 0
        waiting_time = 0
        turnaround_time = 0
        self.gantt_chart = []
        ready_queue = []
        remaining_burst_times = {pid: bt for pid, _, bt, _ in self.processes}

        while remaining_burst_times:
            # Add processes that have arrived to the ready queue
            for pid, at, bt, pr in self.processes:
                if at <= time and pid in remaining_burst_times:
                    ready_queue.append((pid, at, bt, pr))

            if ready_queue:
                # Filter ready_queue to only include processes still in remaining_burst_times
                ready_queue = [proc for proc in ready_queue if proc[0] in remaining_burst_times]

                # Sort the ready queue by remaining burst time and then by priority
                ready_queue.sort(key=lambda x: (remaining_burst_times[x[0]], x[3]))  # Sort by remaining time, then priority
                pid, at, bt, pr = ready_queue[0]  # Get the process with the shortest remaining time
                self.gantt_chart.append((pid, time, time + 1))  # Execute for 1 time unit
                remaining_burst_times[pid] -= 1  # Decrease remaining time

                if remaining_burst_times[pid] == 0:
                    # Process is finished
                    end_time = time + 1
                    waiting_time += end_time - at - bt
                    turnaround_time += end_time - at
                    del remaining_burst_times[pid]  # Remove from remaining burst times
                    ready_queue.remove((pid, at, bt, pr))  # Remove from ready queue
            else:
                # No process is ready, increment time
                self.gantt_chart.append((None, time, time + 1))  # Idle time
            time += 1

        n = len(self.gantt_chart)
        return waiting_time / n, turnaround_time / n

    def priority_scheduling(self):
        self.processes.sort(key=lambda x: (x[1], x[3]))  # Sort by arrival time, then priority
        time, waiting_time, turnaround_time = 0, 0, 0
        self.gantt_chart = []

        for pid, at, bt, pr in self.processes:
            start = max(time, at)
            end = start + bt
            time = end
            waiting_time += start - at
            turnaround_time += end - at
            self.gantt_chart.append((pid, start, end))

        n = len(self.processes)
        return waiting_time / n, turnaround_time / n

    def round_robin(self):
        queue = self.processes[:]
        queue.sort(key=lambda x: x[1])  # Sort by arrival time
        time, waiting_time, turnaround_time = 0, 0, 0
        self.gantt_chart = []

        while queue:
            pid, at, bt, pr = queue.pop(0)
            start = max(time, at)
            exec_time = min(bt, self.time_quantum)
            end = start + exec_time
            time = end
            bt -= exec_time
            self.gantt_chart.append((pid, start, end))

            if bt > 0:
                queue.append((pid, time, bt, pr))  # Re-add process if it needs more time
            else:
                waiting_time += start - at
                turnaround_time += end - at

        n = len(self.gantt_chart)
        return waiting_time / n, turnaround_time / n

    def visualize(self):
        fig, ax = plt.subplots(figsize=(10, 3))
        yticks, labels = [], []

        for i, (pid, start, end) in enumerate(self.gantt_chart):
            if pid is not None:  # Only plot if there's a valid process ID
                ax.barh(y=i, width=end - start, left=start, color='purple', edgecolor='teal')
                ax.text((start + end) / 2, i, f'P{pid}', ha='center', va='center', fontsize=10, color='white')
                yticks.append(i)
                labels.append(f'P{pid}')
            else:
                # Handle idle time
                ax.barh(y=i, width=end - start, left=start, color='lightgray', edgecolor='teal')

        ax.set_yticks(yticks)
        ax.set_yticklabels(labels)
        ax.set_xlabel("Time")
        ax.set_title("Gantt Chart")
        plt.show()

# GUI for User Input
def run_simulation():
    processes = []
    for row in table.get_children():
        pid, at, bt, priority = table.item(row)['values']
        processes.append((int(pid), int(at), int(bt), int(priority)))

    if not processes:
        return

    time_quantum = int(entry_tq.get()) if entry_tq.get() else 2

    scheduler = CPUScheduler(processes, time_quantum)
    algo = algorithm_choice.get()

    if algo == "FCFS":
        awt, tat = scheduler.fcfs()
    elif algo == "SJF":
        awt, tat = scheduler.sjf()
    elif algo == "SRTF":
        awt, tat = scheduler.srtf()  # Call the new SRTF method
    elif algo == "Priority Scheduling":
        awt, tat = scheduler.priority_scheduling()
    elif algo == "Round Robin":
        awt, tat = scheduler.round_robin()

    scheduler.visualize()
    result_label.config(text=f"Average Waiting Time: {awt:.2f}, Average Turnaround Time: {tat:.2f}")

def add_process():
    pid = len(table.get_children()) + 1
    at = int(entry_at.get())
    bt = int(entry_bt.get())
    priority = int(entry_priority.get())
    table.insert("", "end", values=(pid, at, bt, priority))

def clear_processes():
    table.delete(*table.get_children())

# GUI Setup
root = tk.Tk()
root.title("CPU Scheduling Simulator")

frame = tk.Frame(root)
frame.pack()

algorithm_choice = ttk.Combobox(frame, values=["FCFS", "SJF", "SRTF", "Priority Scheduling", "Round Robin"])
algorithm_choice.set("FCFS")
algorithm_choice.pack()

table = ttk.Treeview(frame, columns=("PID", "Arrival Time", "Burst Time", "Priority"), show="headings")
for col in table['columns']:
    table.heading(col, text=col)
    table.column(col, width=100)
table.pack()

entry_at = tk.Entry(frame)
entry_bt = tk.Entry(frame)
entry_priority = tk.Entry(frame)

for widget, text in zip([entry_at, entry_bt, entry_priority], ["Arrival Time", "Burst Time", "Priority"]):
    tk.Label(frame, text=text).pack()
    widget.pack()

tk.Label(frame, text="Time Quantum (for Round Robin)").pack()
entry_tq = tk.Entry(frame)
entry_tq.pack()

tk.Button(frame, text="Add Process", command=add_process).pack()
tk.Button(frame, text="Clear", command=clear_processes).pack()
tk.Button(frame, text="Run Simulation", command=run_simulation).pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()