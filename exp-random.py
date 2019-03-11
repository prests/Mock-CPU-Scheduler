

def main(r, l, upperBound):
    iterations = 1000000
    total = 0
    for i in range(0, iterations):
        r.drand()
        x = -log(r)/float(l)
        if(x > upperBound):
            i -= 1
            continue
        total += x
        
    avg = total/iterations
    print("x average: %s", avg)
    return avg