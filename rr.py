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
        if(process.currentPrempt):
            print("time %dms: Process %s started using the CPU with %dms remaining %s" %(t, process.name, process.cpuBurstTimes[process.completed], queueStr))
        else:
            print("time %dms: Process %s started using the CPU for %dms burst %s" %(t, process.name, process.cpuBurstTimes[process.completed], queueStr))
    elif(eventType == "cpuFinish"):
        print("time %dms: Process %s completed a CPU burst; %d bursts to go %s" %(t, process.name, process.cpuBurstNum-process.burstComplete, queueStr))
    elif(eventType == "ioStart"):
        print("time %dms: Process %s switching out of CPU; will block on I/O until time %dms %s" %(t, process.name, t+process.cpuBurstTimes[process.completed], queueStr))
    elif(eventType == "ioFinish"):
        print("time %dms: Process %s completed I/O; added to ready queue %s" %(t, process.name, queueStr))
    elif(eventType == "timeSlice"):
        print("time %dms: Time slice expired; process %s preempted with %dms bursts to go %s" %(t, process.name, process.remainingTime, queueStr))
    elif(eventType == "timeSliceNoPreempt"):
        print("time %dms: Time slice expired; no preemption because ready queue is empty %s" %(t, queueStr))
    elif(eventType == "terminated"):
        print("time %dms: Process %s terminated %s" %(t, process.name, queueStr))
    else:
        print("I'm not sure how you got here...")


