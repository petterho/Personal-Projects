def control_equal(*variables):
    for variable0 in variables:
        for variable1 in variables:
            if variable0 != variable1:
                return False
    return True


def control_not_equal(*variables):
    n = 0
    for variable0 in variables:
        n += 1
        for variable1 in variables[n:]:
            if variable0 == variable1:
                return False
    return True

def coff_control_function(C, O, F, T, H, E, R):
    coff = F + 10 * F + 100 * O + 1000 * C
    theor = R + 10 * O + 100 * E + 1000 * H + 10000 * T
    if 3 * coff == theor and control_not_equal(C, O, F, T, H, E, R):
        return True
    return False

def coff_function():
    list_of_solutions = []
    for C in range(10):
        for O in range(10):
            for F in range(10):
                for T in range(10):
                    for H in range(10):
                        for E in range(10):
                            for R in range(10):
                                if coff_control_function(C, O, F, T, H, E, R):
                                    answer = {'C': C, 'O': O, 'F': F, 'T': T,
                                              'H': H, 'E': E, 'R': R}
                                    list_of_solutions.append(answer)
    return list_of_solutions

def coffee_control_function(C, O, F, T, H, E, R, M):
    coffee = 11 * E + 1100 * F + 10000 * O + 10**5 * C
    theorem = M + 10010 * E + 100 * R + 10**3 * O + 10**5 * H + 10**6 * T
    if 3 * coffee == theorem and control_not_equal(C, O, F, T, H, E, R, M):
        return True
    return False

def coffee_function():
    list_of_solutions = []
    for C in range(10):
        for O in range(10):
            for F in range(10):
                for T in range(10):
                    for H in range(10):
                        for E in range(10):
                            for R in range(10):
                                for M in range(10):
                                    if coffee_control_function(C, O, F, T, H,
                                                               E, R, M) \
                                            and C < 3:
                                        answer = {'C': C, 'O': O, 'F': F,
                                                  'T': T, 'H': H, 'E': E,
                                                  'R': R, 'M': M}
                                        list_of_solutions.append(answer)
    return list_of_solutions


answer = coff_function()
print(answer)
answer = coffee_function()
print(answer)


