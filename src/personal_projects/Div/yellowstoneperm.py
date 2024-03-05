import numpy as np
import matplotlib.pyplot as plt


def gcd(a, b):
    if a == 0:
        return b
    elif b == 0:
        return a
    else:
        if b > a:
            a, b = b, a

        r = a % b
        gcd_num = gcd(b, r)
        return gcd_num


def yellowstone(n=1000):
    list_of_possibles = [i for i in range(1, n+1)]
    perm = []
    for i in range(3):
        perm.append(list_of_possibles.pop(0))
    while True:
        found_number = False
        for index, elem in enumerate(list_of_possibles):
            if gcd(elem, perm[-1]) == 1 and gcd(elem, perm[-2]) != 1:
                perm.append(list_of_possibles.pop(index))
                found_number = True
                break
        if not found_number:
            break
    return perm


def yellowstone_with_plot(n=1000):
    permutations = yellowstone(n)
    x_axis = [i for i in range(1, len(permutations)+1)]
    plt.plot(x_axis, permutations)
    plt.show()


if __name__ == '__main__':
    yellowstone_with_plot(100000)


