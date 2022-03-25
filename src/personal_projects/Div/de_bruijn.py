"""
De Bruijn is a sequence made to have all other sequences in it. Bad description
"""

from typing import Iterable, Union, Any


def creat_all_possibilities(n, k):
    possibilities = set()
    possibility = [0] * n
    for i in range(k**n):
        i2 = i
        for j in range(n):
            digit = i2 // k**(n-(j+1))
            i2 -= digit*k**(n-(j+1))

            possibility[j] = digit
        possibilities.add(tuple(possibility))
    return possibilities


def de_bruijn_mine(n: int, k: int = 2):
    """
    My own and in no way finished

    Parameters
    ----------
    n
    k

    Returns
    -------

    """
    all_possibilities = creat_all_possibilities(n, k)
    sequence = []
    empty_set = set()
    the_zero_tuple = tuple([0] * n)
    sequence.extend(the_zero_tuple)
    all_possibilities.remove(the_zero_tuple)
    while all_possibilities != empty_set:
        print(sequence)
        new_pos = sequence[-(n-1):]

        while tuple(new_pos) not in all_possibilities:
            new_pos[-1] += 1
        print(tuple(new_pos))

        sequence.append(new_pos[-1])
        all_possibilities.remove(tuple(new_pos))
    return sequence


def de_bruijn(k: Union[Iterable[Any], int], n: int, looping_style: bool =
              True, verbose: bool = False) -> str:
    """de Bruijn sequence for alphabet k
    and subsequences of length n.
    From wikipedia.
    """
    # Two kinds of alphabet input: an integer expands
    # to a list of integers as the alphabet..
    if isinstance(k, int):
        alphabet = list(map(str, range(k)))
    else:
        # While any sort of list becomes used as it is
        alphabet = k
        k = len(k)

    a = [0] * k * n
    sequence = []
    def db(t, p, depth):
        if verbose:
            print(f'!\n\tDepth {depth} in function with t: {t}, p: {p}\n\t'
                  f'a: {a}, sequence: {sequence}')
        if t > n:  # 0
            if n % p == 0:  # 0.0
                sequence.extend(a[1: p + 1])
                if verbose:
                    print(f'0.0\n\t sequence extended with {a[1: p + 1]}, '
                          f'from 1 to {p+1}')
            else:  # 0.1      just for printing
                if verbose:
                    print(f'0.1')
        else:  # 1
            if verbose:
                print(f'1\n\t a[t]: {a[t]} a[t-p]: {a[t-p]}')
            a[t] = a[t - p]
            db(t + 1, p, depth + 1)
            for j in range(a[t - p] + 1, k):
                if verbose:
                    print(f'x\n\tDepth {depth} in function with t: {t}, p: {p}'
                          f'\n\ta: {a}, sequence: {sequence}')
                    print(f'j: {j} from {a[t-p]+1} to {k}')
                a[t] = j
                db(t + 1, t, depth + 1)

    db(1, 1, 1)
    if looping_style is True:
        return "".join(alphabet[i] for i in sequence)
    else:
        sequence_start = sequence[:n-1]
        sequence.extend(sequence_start)
        return "".join(alphabet[i] for i in sequence)


if __name__ == '__main__':
    print(de_bruijn(2, 2, False))
