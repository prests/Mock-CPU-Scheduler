# /usr/bin/python3

'''
    Process class

    how to use in another file:
        import process

        p = process.Process(arrivalTime, status, cpuBurstTime)
'''
class Process(object):
    def __init__(self, arrive, status, cpuBurstNumber):
        self.arrivalTime = arrive
        self.state = status
        self.cpuBurstNum = cpuBurstNumber
        self.cpuBurstTimes = []
    def addBurstTime(self, burstTime):
        cpuBurstTime.append(burstTime)