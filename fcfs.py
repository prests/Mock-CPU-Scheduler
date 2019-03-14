# /usr/bin/python3
import process
import rand48
import expRandom
import math

import time

'''
    Organize the processes based on when they arrive
'''
def fcfsSort(processes):
    for i in range(0,len(processes)):
        for j in range(0, len(processes)-i-1):
            if processes[j].arrivalTime > processes[j+1].arrivalTime:
                processes[j], processes[j+1] = processes[j+1], processes[j]
    return processes


'''
    FCFS algorithm
'''
def main(processes):
    processes = fcfsSort(processes)
    queue = []

    t = 0
    completed = 0
    cpuBurstNum = 0
    startTime = 0 #Start time of process
    print("time %dms: Algorithm FCFS starts" % t)
    while(True):
        for i in processes:
            if(t == i.arrivalTime and i.state == 0): #Marks if a process arrives
                i.changeState(3) #Marks it as ready
                print("time %dms: Process Arrived" % t)
                queue.append(i)
        
        if(len(queue) > 0):
            if(queue[0].state == 3): #Changes the first process in queue from ready to in CPU
                startTime = t
                queue[0].changeState(2)
            if(t == startTime + queue[0].cpuBurstTimes[cpuBurstNum]): #If CPU burst or I/O block is finished
                if(queue[0].state == 2):
                    print("time %dms: Process Finished using the CPU" % t)
                else:
                    print("time %dms: Process Finished using the I/O" % t)

                cpuBurstNum += 1
                if(queue[0].state == 2): #If CPU burst switch to I/O if I/O switch to CPU
                    queue[0].changeState(4)
                else:
                    queue[0].changeState(2)
                
                startTime = t

                if(cpuBurstNum == queue[0].cpuBurstNum): #Last process is finished
                    print("time %dms: Process terminates by finishing its last CPU burst" % t)
                    cpuBurstNum = 0
                    queue.pop(0)
                    completed += 1
                    t -= 1
                    if(completed == len(processes)):
                        break
                
            if(t == startTime): #Start a process
                if(queue[0].state == 2):
                    print("time %dms: Process Started using the CPU" % t)
                else:
                    print("time %dms: Process Started using the I/O" % t)
        t += 1
    print("time %dms: End of simulation" % t)