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
def event(f, eventType, queue, process, t, preempt):
    queueStr = printQueue(queue)
    if(eventType == "arrival"):
        print("time %dms: Process %s (tau %dms) arrived; added to ready queue %s" %(t, process.name, process.tau, queueStr))
        f.write("time %dms: Process %s (tau %dms) arrived; added to ready queue %s\n" %(t, process.name, process.tau, queueStr))
    elif(eventType == "arrivalPreempt"):
        print("time %dms: Process %s (tau %dms) arrived and will preempt %s %s" %(t, process.name, process.tau, preempt.name, queueStr))
        f.write("time %dms: Process %s (tau %dms) arrived and will preempt %s %s\n" %(t, process.name, process.tau, preempt.name, queueStr))
    elif(eventType == "cpuStart"):
        if(process.timeElapsed > 0):
            print("time %dms: Process %s started using the CPU with %dms remaining %s" %(t, process.name, process.cpuBurstTimes[process.completed] - process.timeElapsed, queueStr))
            f.write("time %dms: Process %s started using the CPU with %dms remaining %s\n" %(t, process.name, process.cpuBurstTimes[process.completed] - process.timeElapsed, queueStr))
        else:
            print("time %dms: Process %s started using the CPU for %dms burst %s" %(t, process.name, process.cpuBurstTimes[process.completed], queueStr))
            f.write("time %dms: Process %s started using the CPU for %dms burst %s\n" %(t, process.name, process.cpuBurstTimes[process.completed], queueStr))
    elif(eventType == "cpuFinish"):
        if(process.cpuBurstNum-process.burstComplete == 1):
            print("time %dms: Process %s completed a CPU burst; %d burst to go %s" %(t, process.name, process.cpuBurstNum-process.burstComplete, queueStr))
            f.write("time %dms: Process %s completed a CPU burst; %d burst to go %s\n" %(t, process.name, process.cpuBurstNum-process.burstComplete, queueStr))
        else:
            print("time %dms: Process %s completed a CPU burst; %d bursts to go %s" %(t, process.name, process.cpuBurstNum-process.burstComplete, queueStr))
            f.write("time %dms: Process %s completed a CPU burst; %d bursts to go %s\n" %(t, process.name, process.cpuBurstNum-process.burstComplete, queueStr))
    elif(eventType == "ioStart"):
        print("time %dms: Process %s switching out of CPU; will block on I/O until time %dms %s" %(t, process.name, t+process.cpuBurstTimes[process.completed], queueStr))
        f.write("time %dms: Process %s switching out of CPU; will block on I/O until time %dms %s\n" %(t, process.name, t+process.cpuBurstTimes[process.completed], queueStr))
    elif(eventType == "ioFinish"):
        print("time %dms: Process %s (tau %dms) completed I/O; added to ready queue %s" %(t, process.name, process.tau, queueStr))
        f.write("time %dms: Process %s (tau %dms) completed I/O; added to ready queue %s\n" %(t, process.name, process.tau, queueStr))
    elif(eventType == "ioPreempt"):
        print("time %dms: Process %s (tau %dms) completed I/O and will preempt %s %s" %(t, process.name, process.tau, preempt.name, queueStr))
        f.write("time %dms: Process %s (tau %dms) completed I/O and will preempt %s %s\n" %(t, process.name, process.tau, preempt.name, queueStr))
    elif(eventType == "terminated"):
        print("time %dms: Process %s terminated %s" %(t, process.name, queueStr))
        f.write("time %dms: Process %s terminated %s\n" %(t, process.name, queueStr))
    elif(eventType == "newTau"):
        print("time %dms: Recalculated tau = %dms for process %s %s" %(t, process.tau, process.name, queueStr))
        f.write("time %dms: Recalculated tau = %dms for process %s %s\n" %(t, process.tau, process.name, queueStr))
    elif(eventType == "preemption"):
        print("time %dms: Process %s (tau %dms) will preempt %s %s" %(t, process.name, process.tau, preempt.name, queueStr))
        f.write("time %dms: Process %s (tau %dms) will preempt %s %s\n" %(t, process.name, process.tau, preempt.name, queueStr))
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
    testFile = open("test.txt", "w")
    print("time %dms: Simulator started for SRT [Q <empty>]" % t)
    testFile.write("time %dms: Simulator started for SRT [Q <empty>]\n" % t)
    while(True):

        #End context switch out
        if(currentProcess is not None and contextSwitchOut and (t == contextSwitchOutTime + tCS/2)):
            if(currentProcess.currentPrempt == True): #CPU burst not done add back to ready queue
                for i in range(len(queue)):
                    if((currentProcess.tau - currentProcess.timeElapsed < queue[i].tau - queue[i].timeElapsed) or (currentProcess.tau - currentProcess.timeElapsed == queue[i].tau - queue[i].timeElapsed and currentProcess.name < queue[i].name)):
                        currentProcess.state = 3
                        queue.insert(i, currentProcess)
                        break
                if(currentProcess.state == 6):
                    currentProcess.state = 3
                    queue.append(currentProcess)
            elif(currentProcess.state == 6): #CPU burst done block on I/O
                currentProcess.state = 4
                currentProcess.startTime = t
            currentProcess = None
            contextSwitchOut = False
            contextSwitchOutTime = -1

        if(currentProcess is not None and currentProcess.state != 6 and currentProcess.state != 5):
            if(currentProcess.timeElapsed == currentProcess.cpuBurstTimes[currentProcess.completed] and currentProcess.state == 2): # If CPU burst or I/O block is finished
                contextSwitchOut = True
                contextSwitchOutTime = t
                currentProcess.remainingTime = 0
                currentProcess.timeElapsed = 0
                currentProcess.burstComplete += 1
                currentProcess.completed += 1
                currentProcess.currentPrempt = False
                if(currentProcess.burstComplete == currentProcess.cpuBurstNum): 
                    event(testFile, "terminated", queue, currentProcess, t, "")
                    #Process is done
                    currentProcess.state = 5
                    completed += 1
                    if(completed == len(processes)):
                        #algorithm done
                        t += tCS/2
                        break
                else:
                    if(t<1000):
                        event(testFile, "cpuFinish", queue, currentProcess, t, "")
                    currentProcess.state = 6
                    #Start I/O
                    currentProcess.tau = expAverage.nextTau(currentProcess.tau, alpha, currentProcess.cpuBurstTimes[currentProcess.completed-1])    # Recalculate tau
                    if(t<1000):
                        event(testFile, "newTau", queue, currentProcess, t, "")
                        event(testFile, "ioStart", queue, currentProcess, t, "")
            
        if(contextSwitchIn and (t == contextSwitchInTime + tCS/2)):
            # End context switch in CPU start
            currentProcess.state = 2
            if(t<1000):
                event(testFile, "cpuStart", queue, currentProcess, t, "")
            currentProcess.startTime = t
            contextSwitchIn = False
            contextSwitchInTime = -1
            if(len(queue) > 0):
                if((queue[0].tau - queue[0].timeElapsed < currentProcess.tau - currentProcess.timeElapsed) or (queue[0].tau - queue[0].timeElapsed == currentProcess.tau - currentProcess.timeElapsed and queue[0].name < currentProcess.name)):
                    if(t<1000):
                        event(testFile, "preemption", queue, queue[0], t, currentProcess)
                    currentProcess.state = 6
                    contextSwitchOut = True
                    contextSwitchOutTime = t
                    currentProcess.currentPrempt = True


        for i in processes:
            if(i.state == 4 and (t == i.startTime + i.cpuBurstTimes[i.completed]- int(tCS/2))):
                i.completed += 1
                if(currentProcess is not None and currentProcess.state == 2 and (i.tau - i.timeElapsed < currentProcess.tau - currentProcess.timeElapsed)):# or (i.tau - i.timeElapsed == currentProcess.tau - currentProcess.timeElapsed and i.name < currentProcess.name))):
                    #Preemptive I/O finish
                    i.state = 3
                    queue.insert(0,i)
                    if(t<1000):
                        event(testFile, "ioPreempt", queue, i, t, currentProcess)
                    currentProcess.currentPrempt = True
                    currentProcess.state = 6
                    contextSwitchOut = True
                    contextSwitchOutTime = t 
                else:
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
                        event(testFile, "ioFinish", queue, i, t, "")


        for i in processes:
            if(t == i.arrivalTime and i.state == 0):                                                                                            # Marks if a process arrives and checks if it can cut queue
                '''
                    Process Arrival
                '''
                if(currentProcess is not None and currentProcess.state == 2 and (i.tau - i.timeElapsed < currentProcess.tau - currentProcess.timeElapsed or (i.tau - i.timeElapsed == currentProcess.tau - currentProcess.timeElapsed and i.name < currentProcess.name))):
                    #Preemptive arrival
                    i.state = 3
                    queue.insert(0,i)
                    if(t<1000):
                        event(testFile, "arrivalPreempt", queue, i, t, currentProcess)
                    currentProcess.state = 6
                    currentProcess.currentPrempt = True
                    contextSwitchOut = True
                    contextSwitchOutTime = t
                else:
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
                        event(testFile, "arrival", queue, i, t, "")
            
        if(currentProcess is None and len(queue) > 0):
            # Start a context switch in
            currentProcess = queue.pop(0)
            currentProcess.state = 6
            contextSwitchIn = True
            contextSwitchInTime = t

        if(currentProcess is not None and currentProcess.state == 2):
            currentProcess.timeElapsed += 1
        
        t +=1

    print("time %dms: Simulator ended for SRT [Q <empty>]\n" % t)
    testFile.write("time %dms: Simulator ended for SRT [Q <empty>]\n" % t)


    averageCPUBurstTime = round(burstTimeTotal/float(totalBursts), 3)               # Average burst time for algorithm
    averageWaitTime = round(waitTimeTotal/float(totalBursts), 3)                    # Average wait time for algorithm
    averageTurnaroundTime = round(turnaroundTimeTotal/float(totalBursts), 3)        # Average turnaround time for algorithm
    return averageCPUBurstTime, averageWaitTime, averageTurnaroundTime, contextSwitchTotal, preemptionTotal