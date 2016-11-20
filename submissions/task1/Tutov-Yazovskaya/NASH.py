import scipy.optimize as sp_o
import numpy as np

# Ввод размеров матрицы выигрыша (количество стратегий 1-го и 2-го игроков соответственно)
n = int(input())
m = int(input())

# Основная функция задания
def nash_equilibrium(A):
    # Шаг1: проверка на наличие седловой точки у матрицы выигрыша
    min_row = A.min(axis=1)
    max_col = A.max(axis=0)
    maximin = max(min_row)
    minimax = min(max_col)
    
    if maximin == minimax: 
        
        # Если седловая точка есть, то есть решение в чистых стратегиях, 
        # и нам нужно просто проставить единицы в соотвествующие ячейки массивов стратегий игроков
        
        min_row = A.min(axis=1)
        max_col = A.max(axis=0)
        v = maximin
        for i in range(n):
            for j in range(m):
                if min_row[i] == maximin and max_col[j] == minimax:
                    Ans_x = np.zeros(n)
                    Ans_x[i] = 1
                    Ans_y = np.zeros(m)
                    Ans_y[j] = 1
    else:
        
        # Если седловой точки нет, то записываем две двойственные задачи линейного программирования,
        #     которые решаются функцией scipy.optimize.linprog(...). 
        
        c = []
        b = []
        for i in range(n):
            c.append(1)
        for i in range(m):
            b.append(-1)
        
        add_cost = abs(A.min())
        A += add_cost
        
        # Примечание: ниже используется функция transpose библиотеки numpy. 
        # Она "некорректно" (не так, как нам надо) работает с одномерными массивами.
        # Необходимо заметить, что у одномерной матрицы выигрыша ВСЕГДА существует седловая точка,
        #     поэтому в данном случае применение transpose корректно.
        
        A = np.transpose(A)
        res1 = sp_o.linprog(c, A_ub=(-1)*A, b_ub=b, options={"disp": True})
        A = np.transpose(A)
        res2 = sp_o.linprog(b, A_ub=A, b_ub=c, options={"disp": True})
        v = 1 / (res1.fun)
        Ans_x = abs(v) * res1.x
        Ans_y = abs(v) * res2.x
        v -= add_cost
        
    # Возвращаем список из двух стратегий игроков и цены игры
    
    return [Ans_x, Ans_y, v]


# Инициализация входной матрицы выигрыша, ее ввод, запуск функции решения, и вывод решения на экран

A = []
for i in range(n):
    row = input().split()
    for i in range(m):
        row[i] = int(row[i])
    A.append(row)
A = np.array(A)

res = nash_equilibrium(A)
print("Strategy of player 1: ", res[0], "\nStrategy of player 2: ", res[1], "\nGame cost: ", res[2])