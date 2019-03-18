# /usr/bin/python3
import expAverage


def main(processes, tCS, alpha, tau):
    print("Algorithm SJF")

    queue = []
    t = 0
    while(True):
        for i in processes:
            if(t == i.arrivalTime and i.state == 0):
                print("Processes Arrived")
                if(len(queue) < 2):
                    i.changeState(3)
                    queue.append(i)
                else:
                    nextTau = expAverage.nextTau(tau, alpha, queue[0].actualBurstTime[queue[0].completed-1]) #THIS ISN'T RIGHT??
                    tau = nextTau
                    for j in range(1,len(queue)):
                        if(nextTau < queue[0].cpuBurstTimes[queue[0].completed]):
                            print("Process is jumping the line")
                            queue.insert(j, i)
                            i.changeState(3)
                        elif(j == len(queue)-1):
                            queue.append(i)
                            i.changeState(i)

        if(len(queue) > 0):
            if