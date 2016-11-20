#!/usr/bin/env python3

from scipy.optimize import linprog as lp
import numpy as np

def nash_equilibrium (a):
    size = a.shape
    rows = size[0]
    cols = size[1]

#-------------NEW PART--------------
    k = a[0][0]

    for i  in range (0,rows):
        for j in range (0,cols):
            if k>a[i][j]:
                k = a[i][j]

    if k<0:
        k = -k+1
    else:
        k = k+1

    for i  in range (0,rows):
        for j in range (0,cols):
            a[i][j] = a[i][j] + k
#------------------------------------

    a1 = a.transpose()
    b1 = np.ones((1,cols), dtype=np.int)
    c1 = np.ones((1,rows), dtype=np.int)

    a2 = a
    b2 = np.ones((1,rows), dtype=np.int)
    c2 = np.ones((1,cols), dtype=np.int)

    v = 1/ (lp(c1[0],-a1,-b1[0]).fun)
    p = lp(c1[0],-a1,-b1[0]).x * v

    v = -1/ (lp(-c2[0],a2,b2[0]).fun)
    q = lp(-c2[0],a2,b2[0]).x * v

#-------------------------------------
    v = v - k
#-------------------------------------

    print (v)
    print (p)
    print (q)

    return v,p,q


if __name__ == "__main__":
    n = int(input())
    matrix = np.array([list(map(int, input().split()))
                       for i in range(n)])
    nash_equilibrium(matrix)
