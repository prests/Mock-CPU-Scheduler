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
                    for j in range(1,len(queue)):
                        nextTau = expAverage.nextTau(tau, alpha, ) #THIS ISN'T RIGHT
                        if(nextTau < queue[0].cpuBurstTimes[queue[0].completed]):
                            print("Process is jumping the line")
                        elif(j == len(queue)-1):
                            queue.append(i)

        if(len(queue) > 0):
            

