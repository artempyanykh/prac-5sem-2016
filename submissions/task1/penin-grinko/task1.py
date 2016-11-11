import numpy as np
from scipy.optimize import linprog
def nash_equilibrium(a):        
    mina = a[0][0]
    maximb = 0 
    kol = []
    i_nash = -1
    j_nash = -1
    min_in_a = a[0][0]
    x = []
    y = []
    c1 = []
    for i in range(len(a)) :
        c1.append(1)
        x.append(0)
    c2 = []
    for i in range(len(a[0])) :
        c2.append(-1)
        y.append(0)
    for i in range(len(a)) :
        for j in range(len(a[0])) :
            if a[i][j] <= mina :
                mina = a[i][j]
        for t in range(len(a[0])) :
            if a[i][t] == mina :
                kol.append(t)
        for h in range(len(kol)) :
            maximb = a[0][kol[h]] 
            for k in range(len(a)) :
                if a[k][kol[h]] >= maximb:
                    maximb = a[k][kol[h]]
            if a[i][kol[h]] == maximb :
                i_nash = i
                j_nash = kol[h]
                break
        if i < len(a) - 1 :
            mina = a[i + 1][0]
        del kol[:]
    if i_nash != -1 and j_nash != -1 :
        x[i_nash] = 1
        y[j_nash] = 1
        return a[i_nash][j_nash], x, y
    for i in range(len(a)) :
        for j in range(len(a[0])) :
            if a[i][j] < 0 :
                is_pos = 0
                break
    if is_pos == 0 :
        for i in range(len(a)) :
            for j in range(len(a[0])) :
                if a[i][j] < min_in_a:
                    min_in_a = a[i][j]
        a -= min_in_a
    A = a.transpose()
    for i in range(len(A)) : 
        for j in range(len(A[0])) :
            A[i][j] *= -1
    p = linprog(c1, A, c2).x
    v = np.dot(p, c1)
    p_opt = p*(1/v)
    value = 1/v
    if is_pos == 0:
        value += min_in_a
    for i in range(len(A)) : 
        for j in range(len(A[0])) :
            A[i][j] *= -1
    q = [] 
    b1 = []
    for i in range(len(a[0])) :
        b1.append(-1)
    b2 = []
    for i in range(len(a)) :
        b2.append(1)
    q = linprog(b1, a, b2).x
    q_opt = q*(1/v)
    return value, p_opt, q_opt