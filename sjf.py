#!/usr/bin/python3
import expAverage

'''
    Prints queue for submitty
'''
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
    Output formating for submitty
'''
def event(eventType, queue, process, t, preempt):
    queueStr = printQueue(queue)
    if(eventType == "arrival"):
        print("time %dms: Process %s (tau %dms) arrived; added to ready queue %s" %(t, process.name, process.tau, queueStr))
    elif(eventType == "arrivalPreempt"):
        print("time %dms: Process %s (tau %dms) arrived and will preempt %s %s" %(t, process.name, process.tau, preempt.name, queueStr))
    elif(eventType == "cpuStart"):
        if(process.timeElapsed > 0):
            print("time %dms: Process %s started using the CPU with %dms remaining %s" %(t, process.name, process.cpuBurstTimes[process.completed] - process.timeElapsed, queueStr))
        else:
            print("time %dms: Process %s started using the CPU for %dms burst %s" %(t, process.name, process.cpuBurstTimes[process.completed], queueStr))
    elif(eventType == "cpuFinish"):
        if(process.cpuBurstNum-process.burstComplete == 1):
            print("time %dms: Process %s completed a CPU burst; %d burst to go %s" %(t, process.name, process.cpuBurstNum-process.burstComplete, queueStr))
        else:
            print("time %dms: Process %s completed a CPU burst; %d bursts to go %s" %(t, process.name, process.cpuBurstNum-process.burstComplete, queueStr))
    elif(eventType == "ioStart"):
        print("time %dms: Process %s switching out of CPU; will block on I/O until time %dms %s" %(t, process.name, t+process.cpuBurstTimes[process.completed], queueStr))
    elif(eventType == "ioFinish"):
        print("time %dms: Process %s (tau %dms) completed I/O; added to ready queue %s" %(t, process.name, process.tau, queueStr))
    elif(eventType == "ioPreempt"):
        print("time %dms: Process %s (tau %dms) completed I/O and will preempt %s %s" %(t, process.name, process.tau, preempt.name, queueStr))
    elif(eventType == "terminated"):
        print("time %dms: Process %s terminated %s" %(t, process.name, queueStr))
    elif(eventType == "newTau"):
        print("time %dms: Recalculated tau = %dms for process %s %s" %(t, process.tau, process.name, queueStr))
    elif(eventType == "preemption"):
        print("time %dms: Process %s (tau %dms) will preempt %s %s" %(t, process.name, process.tau, preempt.name, queueStr))
    else:
        print("I'm not sure how you got here...")

'''
    SRT algorithm
