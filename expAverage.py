import math
'''
    tau     =   (alpha *  t  ) + ((1-alpha) * tau )
       i+1                 i                     i
'''
def nextTau(tau, alpha, actualBurstTime):
    x = ((alpha*actualBurstTime) + ((1-alpha)*tau))
    if(float(x) % 1) >= 0.5:
        return math.ceil(x)
    else:
        return round(x)