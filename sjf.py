# /usr/bin/python3
import expAverage


def main(processes, tCS, alpha, tau):
    queue = []
    currentProcess = None
    t = 0
    completed = 0
    contextSwitchTime = -1
    contextSwitchIn = False
    contextSwitchOut = False
    print("time %dms: Simulator started for FCFS [Q <empty>]" % t)