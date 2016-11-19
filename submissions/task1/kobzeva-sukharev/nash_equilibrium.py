import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt
def nash_equilibrium(A):
    #Поиск минимума матрицы А
    min_value = abs(np.amin(A)) + 1
    #Делаем матрицу положительной
    A += min_value
    #Подготовка столбцов ограничений для ЗЛП
    z = np.ones(A.shape[0])
    b_1 = -np.ones(A.shape[1])
    w = -np.ones(A.shape[1])
    b_2 = np.ones(A.shape[0])
    #Проверка на равновесие по Нэшу
    nash_i,nash_j = nash_equilibrium_point(A, min_value)
    if(nash_i != 0):
        p = np.zeros(A.shape[0])
        p[nash_i - 1] = 1
        q = np.zeros(A.shape[1])
        q[nash_j - 1] = 1
        v = A[nash_i - 1, nash_j - 1] - min_value
        return p,q,v
    #Поиск оптимального решения в смешанных стратегиях
    # Игрок 1
    res = linprog(w, A, b_2, options = {"disp": True})
    q = res.get("x")
    # Игрок 2
    A = -np.transpose(A)
    res = linprog(z, A, b_1, options = {"disp": True})
    p = res.get("x")
    #Расчет значения игры
    v = 1 / np.sum(p)
    p *= v
    q *= v
    v = v - min_value
    print("p: ", p)
    print("q: ", q)
    print("v: ", v)
    return p, q, v
def nash_equilibrium_point(A, min_value):
    #Поиск равновесия по Нэшу
    max_nash = np.zeros((len(A),len(A[0])))
    for i, row in enumerate(A):
        max_nash[i] = np.array(row == row.min())
    for j, column in enumerate(A.T):
        max_nash[:, j] += np.array(column == column.max())
    sum = 0
    print ("Ситуации равновесия по Нэшу")
    for (i, j), value in np.ndenumerate(max_nash):
        if value == 2:
            sum += 1
            nash_i = i + 1
            nash_j = j + 1
            print("Точка равновесия #", sum)
            print("v: ", A[i, j] - min_value)
            print("Стратегия первого: ", i + 1)
            print("Стратегия второго: ", j + 1)
    if(sum == 0):
        print("Таких точек нет")
        return 0, 0
    elif(sum == 1):
        return nash_i, nash_j
    else:
        print("Таких точек несколько")
        return 0, 0
def draw(p, q):
    x = max(len(p), len(q))
    y = max(max(p), max(q))
    plt.xlim([0, x + x / 4])
    plt.ylim([0, y + y / 4])
    for i, value in enumerate(p):
        plt.scatter(1.0 * i + 1, value, color = 'blue')
        plt.plot([1.0 * i + 1, 1.0 * i + 1], [0.0, value], color = 'blue') 
        plt.grid(True)   # линии вспомогательной сетк
    plt.show()
    plt.xlim([0, x + x / 4])
    plt.ylim([0, y + y / 4])
    for i, value in enumerate(q):
        plt.scatter(1.0 * i + 1, value, color = 'blue')
        plt.plot([1.0 * i + 1, 1.0 * i + 1], [0.0, value], color = 'blue')
        plt.grid(True)   # линии вспомогательной сетк
    plt.show()
print("Введите число строк в матрице А:")
n = int(input())
A = []
print("Введите матрицу А по строкам")
for i in range(n):
    row = input().split()
    for i in range(len(row)):
        row[i] = float(row[i])
    A.append(row)
A = np.array(A)
p,q,v = nash_equilibrium(A)
draw(p, q)