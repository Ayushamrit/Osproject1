import tkinter as tk
from tkinter import ttk
from cpu_scheduler import CPUScheduler

def run_gui():
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

        awt, tat, gantt_chart = scheduler.run_algorithm(algo)
        scheduler.gantt_chart = gantt_chart  # Store gantt chart for visualization
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