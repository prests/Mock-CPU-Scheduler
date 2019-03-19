import process
# /usr/bin/python3


def makeQueue(Q, processes, currTime, rr_add):
    for key in sorted(processes):
        #value = processes[key]
        # check if the key is in the queue and is not the current process
        if(key not in Q and key.completed != key.cpuBurstNum): 
            # finish me

    return Q 

def getQueue():
    if(len(Q) > 0):
        output = "[Q"
        for i in Q:
            output += " " + i

        output += "]"
        return output

    return "[Q <empty>]"

#def main(processes, timeSlice=8, rrBeginning, tCS, rr_add="END"):
def main(processes, timeSlice=80, rrBeginning, tCS=8, rr_add="END"):
    print("Algorithm RR")
    

    currTime = 0
    numPreeptions = 0
    completed = False

    Q = []
    Q = makeQueue(Q, processes, currTime, rr_add)

    while(completed == False):
        Q = makeQueue(Q, processes, currTime, rr_add)

        while(Q):
            currP = Q.pop(0)
            start = currTime
            
            r = int(tCS/2)
            for i in range(r):
                Q = makeQueue(Q, processes, currTime, rr_add)
                currTime += 1


            # calc wait time of each process (amount of time in ready queue)
            wait = start - currP.arrivalTime
            currP.waitTime +=wait


            formattedQ = getQueue()

            # [5] total wait time
            # [6] remaining t after preemption
            # [7] turnaround time

            # if there is any remaining time after preemption
            if(currP.remainingTime > 0): #idk if this is right
                print('time ' + str(int(currTime)) + 'ms: Process '+ currP + " started using the CPU with " + str(int(currP.cpuBurstTimes)) + "ms remaining " + formattedQ))
            else:
                print('time ' + str(int(currTime)) + 'ms: Process ' + currP + " started using the CPU " + formattedQ)



            # NEED TO CHANGE STATES
            preemption = False
            while(preemption == False):
                # if there is remaining t after preemption, set burst = to that
                # else, set it equal to normal burst time 
                if currP.remainingTime > 0:
                    burstTime = currP.remainingTime
                else:
                    burstTime = currP.cpuBurstTimes # IDK IF THIS IS RIGHT


                if(timeSlice<burstTime):
                    completionTime = currTime + timeSlice
                    currP.remainingTime = burstTime-timeSlice
                    currP.completed = completionTime + tCS/2 # Do I set to currP.completed?
                else:
                    preemption = True
                    completionTime = currTime + burstTime
                    ioTime = start - currTime
                    # idk about the next 2 lines 
                    currP.cpuBurstNum -= 1 
                    currP.cpuBurstTimes += 1
                    currP.completed = completionTime + tCS/2 + iotime
                    currP.remainingTime = 0
                
                while currTime < completionTime:
                    Q = makeQueue(Q, processes, currTime, rr_add)
                    currTime += 1

                formattedQ = getQueue()

                if(currP.remainingTime>0 and len(Q) == 0 ):
                    print('time ' + str(int(currTime)) + 'ms: Time slice expired; no preemption bc queue is empty')
                else:
                    preemption = True
                
            # end while

            if(currP.completed==currP.cpuBurstNum): #check if process is complete
                print('time ' + str(int(currTime)) + 'ms: Process ' + currP)

                # check if remaining time


    