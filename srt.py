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
    Output formating for submitty
'''
def event(eventType, queue, process, t, preempt):
    queueStr = printQueue(queue)
    if(eventType == "arrival"):
        print("time %dms: Process %s (tau %dms) arrived; added to ready queue %s" %(t, process.name, process.tau, queueStr))
    elif(eventType == "arrivalPreempt"):
        print("time %dms: Process %s (tau %dms) arrived and will preempt %s %s" %(t, process.name, process.tau, preempt.name, queueStr))
    elif(eventType == "cpuStart"):
        if(process.currentPrempt):
            print("time %dms: Process %s started using the CPU with %dms remaining %s" %(t, process.name, process.remainingTime, queueStr))
        else:
            print("time %dms: Process %s started using the CPU for %dms burst %s" %(t, process.name, process.cpuBurstTimes[process.completed], queueStr))
    elif(eventType == "cpuFinish"):
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
    contextSwitchTime = -1                          # Time when a context switch is starting
    contextSwitchIn = False                         # Is the process context switching in? 
    contextSwitchOut = False                        # Is the process context switching out?
    print("time %dms: Simulator started for SRT [Q <empty>]" % t)
    while(True):
        for i in processes:
            if(t == i.arrivalTime and i.state == 0):                                                                                            # Marks if a process arrives and checks if it can cut queue
                '''
                    Process Arrival
                '''
                if(currentProcess is not None and ((i.tau < currentProcess.tau) or ((i.tau == currentProcess.tau) and (i.name < currentProcess.name))) and not contextSwitchOut):                                       # Arrival preempts current process
                    if(currentProcess.currentPrempt):                                                                                           # Formatting for calculating time remaining in a preemptions
                        currentProcess.remainingTime -= (t - currentProcess.startTime)
                    else:
                        currentProcess.remainingTime = currentProcess.cpuBurstTimes[currentProcess.completed] - (t - currentProcess.startTime)
                    currentProcess.currentPrempt = True                                                                                         
                    currentProcess.preemptions += 1
                    
                    if(t<1000):
                        event("arrivalPreempt", queue, i, t, currentProcess)
                    queue.insert(0,currentProcess)                                                                                              # Adds current process to front of ready queue
                    queue.insert(0,i)                                                                                                           # Adds preempted process to front of queue to get popped
                    
                    contextSwitchOut = True                                                                                                     # Context is switching out
                    contextSwitchTime = t                                                                                                       # Start time of context switch
                    
                    preemptionTotal += 1                                                                                                        # Increase total preemptions for algorithm
                    i.turnaroundStart = t                                                                                                       # Reset turnaroundStart for given process
                elif(len(queue) == 0):                                                                                                          # queue is empty
                    i.changeState(3)                                                                                                            # Marks it as ready
                    queue.append(i)
                    i.turnaroundStart = t                                                                                                       # Reset turnaroundStart for given process
                    
                    if(t<1000):
                        event("arrival", queue, i, t, "")
                else:
                    for j in range(0,len(queue)):                                                                                               # Check if arriving process can cut ready queue
                        if((i.tau < queue[j].tau) or ((i.tau == queue[j].tau) and (i.name < queue[j].name))):   # Tau is shorter and can cut  
                            i.changeState(3)                                                                                                    # Marks arrived process as ready
                            queue.insert(j, i)
                            i.turnaroundStart = t                                                                                               # Reset turnaroundStart for given process
                            if(t<1000):
                                event("arrival", queue, i, t, "")
                            break
                    if(i.state != 3):                                                                                                           # Arriving process has largest Tau in list
                        i.changeState(3)                                                                                                        # Marks it as ready
                        queue.append(i)
                        if(t<1000):
                            event("arrival", queue, i, t, "")

        if(contextSwitchOut and (t == contextSwitchTime + int(tCS/2))):                                                                         # Context switching to get a process out of CPU
            contextSwitchOut = False
            currentProcess = None

        if(len(queue) > 0 or currentProcess is not None):                                                                                       # If there is a process running or there are ready processes
            if(currentProcess is None):                                                                                                         # Start a process if nothing running
                if(contextSwitchIn and (t == contextSwitchTime + int(tCS/2))):                                                                  # Account for context switching in
                    '''
                        CPU Burst Starting
                    '''
                    currentProcess = queue.pop(0)                                                                                               # Take process off ready queue
                    currentProcess.changeState(2)
                    if(t<1000):
                        event("cpuStart", queue, currentProcess, t, "")
                    contextSwitchIn = False                                                                                                     # Mark done context switching
                    currentProcess.startTime = t                                                                                                # Set start time of process
                    
                    contextSwitchTotal += 1                                                                                                     # Increase total number of context switching
                    
                    if(currentProcess.turnaroundStart == -1):                                                                                   # If turnaround start time isn't set set it
                        currentProcess.turnaroundStart = t
                else:
                    if(not contextSwitchIn and not contextSwitchOut and len(queue) > 0):                                                        # Start context switch to add process in
                        contextSwitchIn = True
                        contextSwitchTime = t
            else:
                if((t == currentProcess.startTime + currentProcess.cpuBurstTimes[currentProcess.completed] and not contextSwitchOut and not currentProcess.currentPrempt) or (t == currentProcess.startTime + currentProcess.remainingTime and not contextSwitchOut and currentProcess.currentPrempt)): # If CPU burst or I/O block is finished
                    '''
                        CPU Burst Completed
                    '''
                    currentProcess.burstComplete += 1
                    currentProcess.completed += 1                                                                                               # Increase bursts completed
                    currentProcess.currentPrempt = False                                                                                        # Burst is no longer preempting
                    currentProcess.remainingTime = 0                                                                                            # Reset remaining time
                    
                    if(currentProcess.burstComplete == currentProcess.cpuBurstNum):                                                                 # Last CPU burst of process finished
                        '''
                            Process Completed
                        '''
                        burstTimeTotal += currentProcess.cpuBurstTimes[currentProcess.completed-1]                                                # Add burst time to average                                               
                        
                        waitTimeTotal += currentProcess.waitTime                                                                                # Add wait time to average
                        currentProcess.waitTime = 0                                                                                             # Reset process wait time
                        
                        turnaroundTimeTotal += (t-currentProcess.turnaroundStart) + tCS/2                                                         # Add turnaround time to average
                        currentProcess.turnaroundStart = -1                                                                                     # Reset burst turnaround time start
                        
                        event("terminated", queue, currentProcess, t, "")                                                                       
                        
                        completed += 1                                                                                                          # Add to completed processes total
                        currentProcess.state = 5
                        currentProcess = None
                        if(completed == len(processes)):                                                                                        # All processes are done
                            '''
                                All Processes Completed
                            '''
                            t += tCS/2
                            break
                    else:                                                                                                                       # Finished a burst so start blocking on I/O
                        '''
                            I/O Blocking Starting
                        '''
                        burstTimeTotal += currentProcess.cpuBurstTimes[currentProcess.completed-1]                                                # Add burst time to average
                        
                        waitTimeTotal += currentProcess.waitTime                                                                                # Add wait time to average
                        currentProcess.waitTime = 0                                                                                             # Reset process wait time
                        
                        turnaroundTimeTotal += (t-currentProcess.turnaroundStart) + tCS/2                                                         # Add turnaround time to average
                        currentProcess.turnaroundStart = -1                                                                                     # Reset burst turnaround time start
                        
                        if(t<1000):
                            event("cpuFinish", queue, currentProcess, t, "")
                        
                        currentProcess.tau = expAverage.nextTau(currentProcess.tau, alpha, currentProcess.cpuBurstTimes[currentProcess.completed-1])    # Recalculate tau
                        
                        if(t<1000):
                            event("newTau", queue, currentProcess, t, "")
                            event("ioStart", queue, currentProcess, t, "")
                        currentProcess.state = 4                                                                                                        # Set process to I/O blocking
                        currentProcess.startTime = t                                                                                                    # Set start time for I/O blocking
                    
                    contextSwitchOut = True                                                                                                             # Start context switch out
                    contextSwitchTime = t

                
        for i in processes:                                                                                                                             # Checking if a process has finished I/O burst
            if(i.state == 4 and (t == i.startTime + i.cpuBurstTimes[i.completed])):                                                                     # Finished I/O blocking
                '''
                    I/O Blocking Completed
                '''
                i.completed += 1
                if(currentProcess is not None and ((i.tau < currentProcess.tau) or ((i.tau == currentProcess.tau) and (i.name < currentProcess.name))) and not contextSwitchOut):                                                
                    i.changeState(3)
                    if(currentProcess.currentPrempt):                                                                                                   # Formatting for calculating time remaining in a preemptions
                        currentProcess.remainingTime -= (t - currentProcess.startTime)
                    else:
                        currentProcess.remainingTime = currentProcess.cpuBurstTimes[currentProcess.completed] - (t - currentProcess.startTime)
                    currentProcess.currentPrempt = True
                    currentProcess.preemptions += 1                                                                                                     # Add preemption to process
                    if(t<1000):
                        event("ioPreempt", queue, i, t, currentProcess)
                    
                    queue.insert(0,currentProcess)                                  # Add current process to ready queue due to preemption
                    queue.insert(0,i)                                               # Put preempting process for front of ready queue to get popped
                    
                    contextSwitchOut = True                                         # Begin context switch
                    contextSwitchTime = t
                    preemptionTotal += 1                                            # Total preemptions increase
                
                elif(len(queue) == 0 and currentProcess is None and not contextSwitchOut and not contextSwitchIn):    # Queue is empty add process to ready queue
                    i.changeState(3)                                                                    # Marks it as ready
                    queue.append(i)
                    contextSwitchIn = True
                    contextSwitchTime = t
                    if(t<1000):
                        event("ioFinish", queue, i, t, "")
                else:
                    for j in range(0,len(queue)):                                   # Check if arriving process can cut ready queue
                        if((i.tau < queue[j].tau) or ((i.tau == queue[j].tau) and (i.name < queue[j].name))):   # Tau is shorter and can cut  
                            i.changeState(3)                                        # Marks it as ready
                            queue.insert(j, i)
                            if(t<1000):
                                event("ioFinish", queue, i, t, "")
                            break
                    if(i.state != 3):                                               # Arriving process has largest Tau in list
                        i.changeState(3)                                            # Marks it as ready
                        queue.append(i)
                        if(t<1000):
                            event("ioFinish", queue, i, t, "")

        for i in processes:                                                         # Check if a process is waiting in ready queue
            if(i.state == 3):
                i.waitTime += 1                                                     # Increment process wait time
        
        t += 1                                                                      # Increment time
    
    print("time %dms: Simulator ended for SRT [Q <empty>]\n" % t)


    averageCPUBurstTime = round(burstTimeTotal/float(totalBursts), 3)               # Average burst time for algorithm
    averageWaitTime = round(waitTimeTotal/float(totalBursts), 3)                    # Average wait time for algorithm
    averageTurnaroundTime = round(turnaroundTimeTotal/float(totalBursts), 3)        # Average turnaround time for algorithm
    return averageCPUBurstTime, averageWaitTime, averageTurnaroundTime, contextSwitchTotal, preemptionTotal