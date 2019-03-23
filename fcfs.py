# /usr/bin/python3

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
        print("time %dms: Process %s switching out of CPU; will block on I/O until time %dms %s" %(t, process.name, t+process.cpuBurstTimes[process.completed], queueStr))
    elif(eventType == "ioFinish"):
        print("time %dms: Process %s completed I/O; added to ready queue %s" %(t, process.name, queueStr))
    elif(eventType == "terminated"):
        print("time %dms: Process %s terminated %s" %(t, process.name, queueStr))
    else:
        print("I'm not sure how you got here...")


'''
    FCFS algorithm
'''
def main(processes, tCS):
    burstTimeTotal = 0 #Total burst time for all processes
    waitTimeTotal = 0 #Total wait time for all processes
    turnaroundTimeTotal = 0 #Total turnaround time for all processes
    contextSwitchTotal = 0 #Total number of context switches when running algorithm
    totalBursts = 0
    for i in processes:
        totalBursts += i.cpuBurstNum
    queue = []
    currentProcess = None
    t = 0
    completed = 0
    contextSwitchTime = -1
    contextSwitchIn = False
    contextSwitchOut = False
    print("time %dms: Simulator started for FCFS [Q <empty>]" % t)
    while(True):

        for i in processes:
            if(t == i.arrivalTime and i.state == 0): #Marks if a process arrives
                i.changeState(3) #Marks it as ready
                queue.append(i)
                event("arrival", queue, i, t)

        if(contextSwitchOut and (t == contextSwitchTime + int(tCS/2))): #Context switching to get a process out of CPU
            contextSwitchOut = False
            currentProcess = None

        if(len(queue) > 0 or currentProcess is not None): #If there is a process running or there are ready processes
            if(currentProcess is None): #Start a process if nothing running
                if(contextSwitchIn and (t == contextSwitchTime + int(tCS/2))): #account for context switching
                    currentProcess = queue.pop(0) #take process off ready queue
                    currentProcess.changeState(2)
                    event("cpuStart", queue, currentProcess, t)
                    contextSwitchIn = False #mark done context switching
                    currentProcess.startTime = t #set start time of process
                    contextSwitchTotal += 1
                else:
                    if(not contextSwitchIn and not contextSwitchOut and len(queue) > 0): #start context switch to add process in
                        contextSwitchIn = True
                        contextSwitchTime = t
            else:
                if(t == currentProcess.startTime + currentProcess.cpuBurstTimes[currentProcess.completed] and not contextSwitchOut): #If CPU burst or I/O block is finished
                    currentProcess.completed += 1
                    if(currentProcess.completed == currentProcess.cpuBurstNum): #Last cpu burst of process finished
                        burstTimeTotal += currentProcess.cpuBurstTimes[currentProcess.completed]
                        waitTimeTotal += currentProcess.waitTime
                        currentProcess.waitTime = 0
                        turnaroundTimeTotal += (t-currentProcess.arrivalTime) + tCS
                        event("terminated", queue, currentProcess, t)
                        completed += 1
                        currentProcess.state = 5
                        currentProcess = None
                        if(completed == len(processes)): #all processes are done
                            t += 2
                            break
                    else: #start blocking on I/O
                        burstTimeTotal += currentProcess.cpuBurstTimes[currentProcess.completed]
                        waitTimeTotal += currentProcess.waitTime
                        currentProcess.waitTime = 0
                        event("cpuFinish", queue, currentProcess, t)
                        event("ioStart", queue, currentProcess, t)
                        currentProcess.state = 4
                        currentProcess.startTime = t
                    contextSwitchOut = True
                    contextSwitchTime = t

                
        for i in processes:
            if(i.state == 4 and (t == i.startTime + i.cpuBurstTimes[i.completed])): #finished I/O blocking
                i.state = 3
                queue.append(i)
                event("ioFinish", queue, i, t)

        for i in processes:
            if(i.state == 3):
                i.waitTime += 1
        t += 1 #Increment time
    print("time %dms: Simulator ended for FCFS [Q <empty>]" % t)


    averageCPUBurstTime = round(burstTimeTotal/float(totalBursts), 3)
    averageWaitTime = round(waitTimeTotal/float(totalBursts), 3)
    averageTurnaroundTime = round(turnaroundTimeTotal/float(len(processes)), 3)
    return averageCPUBurstTime, averageWaitTime, averageTurnaroundTime, contextSwitchTotal