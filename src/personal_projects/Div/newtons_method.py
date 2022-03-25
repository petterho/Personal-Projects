"""
Project by Petter to look at Newtons method of finding roots
"""
import random as r


def grad_function(f, x, delta_x=0.001):
    g = (f(x + delta_x) - f(x)) / delta_x
    return g


def newtons_method(f, x, error_margin_y=0.001, iteration_cap=1000,
                   delta_x=0.001, return_lists=True):
    if return_lists:
        y = f(x)
        x_list = [x]
        y_list = [y]

        i = 0
        while abs(y) > error_margin_y and i < iteration_cap:
            g = grad_function(f, x, delta_x=delta_x)
            x = x - y / g
            y = f(x)

            x_list.append(x)
            y_list.append(y)
            i += 1
        if i >= iteration_cap:
            raise RuntimeError('Did not find a root')
        return x_list, y_list
    else:
        y = f(x)

        i = 0
        while abs(y) > error_margin_y and i < iteration_cap:
            g = grad_function(f, x, delta_x=delta_x)
            x = x - y / g
            y = f(x)

            i += 1
        if i >= iteration_cap:
            raise RuntimeError('Did not find a root')
        return x


def find_roots_newton(f, iter_for_new_roots=10, error_margin_x=0.001,
                      error_margin_y=0.001, seed=None):
    roots = []
    rndgen = r.Random()
    rndgen.seed(seed)
    searching = True
    iter_since_last_root = 0

    while searching:
        x = rndgen.gauss(0, 5)
        try:
            root = newtons_method(f, x, return_lists=False,
                                  error_margin_y=error_margin_y)
        except RuntimeError:
            iter_since_last_root += 1
            continue
        if not x_in_list(root, roots, error_margin_x=error_margin_x):
            roots.append(root)
            iter_since_last_root = 0
        else:
            iter_since_last_root += 1

        if iter_since_last_root > iter_for_new_roots:
            searching = False

    return roots


def x_in_list(x, roots_list, error_margin_x=0.001):
    for root in roots_list:
        if abs(x - root) < error_margin_x:
            return True
    return False


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np


    def function1(x):
        return x**3 + 1 + x - 3*x**2

    X, Y = newtons_method(function1, -4, return_lists=True)
    fig, ax = plt.subplots(2)
    ax[0].plot(Y)
    ax[0].set_title('Y values')
    ax[1].plot(X)
    ax[1].set_title('X values')
    fig.tight_layout()
    fig.show()

    roots = find_roots_newton(function1, error_margin_x=0.1,
                              error_margin_y=0.00001)
    fig, ax = plt.subplots()
    x_values = [k for k in np.linspace(-5, 5)]
    y_values = [function1(x_val) for x_val in x_values]
    ax.plot(x_values, y_values)
    y_roots = [0 for _ in range(len(roots))]
    ax.plot(roots, y_roots, 'bo')
    ax.set_ylim((-5, 5))
    fig.tight_layout()
    fig.show()
    print(roots)
