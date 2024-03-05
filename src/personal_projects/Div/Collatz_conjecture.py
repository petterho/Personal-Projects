import matplotlib.pyplot as plt
import numpy as np
import igraph
from igraph import Graph, EdgeSeq
import cairo

def function_collatz(n):
    """
    Can't handle integers lower than 1

    Parameters
    ----------
    n

    Returns
    -------

    """
    if n == 1:
        return 1

    if n % 2 == 0:
        return n // 2

    return n * 3 + 1


def collatz_verbose(n):
    print(n)
    while n != 1:
        n = function_collatz(n)
        print(n)


def collatz_count(n):
    """
    Counts including 1

    Parameters
    ----------
    n

    Returns
    -------

    """
    count = 1
    while n != 1:
        n = function_collatz(n)
        count += 1
    return count


def collatz_up_to(g):
    counts = np.zeros(g, dtype=np.int64)
    for i in range(g):
        counts[i] = collatz_count(i + 1)
    return counts


def plot_counts(counts):
    fig, ax = plt.subplots()
    ax.plot(counts)
    fig.show()


def collatz_complete_mapping(upper_bound, verbose=False):
    mapping_dict = {}
    for i in range(1, upper_bound + 1):
        n = i
        if verbose:
            print(f'Starting from {i}:')
        while n not in mapping_dict.keys():
            collatz_of_n = function_collatz(n)
            mapping_dict[n] = collatz_of_n
            n = collatz_of_n
            if verbose:
                print(f'    Now at {n}')
        if verbose:
            print(f'{i} mapped to {n}, which was known.')
    return mapping_dict


def collatz_level_mapping(mapping_dict, verbose=False):
    level_mapping_dict = {}
    for key in mapping_dict.keys():
        level = collatz_count(key)
        if verbose:
            print(f'Updating level {level}')
        if level in level_mapping_dict:
            level_mapping_dict[level].add(key)
        else:
            level_mapping_dict[level] = {key}
    return level_mapping_dict


def next_level_collatz(n):
    """
    Forsøk på å produsere for hvert nivå, men feila
    Parameters
    ----------
    n

    Returns
    -------

    """
    double_number = 2 * n
    other_number = 0
    if (n - 1) % 3 == 0:
        other_number = int((n - 1) / 3)
    return double_number, other_number


def collatz_math_mapping(upper_level):
    mapping_dict = {}
    mapping_dict[1] = [1]
    for i in range(1, upper_level + 1):
        tuple_ = next_level_collatz(i)
        mapping_dict[i] = tuple_
    return mapping_dict


def collatz_test_with_plot(n):
    co = collatz_up_to(n)
    plot_counts(co)
    index_max = np.argmax(co)
    print(f'The max is {co[index_max]} and the number that got it was '
          f'{index_max + 1}')


def main_func():
    print(collatz_math_mapping(5))


def tree():
    pass


def plot_level_tree():
    mapping = collatz_complete_mapping(20, verbose=False)
    level_mapping = collatz_level_mapping(mapping, verbose=False)
    mydict = {'apple': ['pear', 'peach'], 'pear': ['peach']}
    g = Graph.ListDict(mydict)
    layout = g.layout()
    fig, ax = plt.subplots()
    #ax.plot([0, 1], [0, 2])
    #igraph.plot(g, target=ax)
    fig.show()


def check_matplotlib():
    fig, ax = plt.subplots()


if __name__ == '__main__':
    #main_func()
    #plot_level_tree()
    check_matplotlib()
    a = """
    import igraph
    from igraph import Graph, EdgeSeq

    nr_vertices = 25
    v_label = list(map(str, range(nr_vertices)))
    G = Graph.Tree(nr_vertices, 2)  # 2 stands for children number
    lay = G.layout('rt')

    position = {k: lay[k] for k in range(nr_vertices)}
    Y = [lay[k][1] for k in range(nr_vertices)]
    M = max(Y)

    es = EdgeSeq(G)  # sequence of edges
    E = [e.tuple for e in G.es]  # list of edges

    L = len(position)
    Xn = [position[k][0] for k in range(L)]
    Yn = [2 * M - position[k][1] for k in range(L)]
    Xe = []
    Ye = []
    for edge in E:
        Xe += [position[edge[0]][0], position[edge[1]][0], None]
        Ye += [2 * M - position[edge[0]][1], 2 * M - position[edge[1]][1],
               None]

    labels = v_label

    import plotly.graph_objects as go

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Xe,
                             y=Ye,
                             mode='lines',
                             line=dict(color='rgb(210,210,210)', width=1),
                             hoverinfo='none'
                             ))
    fig.add_trace(go.Scatter(x=Xn,
                             y=Yn,
                             mode='markers',
                             name='bla',
                             marker=dict(symbol='circle-dot',
                                         size=18,
                                         color='#6175c1',  # '#DB4551',
                                         line=dict(color='rgb(50,50,50)',
                                                   width=1)
                                         ),
                             text=labels,
                             hoverinfo='text',
                             opacity=0.8
                             ))
    fig.show()
    """