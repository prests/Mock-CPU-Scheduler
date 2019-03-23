# /usr/bin/python3
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
    Output formating
'''
def event(eventType, queue, process, t, preempt):
    queueStr = printQueue(queue)
    if(eventType == "arrival"):
        print("time %dms: Process %s (tau %dms) arrived; added to ready queue %s" %(t, process.name, process.tau, queueStr))
    elif(eventType == "cpuStart"):
        if(process.currentPrempt):
            print("time %dms: Process %s started using the CPU with %dms remaining %s" %(t, process.name, process.cpuBurstTimes[process.completed], queueStr))
        else:
            print("time %dms: Process %s started using the CPU for %dms burst %s" %(t, process.name, process.cpuBurstTimes[process.completed], queueStr))
    elif(eventType == "cpuFinish"):
        print("time %dms: Process %s completed a CPU burst; %d to go %s" %(t, process.name, process.cpuBurstNum-process.completed, queueStr))
    elif(eventType == "ioStart"):
        print("time %dms: Process %s switching out of CPU; will block on I/O until time %dms %s" %(t, process.name, t+process.cpuBurstTimes[process.completed], queueStr))
    elif(eventType == "ioFinish"):
        print("time %dms: Process %s (tau %dms) completed I/O; added to ready queue %s" %(t, process.name, process.tau, queueStr))
    elif(eventType == "ioPreempt"):
        print("time %dms: Process %s (tau %dms) completed I/O and will preempt %s %s" %(t, process.name, process.tau, preempt.name, queueStr))
    elif(eventType == "terminated"):
        print("time %dms: Process %s terminated %s" %(t, process.name, queueStr))
    elif(eventType == "newTau"):
        print("time %dms: Recalculated tau = %dms for Process %s %s" %(t, process.tau, process.name, queueStr))
    else:
        print("I'm not sure how you got here...")

'''
    SRT algorithm
'''
def main(processes, tCS, alpha):
    queue = []
    currentProcess = None
    t = 0
    completed = 0
    contextSwitchTime = -1
    contextSwitchIn = False
    contextSwitchOut = False
    print("time %dms: Simulator started for SRT [Q <empty>]" % t)
    while(True):
        for i in processes:
            if(t == i.arrivalTime and i.state == 0): #Marks if a process arrives and checks if it can cut queue
                if(len(queue) == 0): #queue is empty
                    i.changeState(3) #Marks it as ready
                    queue.append(i)
                    event("arrival", queue, i, t, "")
                else:
                    for j in range(0,len(queue)): #Check if arriving process can cut ready queue
                        if(i.tau < queue[j].tau):
                            i.changeState(3) #Marks it as ready
                            queue.insert(j, i)
                            event("arrival", queue, i, t, "")
                            break
                    if(i.state != 3): #Arriving process has largest Tau in list
                        i.changeState(3) #Marks it as ready
                        queue.append(i)
                        event("arrival", queue, i, t, "")

        if(contextSwitchOut and (t == contextSwitchTime + int(tCS/2))): #Context switching to get a process out of CPU
            contextSwitchOut = False
            currentProcess = None

        if(len(queue) > 0 or currentProcess is not None): #If there is a process running or there are ready processes
            if(currentProcess is None): #Start a process if nothing running
                if(contextSwitchIn and (t == contextSwitchTime + int(tCS/2))): #account for context switching
                    currentProcess = queue.pop(0) #take process off ready queue
                    currentProcess.changeState(2)
                    event("cpuStart", queue, currentProcess, t, "")
                    contextSwitchIn = False #mark done context switching
                    currentProcess.startTime = t #set start time of process
                else:
                    if(not contextSwitchIn and not contextSwitchOut and len(queue) > 0): #start context switch to add process in
                        contextSwitchIn = True
                        contextSwitchTime = t
            else:
                if((t == currentProcess.startTime + currentProcess.cpuBurstTimes[currentProcess.completed] and not contextSwitchOut and not currentProcess.currentPrempt) or (t == currentProcess.startTime + currentProcess.remainingTime and not contextSwitchOut and currentProcess.currentPrempt)): #If CPU burst or I/O block is finished
                    currentProcess.completed += 1
                    currentProcess.currentPrempt = False
                    currentProcess.remainingTime = 0
                    if(currentProcess.completed == currentProcess.cpuBurstNum): #Last cpu burst of process finished
                        event("terminated", queue, currentProcess, t, "")
                        completed += 1
                        currentProcess.state = 5
                        currentProcess = None
                        if(completed == len(processes)): #all processes are done
                            t += 2
                            break
                    else: #start blocking on I/O
                        event("cpuFinish", queue, currentProcess, t, "")
                        currentProcess.tau = expAverage.nextTau(currentProcess.tau, alpha, currentProcess.cpuBurstTimes[currentProcess.completed-1])
                        event("newTau", queue, currentProcess, t, "")
                        event("ioStart", queue, currentProcess, t, "")
                        currentProcess.state = 4
                        currentProcess.startTime = t
                    contextSwitchOut = True
                    contextSwitchTime = t

                
        for i in processes:
            if(i.state == 4 and (t == i.startTime + i.cpuBurstTimes[i.completed])): #finished I/O blocking
                if(currentProcess is not None and (i.tau < currentProcess.tau) and not contextSwitchOut): #I/O process preempts current process
                    if(currentProcess.currentPrempt):
                        currentProcess.remainingTime -= (t - currentProcess.startTime)
                    else:
                        currentProcess.remainingTime = currentProcess.cpuBurstTimes[currentProcess.completed] - (t - currentProcess.startTime)
                    currentProcess.currentPrempt = True
                    currentProcess.preemptions += 1
                    event("ioPreempt", queue, i, t, currentProcess)
                    queue.insert(0,currentProcess)
                    queue.insert(0,i)
                    contextSwitchOut = True
                    contextSwitchTime = t
                elif(len(queue) == 0): #queue is empty
                    i.changeState(3) #Marks it as ready
                    queue.append(i)
                    event("ioFinish", queue, i, t, "")
                else:
                    for j in range(0,len(queue)): #Check if arriving process can cut ready queue
                        if(i.tau < queue[j].tau):
                            i.changeState(3) #Marks it as ready
                            queue.insert(j, i)
                            event("ioFinish", queue, i, t, "")
                            break
                    if(i.state != 3): #Arriving process has largest Tau in list
                        i.changeState(3) #Marks it as ready
                        queue.append(i)
                        event("ioFinish", queue, i, t, "")

        t += 1 #Increment time
    print("time %dms: Simulator ended for SRT [Q <empty>]" % t)