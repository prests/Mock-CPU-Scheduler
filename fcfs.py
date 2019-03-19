# /usr/bin/python3
import process
import rand48
import expRandom
import math

import time


def printQueue(queue):
    if len(queue) == 0:
        return "[Q <empty>]"
    else:
        queueStr = "[Q "
        for i in range(len(queue)):
            if(i == len(queue)-1):
                queueStr += queue[i].name + "]"
            else:
                queueStr += queue[i].name + " "
        return queueStr


'''
    Output formating
'''
def event(eventType, queue, process, t):
    queueStr = printQueue(queue)
    if(eventType == "arrival"):
        print("time %dms: Process %s arrived; added to ready queue %s" %(t, process.name, queueStr))
    elif(eventType == "cpuStart"):
        print("time %dms: Process %s started using the CPU for %dms burst %s" %(t, process.name, process.cpuBurstTimes[process.completed], queueStr))
    elif(eventType == "cpuFinish"):
        print("time %dms: Process %s completed a CPU burst; %d to go %s" %(t, process.name, process.cpuBurstNum-process.completed, queueStr))
    elif(eventType == "ioStart"):
        if(process.name == "D"):
            print(len(process.cpuBurstTimes))
            print(process.cpuBurstNum)
            print(process.completed)
        print("time %dms: Process %s switching out of CPU; will block on I/O until time %dms %s" %(t, process.name, t+process.cpuBurstTimes[process.completed], queueStr))
    elif(eventType == "ioFinish"):
        print("time %dms: Process %s completed I/O; added to ready queue %s" %(t, process.name, queueStr))
    elif(eventType == "terminated"):
        print("time %dms: Process %s terminated %s" %(t, process.name, queueStr))
    else:
        print("I'm not sure how you got here...")

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
def main(processes, tCS):
    print(int(tCS/2))
    #processes = fcfsSort(processes)
    queue = []
    currentProcess = None
    t = 0
    completed = 0
    contextSwitchTime = -1
    contextSwitchIn = False
    contextSwitchOut = False
    print("time %dms: Simulator started for FCFS [Q <empty>]" % t)
    while(True):
        '''
        if t % 1000 == 0:
            for i in processes:
                print("Process %s: has %d bursts and %d completed with status %d" %(i.name, i.cpuBurstNum, i.completed, i.state))
        '''
        for i in processes:
            if(t == i.arrivalTime and i.state == 0): #Marks if a process arrives
                i.changeState(3) #Marks it as ready
                queue.append(i)
                event("arrival", queue, i, t)
        
        if(len(queue) > 0 or currentProcess is not None):
            if(contextSwitchOut and (t == contextSwitchTime + int(tCS/2))):
                contextSwitchOut = False
                currentProcess = None

            if(currentProcess is None): #Start a process if nothing running
                if(t == 306039):
                    print('asdfadsf')
                if(t > 306666 and t < 306675):
                    print(t)
                    print(contextSwitchIn)
                    print(contextSwitchOut)
                    print(contextSwitchTime)
                if(contextSwitchIn and (t == contextSwitchTime + int(tCS/2))):
                    currentProcess = queue.pop(0)
                    currentProcess.changeState(2)
                    print("Process %s: has completed %d and has %d" %(currentProcess.name, currentProcess.completed, currentProcess.cpuBurstNum))
                    event("cpuStart", queue, currentProcess, t)
                    contextSwitchIn = False
                    currentProcess.startTime = t
                else:
                    if(not contextSwitchIn and not contextSwitchOut and len(queue) > 0):
                        contextSwitchIn = True
                        contextSwitchTime = t
            else:
                if(t == currentProcess.startTime + currentProcess.cpuBurstTimes[currentProcess.completed]): #If CPU burst or I/O block is finished
                    event("cpuFinish", queue, currentProcess, t)
                    currentProcess.completed += 1
                    if(currentProcess.completed == len(currentProcess.cpuBurstTimes)): #Last process is finished
                        event("terminated", queue, currentProcess, t)
                        completed += 1
                        currentProcess.state = 5
                        currentProcess = None
                        if(completed == len(processes)):
                            t += 2
                            break
                    else:
                        event("ioStart", queue, currentProcess, t)
                        currentProcess.state = 4
                        currentProcess.startTime = t
                        currentProcess = None
                    if(t == 306039):
                        print('yo')
                    contextSwitchOut = True
                    contextSwitchTime = t

                
        for i in processes:
            if(i.state == 4 and (t == i.startTime + i.cpuBurstTimes[i.completed])): #finished I/O processes
                i.state = 3
                i.completed += 1
                queue.append(i)
                event("ioFinish", queue, i, t)
        #print(len(queue))

        t += 1
    print("time %dms: Simulator ended for FCFS [Q <empty>]" % t)