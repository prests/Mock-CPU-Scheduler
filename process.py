# /usr/bin/python3  

'''
    Process class

    how to use in another file:
        import process

        p = process.Process(arrivalTime, status, cpuBurstTime)

        status:
        0 - not arrived
        1 - arrived
        2 - running
        3 - ready
        4 - blocked
        5 - Done
        6 - Switching
'''
class Process(object):
    def __init__(self, arrive, status, cpuBurstNumber, cpuBurstTimes, newName, Tau):
        self.arrivalTime = arrive             # Time the process arrives to the scheduler
        self.state = status                   # See above for states
        self.cpuBurstNum = cpuBurstNumber     # total bursts process will have (including io bursts)
        self.cpuBurstTimes = cpuBurstTimes    # list of all times the CPU and IO alternated
        self.completed = 0                    # num of bursts that the process has completed
        self.waitTime = 0                     # Wait time for a CPU Burst
        self.waitTimeStart = -1               # When the process starts waiting
        self.remainingTime = 0                # Time needed to finish a CPU burst. Used for formating
        self.name = newName                   # Name of process
        self.startTime = 0                    # Start when a process starts using the CPU
        self.tau = Tau                        # Tau value for a process. Recalculated after each burst
        self.preemptions = 0                  # Number of preemptions a CPU burst encounters
        self.currentPrempt = False            # Did the CPU burst encounter a Preemptions? This is for print outputs for submitty
        self.turnaroundStart = -1             # Sets that start value of the single CPU burst
        self.burstComplete = 0                # Number of bursts completed (for submitty got lazy)
    def changeState(self, status):
        self.state = status