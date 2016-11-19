import numpy as np
from scipy.optimize import linprog
def nash_equilibrium(a):  
    A = a.transpose()
    rownum, colnum = np.shape(A)
    #������� ������ c1 ������� ������� ��� ���, �������������� ������� ������      
    c1 = np.array([1] * colnum)
    #������� ������ c2 ������ ����� ��� ���, ��������������� ������� ������ 
    c2 = np.array([-1] * rownum)
    #�������� ������� � � ����, ����������� ��� ������������� �-�� linprog ��� ���������� ��������� ������ 1
    min_a = np.amin(A)
    if (min_a < 0):
        A -= min_a - 1
    A *= -1
    p = linprog(c1, A, c2).x
    v = np.dot(p, c1)
    p_opt = p*(1/v)
    value = 1/v
    if (min_a < 0):
        value += min_a - 1
    #�������� ������� � � ����, ����������� ��� ������������� �-�� linprog ��� ���������� ��������� ������ 2
    A *= -1
    #������� ������ b1 ������� ������� ��� ���, �������������� ������� ������
    b1 = np.array([-1] * rownum)
    #������� ������ b2 ������ ����� ��� ���, �������������� ������� ������
    b2 = np.array([1] * colnum)
    q = linprog(b1, a, b2).x
    q_opt = q*(1/v)
    return value, p_opt, q_opt
