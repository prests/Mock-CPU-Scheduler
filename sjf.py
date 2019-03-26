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
    Output formating
'''
def event(eventType, queue, process, t):
    queueStr = printQueue(queue)
    if(eventType == "arrival"):
        print("time %dms: Process %s (tau %dms) arrived; added to ready queue %s" %(t, process.name, process.tau, queueStr))
    elif(eventType == "cpuStart"):
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
    elif(eventType == "terminated"):
        print("time %dms: Process %s terminated %s" %(t, process.name, queueStr))
    elif(eventType == "newTau"):
        print("time %dms: Recalculated tau = %dms for process %s %s" %(t, process.tau, process.name, queueStr))
    else:
        print("I'm not sure how you got here...")

'''
    SJF algorithm
'''
def main(processes, tCS, alpha):
    burstTimeTotal = 0                              # Total burst time for all processes
    waitTimeTotal = 0                               # Total wait time for all processes
    turnaroundTimeTotal = 0                         # Total turnaround time for all processes
    contextSwitchTotal = 0                          # Total number of context switches when running algorithm
    
    totalBursts = 0                                 # The total number of CPU bursts
    for i in processes:
        totalBursts += i.cpuBurstNum
    
    queue = []                                      # Ready queue
    currentProcess = None                           # The current process running
    
    t = 0                                           # Current time
    completed = 0                                   # How many processes have been completed
    contextSwitchTime = -1                          # Time when a context switch is starting
    contextSwitchIn = False                         # Is the process context switching in? 
    contextSwitchOut = False                        # Is the process context switching out?
    print("time %dms: Simulator started for SJF [Q <empty>]" % t)
    while(True):
        for i in processes:
            if(t == i.arrivalTime and i.state == 0):                                                    # Marks if a process arrives and checks if it can cut queue
                '''
                    Process Arrival
                '''
                if(len(queue) == 0):                                                                    # Queue is empty so add to ready queue
                    i.changeState(3)                                                                    # Marks it as ready
                    queue.append(i)
                    if(t<1000):
                        event("arrival", queue, i, t)

                    if(i.turnaroundStart == -1):                                           # If not turnaround start time is set then set it
                        i.turnaroundStart = t
                else:
                    for j in range(0,len(queue)):                                                       # Check if arriving process can cut ready queue
                        if((i.tau < queue[j].tau) or ((i.tau == queue[j].tau) and (i.name < queue[j].name))):   # Tau is shorter and can cut  
                            i.changeState(3)                                                            # Marks it as ready
                            queue.insert(j, i)
                            if(t<1000):
                                event("arrival", queue, i, t)
                            if(i.turnaroundStart == -1):                                           # If not turnaround start time is set then set it
                                i.turnaroundStart = t
                            break
                    if(i.state != 3):                                                                   # Arriving process has largest Tau in list
                        i.changeState(3)                                                                # Marks it as ready
                        queue.append(i)
                        if(t<1000):
                            event("arrival", queue, i, t)
                        if(i.turnaroundStart == -1):                                           # If not turnaround start time is set then set it
                            i.turnaroundStart = t

        if(contextSwitchOut and (t == contextSwitchTime + int(tCS/2))):                                 # Context switching to get a process out of CPU
            contextSwitchOut = False
            contextSwitchTime = -1 

            for i in processes:                                                                             # Check if a process is finished blocking on I/O
                if(i.state == 4 and (t == i.startTime + i.cpuBurstTimes[i.completed])):                     # Process finished I/O blocking
                    '''
                        I/O Blocking Completed
                    '''
                    i.completed += 1
                    if(len(queue) == 0 and currentProcess is None and not contextSwitchOut and not contextSwitchIn):    # Queue is empty add process to rady queue
                        i.changeState(6)                                                                    # Marks it as ready
                        queue.append(i)
                        contextSwitchIn = True
                        contextSwitchTime = t
                        if(t<1000):
                            event("ioFinish", queue, i, t)
                        currentProcess = i
                        queue.pop(0)
                    else:
                        for j in range(0,len(queue)):                                                       # Check if arriving process can cut ready queue
                            
                            if((i.tau < queue[j].tau) or ((i.tau == queue[j].tau) and (i.name < queue[j].name))):   # Tau is shorter and can cut  
                                i.changeState(3)                                                            # Marks it as ready
                                queue.insert(j, i)
                                if(t<1000):
                                    event("ioFinish", queue, i, t)
                                if(i.turnaroundStart == -1):                                           # If not turnaround start time is set then set it
                                    i.turnaroundStart = t
                                break
                        if(i.state != 3):                                                                   # Arriving process has largest Tau in list
                            i.changeState(3)                                                                # Marks it as ready
                            queue.append(i)
                            if(t<1000):
                                event("ioFinish", queue, i, t)
                            if(i.turnaroundStart == -1):                                           # If not turnaround start time is set then set it
                                i.turnaroundStart = t

            if(currentProcess.state == 4 or currentProcess.state == 5):
                currentProcess = None

        if(len(queue) > 0 or currentProcess is not None):                                               # If there is a process running or there are ready processes
            
            if(currentProcess is None or currentProcess.state == 6):                                                                 # Start a process if nothing running
                if(contextSwitchIn and (t == contextSwitchTime + int(tCS/2) and currentProcess is not None)):                          # Account for context switching
                    '''
                        CPU Burst Starting
                    '''
                    currentProcess.changeState(2)
                    if(t<1000):
                        event("cpuStart", queue, currentProcess, t)
                    contextSwitchIn = False                                                             # Mark done context switching
                    currentProcess.startTime = t                                                        # Set start time of process
                    contextSwitchTotal += 1
                    if(currentProcess.turnaroundStart == -1):                                           # If not turnaround start time is set then set it
                        currentProcess.turnaroundStart = t
                else:
                    if(not contextSwitchIn and not contextSwitchOut and len(queue) > 0):                # Start context switch to add process in
                        contextSwitchIn = True
                        if(currentProcess is None):
                            currentProcess = queue.pop(0)
                            currentProcess.changeState(6)
                        contextSwitchTime = t
            else:
                if(currentProcess.state != 5):
                    if(t == currentProcess.startTime + currentProcess.cpuBurstTimes[currentProcess.completed] and not contextSwitchOut): #If CPU burst or I/O block is finished
                        '''
                            CPU Burst Completed
                        '''
                        currentProcess.completed += 1
                        currentProcess.burstComplete += 1
                        if(currentProcess.burstComplete == currentProcess.cpuBurstNum):                         # Last cpu burst of process finished
                            '''
                                Process Completed
                            '''
                            burstTimeTotal += currentProcess.cpuBurstTimes[currentProcess.completed-1]        # Add burst time to total
                            
                            waitTimeTotal += currentProcess.waitTime                                        # Add wait time to total
                            currentProcess.waitTime = 0                                                     # Reset burst wait time
                            
                            turnaroundTimeTotal += (t-currentProcess.turnaroundStart) + tCS/2                 # Add turnaround time to total
                            currentProcess.turnaroundStart = -1                                             # Reset burst turnaround time
                            
                            event("terminated", queue, currentProcess, t)
                            
                            completed += 1                                                                  # Increase completed process
                            currentProcess.state = 5
                            
                            if(completed == len(processes)):                                                # All processes are done
                                '''
                                    All Processes Completed
                                '''
                                t += tCS/2
                                break
                        else:                                                                               # Burst is done so start blocking on I/O
                            '''
                                I/O Blocking Starting
                            '''
                            burstTimeTotal += currentProcess.cpuBurstTimes[currentProcess.completed-1]        # Add burst time to total
                            
                            waitTimeTotal += currentProcess.waitTime                                        # Add wait time to total
                            currentProcess.waitTime = 0                                                     # Reset burst wait time
                            
                            turnaroundTimeTotal += (t-currentProcess.turnaroundStart) + tCS/2                 # Add turnaround time to total
                            currentProcess.turnaroundStart = -1                                             # Reset burst turnaround time
                            
                            if(t<1000):
                                event("cpuFinish", queue, currentProcess, t)
                            currentProcess.tau = expAverage.nextTau(currentProcess.tau, alpha, currentProcess.cpuBurstTimes[currentProcess.completed-1])        # Recalculate tau
                            if(t<1000):
                                event("newTau", queue, currentProcess, t)
                                event("ioStart", queue, currentProcess, t)
                            
                            currentProcess.state = 4
                            currentProcess.startTime = t                                                    # Set start time for I/O burst
                        
                        contextSwitchOut = True                                                             # Start context switch out
                        contextSwitchTime = t



        for i in processes:                                                                             # Check if a process is finished blocking on I/O
            if(i.state == 4 and (t == i.startTime + i.cpuBurstTimes[i.completed])):                     # Process finished I/O blocking
                '''
                    I/O Blocking Completed
                '''
                i.completed += 1
                if(len(queue) == 0 and currentProcess is None and not contextSwitchOut and not contextSwitchIn):    # Queue is empty add process to rady queue
                    i.changeState(6)                                                                    # Marks it as ready
                    queue.append(i)
                    if(i.turnaroundStart == -1):                                           # If not turnaround start time is set then set it
                        i.turnaroundStart = t
                    contextSwitchIn = True
                    contextSwitchTime = t
                    if(t<1000):
                        event("ioFinish", queue, i, t)
                    currentProcess = i
                    queue.pop(0)
                else:
                    for j in range(0,len(queue)):                                                       # Check if arriving process can cut ready queue
                        
                        if((i.tau < queue[j].tau) or ((i.tau == queue[j].tau) and (i.name < queue[j].name))):   # Tau is shorter and can cut  
                            i.changeState(3)                                                            # Marks it as ready
                            queue.insert(j, i)
                            if(t<1000):
                                event("ioFinish", queue, i, t)
                            if(i.turnaroundStart == -1):                                           # If not turnaround start time is set then set it
                                i.turnaroundStart = t
                            break
                    if(i.state != 3):                                                                   # Arriving process has largest Tau in list
                        i.changeState(3)                                                                # Marks it as ready
                        queue.append(i)
                        if(t<1000):
                            event("ioFinish", queue, i, t)
                        if(i.turnaroundStart == -1):                                           # If not turnaround start time is set then set it
                            i.turnaroundStart = t

        for i in processes:                                                                             # Checks if process is waiting in ready queue
            if(i.state == 3):                                                                           # Process is waiting for increment wait time
                i.waitTime += 1
            
        
        t += 1                                                                                          # Increment time
    print("time %dms: Simulator ended for SJF [Q <empty>]\n" % t)

    averageCPUBurstTime = round(burstTimeTotal/float(totalBursts), 3)               # Average burst time for algorithm
    averageWaitTime = round(waitTimeTotal/float(totalBursts), 3)                    # Average wait time for algorithm
    averageTurnaroundTime = round(turnaroundTimeTotal/float(totalBursts), 3)        # Average turnaround time for algorithm
    return averageCPUBurstTime, averageWaitTime, averageTurnaroundTime, contextSwitchTotal