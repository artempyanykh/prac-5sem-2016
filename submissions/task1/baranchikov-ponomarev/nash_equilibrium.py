def nash_equilibrium(a):
    # preprocessing matrix for linprog
    a = np.array(a)
    aij_min = a.min()
    was_normalization = False
    if aij_min <= 0:
        a -= aij_min - 1
        was_normalization = True
        
    c = [1] * len(a)
    A_ub = -a.T
    b_ub = [-1] * len(a[0])
    
    first_distribution = linprog(c, A_ub, b_ub).x 
    game_value = 1 / np.sum(first_distribution)
    first_distribution *= game_value
    
    c, b_ub = b_ub, c
    A_ub = a
    second_distribution = linprog(c, A_ub, b_ub).x * game_value
    
    if was_normalization:
        game_value += aij_min - 1
    
    return game_value, first_distribution, second_distribution
