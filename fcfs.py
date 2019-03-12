# /usr/bin/python3
import process
import rand48
import expRandom
import math

def fcfsSort(processes):
    for i in range(0,len(processes)):
        for j in range(0, len(processes)-i-1):
            if processes[j].arrivalTime > processes[j+1]:
                processes[j], processes[j+1] = processes[j+1], processes[j]
    return processes

def main(processes):
    print("Algorithm FCFS")
    processes = fcfsSort(processes)
    queue = []

    t = 0
    completed = 0

    while(completed != len(processes)):
        