# Mock-CPU-Scheduler

The Mock CPU Scheduler is a project for RPI's Operating Systems class. The project is created in Python3 and simulates various schenarios for how processes are scheduled by a CPU.

## Types of schedules Supported
1. Shortest Job First (SJF) - Non-preemptive scheduler where jobs are queued in priority based on which is the shortest job
2. Shortest Remaining Time (SRT) - Preemptive version of (SJF) where jobs with the shortest remaining time are prioritized
3. First Come, First Served (FCFS) - Non-preemptive algorithm where whichever job is first run and the queue is organized as such
4. Round Robin (RR) - A fixed amount of time is provided where a process is allowed to run for that amount of time. Preemption occurs if a process isn't finished in the fixed amount of time.

## How to run project

python3 main.py s lamda uB n tCS alpha tS rr

s - Seed for random number generator
lamda - Exponential distribution for interarrival times
uB - Upper bound for valid pseudo-random numbers
n - Number of processes to simulate
tCS - Time (milliseconds) to perform a context switch
alpha - Constant used in exponential averaging
tS - Time slice for a process in Round Robin algorithm
rr - Determine if processes are added to beginning or end of queue on arrivale (BEGINNING/END with END being default)
