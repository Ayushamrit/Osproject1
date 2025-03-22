from algorithms.fcfs import fcfs
from algorithms.sjf import sjf
from algorithms.srtf import srtf
from algorithms.priority import priority_scheduling
from algorithms.round_robin import round_robin

class CPUScheduler:
    def __init__(self, processes, time_quantum=2):
        self.processes = processes
        self.time_quantum = time_quantum
        self.gantt_chart = []

    def run_algorithm(self, algorithm):
        if algorithm == "FCFS":
            return fcfs(self.processes)
        elif algorithm == "SJF":
            return sjf(self.processes)
        elif algorithm == "SRTF":
            return srtf(self.processes)
        elif algorithm == "Priority Scheduling":
            return priority_scheduling(self.processes)
        elif algorithm == "Round Robin":
            return round_robin(self.processes, self.time_quantum)

    def visualize(self):
        # Visualization logic remains the same
        pass