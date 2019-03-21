import process
# /usr/bin/python3


def makeQueue(Q, processes, currTime, rr_add, currP = 0): # addElementsToQRR
    for p in (processes):
        # check if the p is in the queue and is not the current process
        if(p not in Q and p.completed != p.cpuBurstNum): 
            # finish me
            if(p.arrivalTime<=currTime):
                if(rr_add == "END"):
                    Q.append(p)
                else:
                    Q.insert(0, p)
            
            
            formattedQ = getQueue(Q)

            if(p.remainingTime == 0):
                if(p.completed > 0):
                    print('time ' + str(int(currTime)) + 'ms: Process ' + p.name + " completed I/O; added to ready queue " + formattedQ)
                else:
                    print('time ' + str(int(currTime)) + 'ms: Process ' + p.name + " arrived and added to ready queue " + formattedQ)

    return Q

def getQueue(Q):
    if(len(Q) > 0):
        output = "[Q"
        for i in Q:
            output += " " + i.name

        output += "]"
        return output

    return "[Q <empty>]"

#def main(processes, timeSlice=8, rrBeginning, tCS, rr_add="END"):
'''

processes   =     allProcesses, time slice for each process)
timeSlice   =     time slot given for each p to execute
rrBeginning =     boolean
tCS         =     turn around time (context switches)
rr_add      =     determines whether process goes to beginning or end of queue

'''
def main(processes, rrBeginning, timeSlice=80, tCS=8, rr_add="END"):
    print("Algorithm RR")
    

    currTime = 0
    numPreeptions = 0
    completed = False
    '''
    status:
        0 - not arrived
        1 - arrived
        2 - running
        3 - ready
        4 - blocked
        5 - Done
    '''
    Q = []
    Q = makeQueue(Q, processes, currTime, rr_add)

    

    while(completed == False):
        # create queue
        Q = makeQueue(Q, processes, currTime, rr_add)

        while(Q): #while shits still in the Q

            # create current process var and setis its start time
            currP = Q.pop(0)
            currP.startTime = currTime


            # update states
            for i in Q:
                if(currTime == i.arrivalTime and i.state == 0): #Marks if a process arrives
                    i.changeState(3) #Marks it as ready
            
            # account for context switch time
            r = int(tCS/2)
            for i in range(r):
                Q = makeQueue(Q, processes, currTime, rr_add)
                currTime += 1


            # calc wait time of each process (amount of time in ready queue)
            wait = currP.startTime - currP.arrivalTime
            currP.waitTime += wait

            # get str of queue
            formattedQ = getQueue(Q)


            # [0] time process took to complete
            # [1] a constant???
            # [2] bursts left to complete?
            # [3] 
            # [4] num bursts completed
            # [5] total wait time
            # [6] remaining t after preemption
            # [7] turnaround time

            # if there is any remaining time after preemption, print Q & remaing time
            if(currP.remainingTime > 0): #idk if this is right
                print('time ' + str(int(currTime)) + 'ms: Process '+ currP.name + " started using the CPU with " + str(int(currP.cpuBurstTimes)) + "ms remaining " + formattedQ)
            else: 
                # else print Q & termination str
                print('time ' + str(int(currTime)) + 'ms: Process ' + currP.name + " started using the CPU " + formattedQ)



            # NEED TO CHANGE STATES
            preemption = False
            while(preemption == False): # while there is no preemption, run currP
                # if there is remaining t, set burst t = to that
                # else, set it equal to normal burst time 

                '''
                if currP.remainingTime < timeSlice:
                    burstTime = currP.remainingTime
                else:
                    burstTime = currP.something # IDK IF THIS IS RIGHT
                '''
                currP.changeState(2)
                burstTime = currP.remainingTime

                if(timeSlice<burstTime):
                    # if there is no time to complete the process...
                    completionTime = currTime + timeSlice      # this burst will take the whole timeslice to complete
                    currP.remainingTime = burstTime-timeSlice  # update remaining t of process
                    currP.completed = completionTime + tCS/2   # Update time to complete
                else:
                    # if there is preemption...
                    preemption = True
                    completionTime = currTime + burstTime       # hng but is + burst time correct?
                    ioTime = currP.startTime - currTime
                    currP.cpuBurstTimes.append(completionTime)  # hngggg
                    currP.completed += 1
                    # currP.preemption += 1 wasnt sure if I should keep here or below
                    currP.remainingTime = completionTime + tCS/2 + ioTime # idk about this one
                    currP.changeState(4)                         # change to blocked state
                
                while currTime < completionTime:
                    # wait the amount of time determined to simulate CPU usage
                    Q = makeQueue(Q, processes, currTime, rr_add)
                    currTime += 1

                # if this is the last processs to complete...
                formattedQ = getQueue(Q)
                if(currP.remainingTime>0 and len(Q) == 0 ):
                    print('time ' + str(int(currTime)) + 'ms: Time slice expired; no preemption bc queue is empty')
                else:
                    preemption = True
                
            # end while

            if(currP.completed==currP.cpuBurstNum): #check if process is complete
                print('time ' + str(int(currTime)) + 'ms: Time slice expired; process ' + currP.name)
                currP.changeState(5)
            elif currP.remainingTime > 0:
                print('time ' + str(int(currTime)) + 'ms: Process ' + currP.name + " preempted with " + str(int(currP.remainingTime)) + "ms to go " + formattedQ)
                currP.preemption += 1
                currP.changeState(3)
            else:
                print('time ' + str(int(currTime)) + 'ms: Process ' + currP.name + " completed a CPU burst; " + str(currP.completed) + " burst(s) to go " + formattedQ)
                print('time ' + str(int(currTime)) + 'ms: Process ' + currP.name + " switching out of CPU; will block on I/O until time " + str(int(currTime + ioTime + t_cs/2)) + "ms " + formattedQ)
                currP.changeState(4)

            
            # account for context switch
            r = int(tCS/2)
            for i in range(r):
                Q = makeQueue(Q, processes, currTime, rr_add)
                currTime += 1

    
        allDone = True
        for p in Q:
            if (p.state != 5): #its not done
                allDone = False

        print('time ' + str(int(currTime)) + 'ms: Simulator ended for RR')
        completed = True

