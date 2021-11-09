"""
Project by Petter to look at Newtons method of finding roots
"""


def grad_function(f, x, delta_x=0.001):
    g = (f(x + delta_x) - f(x)) / delta_x
    return g


def newtons_method(f, x, error_margin=0.001, iteration_cap=1000,
                   delta_x=0.001, return_lists=True):
    if return_lists:
        y = f(x)
        x_list = [x]
        y_list = [y]

        i = 0
        while abs(y) > error_margin and i < iteration_cap:
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
        while abs(y) > error_margin and i < iteration_cap:
            g = grad_function(f, x, delta_x=delta_x)
            x = x - y / g
            y = f(x)

            i += 1
        if i >= iteration_cap:
            raise RuntimeError('Did not find a root')
        return x


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    def function1(x):
        return x**2 - 1

    X, Y = newtons_method(function1, -4, return_lists=True)
    fig, ax = plt.subplots(2)
    ax[0].plot(Y)
    ax[0].set_title('Y values')
    ax[1].plot(X)
    ax[1].set_title('X values')
    fig.show()
