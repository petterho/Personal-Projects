from math import pi


def farey_alg(n, largest_divisor=100):
    """
    This started simple, but then i figured it could be really close and
    then come farther away again, so i changed it to a much more complicated
    one.

    It can still gives a closing range, but it now gives the best
    approximate it has come across, not the last. This means if the n is
    close to, but slightly over 1/2 it gives 1/2 until the upper bound i
    closer than the 1/2 is.
    
    Parameters
    ----------
    n: float
    largest_divisor: int

    Returns
    -------

    """
    if n > 1:
        n = n - int(n)

    small_dividend = 0
    small_divisor = 1

    large_dividend = 1
    large_divisor = 1

    next_divisor = small_divisor + large_divisor

    best_dividend = 0
    best_divisor = 0
    best_error = 1

    while next_divisor <= largest_divisor:
        new_dividend = small_dividend + large_dividend
        new_divisor = next_divisor
        new_approx = new_dividend / new_divisor

        if new_approx == n:
            range_ = (small_dividend / small_divisor,
                      large_dividend / large_divisor)
            return new_dividend, new_divisor, range_
        elif new_approx < n:
            small_dividend = new_dividend
            small_divisor = new_divisor
        else:
            large_dividend = new_dividend
            large_divisor = new_divisor

        new_error = abs(n - new_approx)
        if new_error < best_error:
            best_dividend = new_dividend
            best_divisor = new_divisor
            best_error = new_error

        print(new_dividend, new_divisor, new_approx)
        next_divisor = small_divisor + large_divisor

    range_ = (small_dividend / small_divisor,
              large_dividend / large_divisor)
    return best_dividend, best_divisor, range_


def halving_alg(n, largest_divisor=100):
    if n > 1:
        n = n - int(n)

    small_dividend = 0
    large_dividend = 1

    next_divisor = 2

    best_dividend = 0
    best_divisor = 0
    best_error = 1

    while next_divisor <= largest_divisor:
        small_dividend *= 2
        large_dividend *= 2

        new_dividend = (small_dividend + large_dividend) / 2
        new_approx = new_dividend / next_divisor  # Just any of them will do

        if new_approx == n:
            range_ = (small_dividend / (next_divisor / 2),
                      large_dividend / (next_divisor / 2))
            return int(new_dividend), next_divisor, range_
        elif new_approx < n:
            small_dividend = new_dividend
        else:
            large_dividend = new_dividend

        new_error = abs(n - new_approx)
        if new_error < best_error:
            best_dividend = new_dividend
            best_divisor = next_divisor
            best_error = new_error

        print(new_dividend, next_divisor, new_approx)
        next_divisor *= 2

    range_ = (small_dividend / (next_divisor / 2),
              large_dividend / (next_divisor / 2))
    return int(best_dividend), best_divisor, range_


if __name__ == '__main__':
    n_ = 0.701
    largest_divisor0 = 1000
    sol_halving = halving_alg(n_, largest_divisor0)
    sol_farey = farey_alg(n_, largest_divisor0)
    print('-----------------------------------------')
    print(f'Dividend: {sol_halving[0]:7}, divisor: {sol_halving[1]:7}, '
          f'approximation: {sol_halving[0] / sol_halving[1]:10}, range: '
          f'{sol_halving[2][0]:7} to {sol_halving[2][1]:7}')
    print(f'Dividend: {sol_farey[0]:7}, divisor: {sol_farey[1]:7}, '
          f'approximation: {sol_farey[0] / sol_farey[1]:11}, range: '
          f'{sol_farey[2][0]:7} to {sol_farey[2][1]:7}')
    the_matt_parker_part = """
    matt_parker_number = 11**6 / 13
    matt_parker_number_d_pi = matt_parker_number / pi
    the_wholes = int(matt_parker_number_d_pi)
    the_rest = matt_parker_number_d_pi - the_wholes
    approx = farey_alg(the_rest, 10000)
    divisor = approx[1]
    dividend = approx[0] + the_wholes * divisor
    print(matt_parker_number * divisor / dividend)
    print(pi)
    """
