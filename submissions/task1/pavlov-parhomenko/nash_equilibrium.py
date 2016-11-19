import numpy as np
import pandas as pd
import time
from scipy.optimize import linprog
from scipy import misc
import sys
from unittest import *
import os
import numpy as np
import unittest

import matplotlib.pylab as plt

def nash_equilibrium_points(A, min_threshold):
    nash = np.zeros((A.shape))
    for i in range(A.shape[0]):
        for idx in np.argwhere(A[i] == np.min(A[i])):
            nash[i][idx] += 1
            
    for i in range(A.shape[1]):
        for idx in np.argwhere(A[:, i] == np.max(A[:, i]))[0]:
            nash[idx][i] += 1

    points_vals = [[i, j] for i in range(nash.shape[0]) for j in range(nash.shape[1]) if nash[i][j] == 2]

    if not len(points_vals):
        print 'no points'
        return None
    else:
        for point in points_vals:
            print('value', A[point[0]][point[1]] - min_threshold, 'First strategy', point[0] + 1, \
               'Second strategy', point[1] + 1)
        return points_vals
    return 0

def nash_equilibrium(A):
    print np.min(A)
    min_threshold = np.abs(np.min(A)) + 1
    A += min_threshold

    points = nash_equilibrium_points(A, min_threshold)
    if points and len(points) == 1:
        first = np.zeros(A.shape[0])
        second = np.zeros(A.shape[1])
        first[points[0][0]] = 1
        second[points[0][1]] = 1
        return first, second, A[points[0][0]][points[0][1]] - min_threshold
    print 'all finish'
    
    b, w = np.ones(A.shape[0]), -np.ones(A.shape[1])
    res_first = linprog(w, A_ub = A, b_ub = b, options = {"disp": False})
    b, w = -np.ones(A.shape[1]), np.ones(A.shape[0])
    res_second = linprog(w, A_ub = -A.T, b_ub = b, options = {"disp": False})

    game_value = np.sum(res_second.get("x"))
    
    return res_first.get("x") / game_value, res_second.get("x") / game_value, (1 / game_value) - min_threshold

def draw(p, q):
    x1, x2 = np.arange(p.shape[0]), np.arange(q.shape[0])
    for pair in zip([x1, x2], [p, q]):
        plt.figure(figsize=(8,6), dpi = 80)
        plt.ylabel('strategy selection probability')
        plt.xlabel('strategy number')
        plt.grid(True)
        plt.scatter(pair[0], pair[1], color='blue')
        map(lambda x, y: plt.plot([x, x], [0.0, y], color = 'blue'), pair[0], pair[1])
        plt.show()

def main():
	print("Input number of rows in matrix")
	n = int(input())
	A = []
	print 'Input matrix A by rows'
	for i in range(n):
	    row = input().split()
	    for i in range(len(row)):
        	row[i] = float(row[i])
	    A.append(row)

	p,q,v = nash_equilibrium(A)
	draw(p, q)
	return 0

if __name__ == '__main__':
	main()