from scipy.optimize import linprog
import numpy as np
 
def nash_equilibrium(inMatrix):
    inMatrix = np.array(inMatrix)
    mmin = inMatrix.min()
    delta = abs(mmin) + 1
    inMatrix = inMatrix + delta
    transp = inMatrix.T*-1
    c = np.ones((len(inMatrix)))
    bub = np.ones((len(inMatrix[0])))*-1
    resz = linprog(c, transp, bub)
    resw = linprog(bub, inMatrix, c)
    v = 1 / sum(resz.x)
    return v * resz.x, v * resw.x, v - delta
