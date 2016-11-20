import numpy as np
from scipy.optimize import linprog
def nash_equilibrium(a):  
    A = a.transpose()
    rownum, colnum = np.shape(A)
    #создаем вектор c1 целевой функции для ЗЛП, соответсвующей первому игроку      
    c1 = np.array([1] * colnum)
    #создаем вектор c2 правой части для ЗЛП, соответствующей первому игроку 
    c2 = np.array([-1] * rownum)
    #приводим матрицу а к виду, подходящему для использования ф-ии linprog для нахождения стратегий игрока 1
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
    #приводим матрицу а к виду, подходящему для использования ф-ии linprog для нахождения стратегий игрока 2
    A *= -1
    #создаем вектор b1 целевой функции для ЗЛП, соответсвующей второму игроку
    b1 = np.array([-1] * rownum)
    #создаем вектор b2 правой части для ЗЛП, соответсвующей второму игроку
    b2 = np.array([1] * colnum)
    q = linprog(b1, a, b2).x
    q_opt = q*(1/v)
    return value, p_opt, q_opt