'''
    FCFS algorithm
'''
def main(processes, rrBeginning, timeSlice, tCS):
    burstTimeTotal = 0                              # Total burst time for all processes
    waitTimeTotal = 0                               # Total wait time for all processes
    turnaroundTimeTotal = 0                         # Total turnaround time for all processes
    contextSwitchTotal = 0                          # Total number of context switches when running algorithm
    preemptionTotal = 0

    totalBursts = 0                                 # Total number of bursts of all processes
    for i in processes:
        totalBursts += i.cpuBurstNum
    
    queue = []                                      # Ready queue
    currentProcess = None                           # Current process running in CPU
    t = 0                                           # Current time
    completed = 0                                   # Number of process completed
    
    contextSwitchTime = -1                          # Start time for context switch
    contextSwitchIn = False                         # Is CPU context switching in?
    contextSwitchOut = False                        # Is CPU context switching out?

    print("time %dms: Simulator started for RR [Q <empty>]" % t)
    while(True):
        for i in processes:                                                                             # Checks if a process is arriving
            if(t == i.arrivalTime and i.state == 0):                                                    # Marks if a process arrives
                '''
                    Process Arrival
                '''
                i.changeState(3)                                                                        # Marks it as ready
                
                if(rrBeginning == "END"):                                                               # Determines for RR if process gets added to BEGINNING or END of queue
                    queue.append(i)
                else:
                    queue.insert(0,i)
                if(t<1000):
                    event("arrival", queue, i, t)

        if(contextSwitchOut and (t == contextSwitchTime + int(tCS/2))):                     # Context switching to get a process out of CPU
            contextSwitchOut = False
            currentProcess = None

        if(len(queue) > 0 or currentProcess is not None):                                   # If there is a process running or there are ready processes
            if(currentProcess is None):                                                     # Start a process if nothing running
                
                if(contextSwitchIn and (t == contextSwitchTime + int(tCS/2))):              # Account for context switching
                    '''
                        CPU Burst Starting
                    '''
                    currentProcess = queue.pop(0)                                           # Take process off ready queue
                    currentProcess.changeState(2)
                    if(t<1000):
                        event("cpuStart", queue, currentProcess, t)
                    contextSwitchIn = False                                                 # Mark done context switching
                    currentProcess.startTime = t                                            # Set start time of process
                    contextSwitchTotal += 1                                                 # Increase context switch total for algorithm
                    
                    if(currentProcess.turnaroundStart == -1):                               # If process turnaround start time isn't set then set it
                        currentProcess.turnaroundStart = t
                else:
                    if(not contextSwitchIn and not contextSwitchOut and len(queue) > 0):    # Start context switch to add process in
                        contextSwitchIn = True
                        contextSwitchTime = t
            else:
                if((t == currentProcess.startTime + currentProcess.cpuBurstTimes[currentProcess.completed] and not contextSwitchOut and not currentProcess.currentPrempt) or (t == currentProcess.startTime + currentProcess.remainingTime and not contextSwitchOut and currentProcess.currentPrempt)): # If CPU burst is finished
                    '''
                        CPU Burst Completed
                    '''
                    currentProcess.completed += 1                                                       # Incrememnt Process completed bursts
                    currentProcess.burstComplete += 1
                    currentProcess.currentPrempt = False                                                # Burst is no longer preempting
                    currentProcess.remainingTime = 0                                                    # Reset burst remaining time

                    if(currentProcess.burstComplete == currentProcess.cpuBurstNum):                         # Last cpu burst of process finished
                        '''
                            Process Completed
                        '''
                        burstTimeTotal += currentProcess.cpuBurstTimes[currentProcess.completed-1]        # Add burst time to total
                        
                        waitTimeTotal += currentProcess.waitTime                                        # Add wait time to total
                        currentProcess.waitTime = 0                                                     # Reset process wait time
                        
                        turnaroundTimeTotal += (t-currentProcess.turnaroundStart) + tCS                 # Add turnaround time to total
                        currentProcess.turnaroundStart = -1                                             # Reset process turnaround start time
                        
                        event("terminated", queue, currentProcess, t)
                        completed += 1                                                                  # Incremement number of processes completed
                        currentProcess.state = 5
                        currentProcess = None
                        if(completed == len(processes)):                                                # All processes are done
                            '''
                                All Processes Completed
                            '''
                            t += tCS/2
                            break
                    else:                                                                               # CPU burst finished so start blocking on I/O
                        '''
                            I/O Blocking Starting
                        '''
                        burstTimeTotal += currentProcess.cpuBurstTimes[currentProcess.completed-1]        # Add burst time to total
                        
                        waitTimeTotal += currentProcess.waitTime                                        # Add wait time to total
                        currentProcess.waitTime = 0                                                     # Reset process wait time
                        
                        turnaroundTimeTotal += (t-currentProcess.turnaroundStart) + tCS                 # Add turnaround time to total
                        currentProcess.turnaroundStart = -1                                             # Reset process turnaround start time
                        
                        if(t<1000):
                            event("cpuFinish", queue, currentProcess, t)
                            event("ioStart", queue, currentProcess, t)
                        currentProcess.state = 4
                        currentProcess.startTime = t
                    contextSwitchOut = True                                                             # Start context switch out
                    contextSwitchTime = t
                elif(t == currentProcess.startTime + timeSlice):                                        # Time slice expired
                    '''
                        Time Slice Ending
                    '''
                    if(len(queue) == 0):                                                                # Ending but no other process in ready queue
                        if(t<1000):
                            event("timeSliceNoPreempt", queue, currentProcess, t)
                        else:
                            pass
                    else:
                        if(currentProcess.currentPrempt):                                               # Set remaining time for burst
                            currentProcess.remainingTime -= (t - currentProcess.startTime)
                        else:
                            currentProcess.remainingTime = currentProcess.cpuBurstTimes[currentProcess.completed] - (t - currentProcess.startTime)
                        currentProcess.currentPrempt = True                                             # Burst will now have at least 1 preemption
                        currentProcess.preemptions += 1

                        if(t<1000):
                            event("timeSlice", queue, currentProcess, t)
                        
                        queue.append(currentProcess)                                                    # Add process to the end of ready queue
                        contextSwitchOut = True                                                         # Begin a context switch out
                        contextSwitchTime = t

                        preemptionTotal += 1                                                            # Increase total preemptions for algorithm

                
        for i in processes:                                                                             # Checks if a process is done blocking on I/O
            if(i.state == 4 and (t == i.startTime + i.cpuBurstTimes[i.completed])):                     # Process is  finished I/O blocking
                '''
                    I/O Blocking Completed
                '''
                i.completed += 1
                i.state = 3
                if(len(queue) == 0 and currentProcess is None and not contextSwitchOut and not contextSwitchIn):
                    queue.append(i)
                    if(i.turnaroundStart == -1):                                           # If not turnaround start time is set then set it
                        i.turnaroundStart = t
                    contextSwitchIn = True
                    contextSwitchTime = t
                    if(t<1000):
                        event("ioFinish", queue, i, t)
                else:
                    if(rrBeginning == "END"):                                                               # Determines for RR if process gets added to BEGINNING or END of queue
                        queue.append(i)
                    else:
                        queue.insert(0,i)
                    if(i.turnaroundStart == -1):                                           # If not turnaround start time is set then set it
                        i.turnaroundStart = t
                    if(t<1000):
                        event("ioFinish", queue, i, t)

        for i in processes:                                                                             # Check if process is waiting in ready queue
            if(i.state == 3):
                i.waitTime += 1                                                                         # Incrememnt total wait time of burst
        
        t += 1                                                                                          # Increment time
    print("time %dms: Simulator ended for RR [Q <empty>]" % t)


    averageCPUBurstTime = round(burstTimeTotal/float(totalBursts), 3)               # Average burst time for algorithm
    averageWaitTime = round(waitTimeTotal/float(totalBursts), 3)                    # Average wait time for algorithm
    averageTurnaroundTime = round(turnaroundTimeTotal/float(totalBursts), 3)        # Average turnaround time for algorithm
    return averageCPUBurstTime, averageWaitTime, averageTurnaroundTime, contextSwitchTotal, preemptionTotal