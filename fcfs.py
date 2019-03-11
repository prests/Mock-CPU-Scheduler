# /usr/bin/python3
import process
import rand48

def main(seed, upperBound, n, tCS):
    print("Algorithm FCFS")

    r = rand48.Rand48(0)
    r.srand(seed)

    processes = []

    for i in range(0, n):
        arrivalTime = r.drand()
        cpuBurstNumber = round(r.drand()*100)+1
        CPUtime = r.drand()
        IOtime = r.drand()
        p = process.Process(arrivalTime, 0, cpuBurstNumber)
        for i in range(0, cpuBurstNumber):
            
        print(p.cpuBurstNum)