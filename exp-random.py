import rand48
import math

def classExample(seed, upperBound):
    r = rand48.Rand48(0)
    r.srand(seed)
    iterations = 1000000
    total = 0
    minVal = 0
    maxVal = 0
    l = 0.001
    for i in range(0, iterations):
        uniformDist = r.drand()
        x = -math.log(uniformDist)/float(l)
        if(x > upperBound):
            i -= 1
            continue
        total += x
        if(i < 20):
            print(x)
        if(i == 0 or x < minVal):
            minVal = x
        if(i ==0 or x > maxVal):
            maxVal = x
    
    avg = total/iterations

    print("minimum value: %d", minVal)
    print("maximum value: %d", maxVal)
    print("average value: %d", avg)

def expDist(uniformDist, l, upperBound, r):
    while(True):
        x = -math.log(uniformDist)/float(l)
        if(x > upperBound):
            uniformDist = r.drand()
            print("failed")
        else:
            break
    return x
        
        
    avg = total/iterations
    print("x average: %s", avg)
    return avg


if __name__ == "__main__":
    seed = 80
    upperBound = 3000
    rand = rand48.Rand48(0)
    rand.srand(seed)
    classExample(seed, upperBound)
    val = expDist(rand.drand(), 0.001, 10, rand)
    print(val)