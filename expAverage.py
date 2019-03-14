'''
    tau     =   (alpha *  t  ) + ((1-alpha) * tau )
       i+1                 i                     i
'''
def nextTau(tau, alpha, actualBurstTime):
    return ((alpha*actualBurstTime) + ((1-alpha)*tau))