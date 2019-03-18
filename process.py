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
'''
class Process(object):
    def __init__(self, arrive, status, cpuBurstNumber, cpuBurstTimes, newName):
        self.arrivalTime = arrive
        self.state = status
        self.cpuBurstNum = cpuBurstNumber
        self.cpuBurstTimes = cpuBurstTimes
        self.completed = 0
        self.name = newName
        self.startTime = 0
    def changeState(self, status):
        self.state = status