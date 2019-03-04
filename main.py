# /usr/bin/python3

#Used for command line argument parsing
import sys

#Our algorithms
import fcfs
import rr
import sjf
import srt



def main(seed, lambdaED, upperBound, n, tCS, alpha, timeSlice, rrBeginning):
    sjf.main()
    srt.main()
    fcfs.main(seed, upperBound, n, tCS)
    rr.main()

'''
Parse arguments
'''
if __name__ == '__main__':
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
        alpha = int(alpha)
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
    
    main(seed, lambdaED, upperBound, n, tCS, alpha, timeSlice, rrBeginning)