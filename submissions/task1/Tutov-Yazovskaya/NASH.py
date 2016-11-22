import scipy.optimize as sp_o
import numpy as np

# Основная функция задания
def nash_equilibrium(A):
    
    A = np.array(A)
    n = np.shape(A)[0]
    m = np.shape(A)[1]
    
    # Записываем две двойственные задачи линейного программирования,
    #     которые решаются функцией scipy.optimize.linprog(...). 
    
    c = []
    b = []
    for i in range(n):
        c.append(1)
    for i in range(m):
        b.append(-1)
    
    # Делаем матрицу выигрыша положительной. Потом в конце вычтем то, на что прибавили.

    add_cost = abs(A.min())
    A += add_cost
        
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
if __name__ == '__main__':
    n = int(input())
    m = int(input())
    A = []
    for i in range(n):
        row = input().split()
        for i in range(m):
            row[i] = int(row[i])
        A.append(row)

    res = nash_equilibrium(A)
    print("Strategy of player 1: ", res[0], "\nStrategy of player 2: ", res[1], "\nGame cost: ", res[2])