'''
def main(processes, tCS, alpha):
    burstTimeTotal = 0                              # Total burst time for all processes
    waitTimeTotal = 0                               # Total wait time for all processes
    turnaroundTimeTotal = 0                         # Total turnaround time for all processes
    contextSwitchTotal = 0                          # Total number of context switches when running algorithm
    preemptionTotal = 0                             # Total number of preemptions in algorithm
    
    totalBursts = 0                                 # The total number of CPU bursts a process has
    for i in processes:
        totalBursts += i.cpuBurstNum
    
    queue = []                                      # Ready queue
    currentProcess = None                           # The current process running
    
    t = 0                                           # Current time
    completed = 0                                   # How many processes have been completed
    contextSwitchInTime = -1                          # Time when a context switch is starting
    contextSwitchIn = False                         # Is the process context switching in? 
    contextSwitchOut = False                        # Is the process context switching out?
    contextSwitchOutTime = -1
    print("time %dms: Simulator started for SJF [Q <empty>]" % t)
    while(True):

        #End context switch out
        if(currentProcess is not None and contextSwitchOut and (t == contextSwitchOutTime + tCS/2)):
            if(currentProcess.state == 6): #CPU burst done block on I/O
                currentProcess.state = 4
                currentProcess.startTime = t
                turnaroundTimeTotal += (t - currentProcess.turnaroundStart)
                currentProcess.turnaroundStart = -1
            if(currentProcess.state == 5):
                turnaroundTimeTotal += (t - currentProcess.turnaroundStart)
            currentProcess = None
            contextSwitchOut = False
            contextSwitchOutTime = -1

        if(currentProcess is not None and currentProcess.state != 6 and currentProcess.state != 5):
            if(currentProcess.timeElapsed == currentProcess.cpuBurstTimes[currentProcess.completed] and currentProcess.state == 2): # If CPU burst or I/O block is finished
                contextSwitchOut = True
                contextSwitchOutTime = t
                currentProcess.remainingTime = 0
                currentProcess.timeElapsed = 0
                burstTimeTotal += currentProcess.cpuBurstTimes[currentProcess.completed]
                currentProcess.burstComplete += 1
                currentProcess.completed += 1
                currentProcess.currentPrempt = False

                waitTimeTotal += currentProcess.waitTime
                currentProcess.waitTime = 0

                if(currentProcess.burstComplete == currentProcess.cpuBurstNum): 
                    event("terminated", queue, currentProcess, t, "")
                    #Process is done
                    currentProcess.state = 5
                    completed += 1
                    if(completed == len(processes)):
                        #algorithm done
                        t += tCS/2
                        break
                else:
                    if(t<1000):
                        event("cpuFinish", queue, currentProcess, t, "")
                    currentProcess.state = 6
                    #Start I/O
                    currentProcess.tau = expAverage.nextTau(currentProcess.tau, alpha, currentProcess.cpuBurstTimes[currentProcess.completed-1])    # Recalculate tau
                    if(t<1000):
                        event("newTau", queue, currentProcess, t, "")
                        event("ioStart", queue, currentProcess, t, "")
            
        if(contextSwitchIn and (t == contextSwitchInTime + tCS/2)):
            # End context switch in CPU start
            currentProcess.state = 2
            if(t<1000):
                event("cpuStart", queue, currentProcess, t, "")
            currentProcess.startTime = t
            contextSwitchIn = False
            contextSwitchInTime = -1
            contextSwitchTotal += 1


        for i in processes:
            if(i.state == 4 and (t == i.startTime + i.cpuBurstTimes[i.completed]- int(tCS/2))):
                i.completed += 1
                if(i.turnaroundStart == -1):
                    i.turnaroundStart = t
                #I/O finish
                for j in range(len(queue)):
                    if((i.tau - i.timeElapsed < queue[j].tau - queue[j].timeElapsed) or (i.tau - i.timeElapsed == queue[j].tau - queue[j].timeElapsed and i.name < queue[j].name)):
                        i.state = 3
                        queue.insert(j, i)
                        break
                if(i.state == 4):
                    i.state = 3
                    queue.append(i)
                if(t<1000):
                    event("ioFinish", queue, i, t, "")


        for i in processes:
            if(t == i.arrivalTime and i.state == 0):                                                                                            # Marks if a process arrives and checks if it can cut queue
                '''
                    Process Arrival
                '''
                #arrival
                for j in range(len(queue)):
                    if((i.tau - i.timeElapsed < queue[j].tau - queue[j].timeElapsed) or (i.tau - i.timeElapsed == queue[j].tau - queue[j].timeElapsed and i.name < queue[j].name)):
                        i.state = 3
                        queue.insert(j, i)
                        break
                if(i.state == 0):
                    i.state = 3
                    queue.append(i)
                if(t<1000):
                    event("arrival", queue, i, t, "")
            
        if(currentProcess is None and len(queue) > 0):
            # Start a context switch in
            currentProcess = queue.pop(0)
            currentProcess.state = 6
            contextSwitchIn = True
            contextSwitchInTime = t
            if(i.turnaroundStart == -1):
                i.turnaroundStart = t

        if(currentProcess is not None and currentProcess.state == 2):
            currentProcess.timeElapsed += 1
        
        for i in processes:
            if(i.state == 3):
                i.waitTime += 1

        t +=1

    print("time %dms: Simulator ended for SJF [Q <empty>]\n" % t)


    averageCPUBurstTime = round(burstTimeTotal/float(totalBursts), 3)               # Average burst time for algorithm
    averageWaitTime = round(waitTimeTotal/float(totalBursts), 3)                    # Average wait time for algorithm
    averageTurnaroundTime = round(turnaroundTimeTotal/float(totalBursts), 3)        # Average turnaround time for algorithm
    return averageCPUBurstTime, averageWaitTime, averageTurnaroundTime, contextSwitchTotal