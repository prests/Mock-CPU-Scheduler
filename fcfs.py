# /usr/bin/python3
import process
import rand48
import expRandom
import math

import time

def fcfsSort(processes):
    for i in range(0,len(processes)):
        for j in range(0, len(processes)-i-1):
            if processes[j].arrivalTime > processes[j+1].arrivalTime:
                processes[j], processes[j+1] = processes[j+1], processes[j]
    return processes

def main(processes):
    processes = fcfsSort(processes)
    queue = []

    t = 0
    completed = 0
    cpuBurstNum = 0
    startTime = 0
    print("time %dms: Algorithm FCFS starts" % t)
    while(True):
        for i in processes:
            if(t == i.arrivalTime and i.state == 0):
                i.changeState(3)
                print("time %dms: Process Arrived" % t)
                queue.append(i)
        
        if(len(queue) > 0):
            if(queue[0].state == 3):
                startTime = t
                queue[0].changeState(2)
            if(t == startTime + queue[0].cpuBurstTimes[cpuBurstNum]):
                if(queue[0].state == 2):
                    print("time %dms: Process Finished using the CPU" % t)
                else:
                    print("time %dms: Process Finished using the I/O" % t)

                cpuBurstNum += 1
                if(queue[0].state == 2):
                    queue[0].changeState(4)
                else:
                    queue[0].changeState(2)
                
                startTime = t

                if(cpuBurstNum == queue[0].cpuBurstNum):
                    print("time %dms: Process terminates by finishing its last CPU burst" % t)
                    cpuBurstNum = 0
                    queue.pop(0)
                    completed += 1
                    t -= 1
                    if(completed == len(processes)):
                        break
                
            if(t == startTime):
                if(queue[0].state == 2):
                    print("time %dms: Process Started using the CPU" % t)
                else:
                    print("time %dms: Process Started using the I/O" % t)
        t += 1
    print("time %dms: End of simulation" % t)