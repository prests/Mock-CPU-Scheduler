# /usr/bin/python3

#Used for command line argument parsing
import sys
import math

#Our algorithms
import fcfs
#import rr
#import sjf
#import rr
import sjf
import srt

#Our classes
import process
import rand48

#Exponential Distribution
import expRandom

#Other imports needed
import math

"""
    Outputs for algorithm statistics
"""
def calculateAverage(outFile, name, averageCPUBurstTime, averageWaitTime, averageTurnaroundTime, contextSwitchTotal, preemptionsTotal):
    outFile.write("Algorithm %s\n" %(name))
    outFile.write("-- average CPU burst time: %.3f ms\n" %(averageCPUBurstTime))
    outFile.write("-- average wait time: %.3f ms\n" %(averageWaitTime))
    outFile.write("-- average turnaround time: %.3f ms\n" %(averageTurnaroundTime))
    outFile.write("-- total number of context switches: %d\n" %(contextSwitchTotal))
    outFile.write("-- total number of preemptions: %d\n" %(preemptionsTotal))

'''
    Reset all values of processes between sorting algorithms
'''
def resetProcesses(processes, lambdaED):
    for i in processes:
        i.completed = 0
        i.waitTime = 0
        i.remainingTime = 0
        i.startTime = 0
        i.tau = math.ceil(1/float(lambdaED))
        i.currentPrempt = False
        i.preemptions = 0
        i.state = 0
    return processes

'''
    Printing all the processes before an algorithm for submitty
'''
def printProcesses(processes):
    for i in processes:
        print("Process %s [NEW] (arrival time %d ms) %d CPU bursts" %(i.name, i.arrivalTime, i.cpuBurstNum))

def main(seed, lambdaED, upperBound, n, tCS, alpha, timeSlice, rrBeginning):
    r = rand48.Rand48(0)
    r.srand(seed)
    processes = []
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    '''
        Get all the processes from parameters
    '''
    for i in range(0, n):
        arrivalTime = math.floor(expRandom.expDist(lambdaED, upperBound, r))
        print(arrivalTime)
        cpuBurstNumber = math.floor(r.drand()*100)+1
        print(cpuBurstNumber)
        cpuBurstTimes = []
        for j in range(0, (cpuBurstNumber-1)*2+1):
            cpuBurstTimes.append(math.ceil(expRandom.expDist(lambdaED, upperBound, r)))
        
        tau = math.ceil(1/float(lambdaED))
        p = process.Process(arrivalTime, 0, cpuBurstNumber, cpuBurstTimes, alphabet[i], tau)
        processes.append(p)
    
    '''
        All the sorting algorithms
    '''
    outFile = open("simout.txt", "w")

    printProcesses(processes)
    avgCPUBurstTime, avgWaitTime, avgTurnTime, contextSwitchTotal = sjf.main(processes, tCS, alpha) #Shortest Job First
    calculateAverage(outFile, "SJF", avgCPUBurstTime, avgWaitTime, avgTurnTime, contextSwitchTotal, 0)
    processes = resetProcesses(processes, lambdaED)

    printProcesses(processes)
    avgCPUBurstTime, avgWaitTime, avgTurnTime, contextSwitchTotal, preemptionsTotal = srt.main(processes, tCS, alpha) #Shortest Remaining First
    calculateAverage(outFile, "SRT", avgCPUBurstTime, avgWaitTime, avgTurnTime, contextSwitchTotal, preemptionsTotal)
    processes = resetProcesses(processes, lambdaED)
    
    printProcesses(processes)
    avgCPUBurstTime, avgWaitTime, avgTurnTime, contextSwitchTotal = fcfs.main(processes, tCS) #First Come First Serve
    calculateAverage(outFile, "FCFS", avgCPUBurstTime, avgWaitTime, avgTurnTime, contextSwitchTotal, 0)
    processes = resetProcesses(processes, lambdaED)
    
    printProcesses(processes)
    #rr.main(processes, rrBeginning, timeSlice, tCS) #Round Robin

    outFile.close()

'''
Parse arguments
'''
if __name__ == '__main__':
    '''
    #Checking size of argument array
    if(len(sys.argv) < 8):
        print("Invalid number of arguments provided")
        sys.exit()
    
    #Checking Seed
    seed = sys.argv[1]
    try:
        seed = int(seed)
    except:
        print("Invalid seed provided (not integer)")
        sys.exit()

    #Checking lamda for Exponential Distribution
    lambdaED = sys.argv[2]
    try:
        lambdaED = float(lambdaED)
    except:
        try:
            lambdaED = int(lambdaED)
        except:
            print("Invalid lamda value provided (not interger or float)")
            sys.exit()

    #Checking Upper Bound for pseudo random number generator
    upperBound = sys.argv[3]
    try:
        upperBound = int(upperBound)
    except:
        print("Invalid Upper Bound provided (not integer)")
        sys.exit()

    #Checking number of processes provided 
    n = sys.argv[4]
    try:
        n = int(n)
    except:
        print("Invalid number of processes provided (not integer)")
        sys.exit()
    
    if(n < 0):
            print("expected positive number of processes")
            sys.exit()

    #Checking time for context switching
    tCS = sys.argv[5]
    try:
        tCS = int(tCS)
    except:
        print("Invalid time provided for context switching (not integer)")
        sys.exit()

    #Checking alpha constant for exponential distribution
    alpha = sys.argv[6]
    try:
        alpha = float(alpha)
    except:
        print("Invalid alpha provided (not integer)")
        sys.exit()
    
    #Checking time slicing for Round Robing (RR)
    timeSlice = sys.argv[7]
    try:
        timeSlice = int(timeSlice)
    except:
        print("Invalid time slice provided (not integer)")
        sys.exit()

    #Checking queue order for Round Robin if provided 
    rrBeginning = False
    if(len(sys.argv) == 9):
        if(sys.argv[8] == "BEGGINNING"):
            rrBeginning = True
        elif(sys.argv[8] == "END"):
            rrBeginning = False
        else:
            print("Invalid queue arrival for Round Robin check argument 9 (BEGGINING/END)")
            sys.exit()
    '''
    seed = 70
    lambdaED = 0.001
    upperBound = 3000
    n = 10
    tCS = 8
    alpha = 0.5
    timeSlice = 80
    rrBeginning = "BEGGINNING"
    main(seed, lambdaED, upperBound, n, tCS, alpha, timeSlice, rrBeginning)