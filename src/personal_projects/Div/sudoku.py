import numpy as np
from pprint import pprint

sudoku_matrix = np.array([
    [8, 0, 0, 9, 0, 0, 0, 1, 6],
    [0, 0, 9, 0, 0, 8, 0, 0, 0],
    [0, 0, 0, 0, 0, 4, 9, 0, 3],
    [0, 0, 7, 0, 0, 0, 0, 5, 0],
    [0, 0, 0, 0, 6, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 2, 1, 0, 8],
    [3, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 5, 7, 9, 0]
                          ])


def possible_numbers(sud_mat, i, j):
    possible_numb = set([k for k in range(1, 10)])

    for number in sud_mat[i, :]:
        possible_numb.discard(number)
    for number in sud_mat[:, j]:
        possible_numb.discard(number)

    low_i = i - i % 3
    low_j = j - j % 3
    for k in range(low_i, low_i + 3):
        for m in range(low_j, low_j + 3):
            number = sud_mat[k, m]
            possible_numb.discard(number)

    return possible_numb


def solve_sudoku(sud_mat, solutions=None):
    if solutions is None:
        solutions = []

    for i in range(9):
        for j in range(9):
            if sud_mat[i, j] == 0:
                pos_num = possible_numbers(sud_mat, i, j)
                for number in pos_num:
                    sud_mat[i, j] = number
                    solutions = solve_sudoku(sud_mat, solutions)
                sud_mat[i, j] = 0
                return solutions
    solutions.append(sud_mat.copy())
    return solutions


def solve_sudoku_count_sol(sud_mat, stopping_point=30, count=0, verbose=0):
    for i in range(9):
        for j in range(9):
            if sud_mat[i, j] == 0:
                pos_num = possible_numbers(sud_mat, i, j)
                for number in pos_num:
                    sud_mat[i, j] = number
                    count = solve_sudoku_count_sol(sud_mat,
                                                   stopping_point=
                                                   stopping_point,
                                                   count=count)
                sud_mat[i, j] = 0
                return count
    count += 1
    if count > stopping_point:
        raise RuntimeError('Too many solutions')
    if verbose > 2:
        print(f'\tFound {count} solutions so far')
    return count


def add_numbers_till_one_solution(sud_mat, num_sol, rng, max_n_solutions,
                                  number_of_prefilled, verbose=0):
    num_sol_before = num_sol
    number_of_prefilled_before = number_of_prefilled
    reset_counter = 0

    if num_sol == 1:
        return sud_mat, number_of_prefilled, reset_counter

    while num_sol != 1:
        if verbose > 1:
            print(f'Resetting for {reset_counter}th time to find one '
                  f'solution.')
        reset_counter += 1

        num_sol = num_sol_before
        number_of_prefilled = number_of_prefilled_before
        sud_mat_2 = sud_mat.copy()
        while num_sol > 1:
            coordinates = rng.integers(9, size=2)
            possibilities = possible_numbers(sud_mat_2, coordinates[0],
                                             coordinates[1])
            while sud_mat_2[coordinates[0], coordinates[1]] != 0 or len(
                    possibilities) == 0:
                coordinates = rng.integers(9, size=2)
                possibilities = possible_numbers(sud_mat_2,
                                                 coordinates[0],
                                                 coordinates[1])
            sud_mat_2[coordinates[0], coordinates[1]] = rng.choice(
                list(possibilities))
            num_sol = solve_sudoku_count_sol(sud_mat_2,
                                             stopping_point=max_n_solutions,
                                             verbose=verbose)
            number_of_prefilled += 1
            if verbose > 2:
                print(f'{number_of_prefilled} number of prefilled has '
                      f'{num_sol} solutions of {num_sol_before}')
    return sud_mat_2, number_of_prefilled, reset_counter


def create_sudoku_and_solution(number_of_prefilled=30, max_n_solutions=1,
                               one_sol=False, seed=None, verbose=0):
    """
    If one_sol is True then the number of prefilled will increase until there
    is just one solution, resulting in a higher number of prefilled numbers.

    A way to get a precise number of prefills and just one solution is to
    set max_n_solutions to 1.

    This method of creating sudoku is bad for low number of prefilled tiles.
    """
    rng = np.random.default_rng(seed=seed)
    num_sol = -1
    n_try = 0
    reset_counter = 0
    while num_sol > max_n_solutions or num_sol < 1:
        sud_mat = np.zeros((9, 9), int)
        for _ in range(number_of_prefilled):
            coordinates = rng.integers(9, size=2)
            possibilities = possible_numbers(sud_mat, coordinates[0],
                                             coordinates[1])
            while sud_mat[coordinates[0], coordinates[1]] != 0 or len(
                    possibilities) == 0:
                coordinates = rng.integers(9, size=2)
                possibilities = possible_numbers(sud_mat, coordinates[0],
                                                 coordinates[1])
            sud_mat[coordinates[0], coordinates[1]] = rng.choice(
                list(possibilities))
        try:
            num_sol = solve_sudoku_count_sol(sud_mat,
                                             stopping_point=max_n_solutions,
                                             verbose=verbose)
        except RuntimeError:
            num_sol = -1
        n_try += 1
        if verbose > 1:
            print(f'Try number {n_try} to find a suitable matrix has {num_sol}'
                  f' solutions')

    if verbose > 0:
        print(f'Found a suitable matrix in {n_try} tries. This has '
              f'{num_sol} solutions with {number_of_prefilled} prefilled '
              f'numbers')

    if one_sol is True:
        sud_mat, number_of_prefilled, reset_counter = \
            add_numbers_till_one_solution(sud_mat,
                                          num_sol,
                                          rng,
                                          max_n_solutions,
                                          number_of_prefilled,
                                          verbose=verbose)
        num_sol = 1

    sol_sud_mat = solve_sudoku(sud_mat)

    if verbose > 0:
        print(f'Found a sudoku with in {n_try} tries and {reset_counter} '
              f'resets. This has '
              f'{number_of_prefilled} prefilled tiles and '
              f'{num_sol} solutions')

    return sud_mat, sol_sud_mat, num_sol


if __name__ == '__main__':
    sudok, sol_sudok, num = create_sudoku_and_solution(25, max_n_solutions=1,
                                                       one_sol=True,
                                                       verbose=2)
    print('Sudoku:')
    print(sudok)
    print('Solutions')
    pprint(sol_sudok[0])
    print(num)
