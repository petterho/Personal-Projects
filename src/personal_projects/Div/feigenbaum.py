import numpy as np
import matplotlib.pyplot as plt


def pop_function(c, x):
    return c * x * (1 - x)


def stable_points(c, x=0.5, start_loops=100, error=0.01):
    for _ in range(start_loops):
        x = pop_function(c, x)

    list_stable_points = [x]
    x = pop_function(c, x)
    while abs(x - list_stable_points[0]) > error:
        list_stable_points.append(x)
        x = pop_function(c, x)
    return list_stable_points


def plot_stable_points(c_from=0, c_to=4, error=0.01, number_of_cs=1000,
                       start_loops=1000):
    c_list = np.linspace(c_from, c_to, number_of_cs)
    fig, ax = plt.subplots()

    cs = []
    points_list = []
    for c in c_list:
        points = stable_points(c, error=error, start_loops=start_loops)
        points_list.extend(points)
        cs.extend([c] * len(points))
    ax.plot(cs, points_list, 'bo', markersize=0.1)
    fig.show()


if __name__ == '__main__':
    plot_stable_points(3.57, 3.585, 0.0001, 1000, 1000)
    stable_p = stable_points(c=3.5822, x=0.5, start_loops=100000,
                             error=0.01)
    print(len(stable_p))
