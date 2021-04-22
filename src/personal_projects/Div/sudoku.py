import numpy as np

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
        for l in range(low_j, low_j + 3):
            number = sud_mat[k, l]
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


def solve_sudoku_count_sol(sud_mat, stopping_point=30, count=0):
    for i in range(9):
        for j in range(9):
            if sud_mat[i, j] == 0:
                pos_num = possible_numbers(sud_mat, i, j)
                for number in pos_num:
                    sud_mat[i, j] = number
                    count = solve_sudoku_count_sol(sud_mat, stopping_point=stopping_point, count=count)
                sud_mat[i, j] = 0
                return count
    count += 1
    if count > stopping_point:
        raise RuntimeError('Too many solutions')
    print(f'\tFound {count} solutions so far')
    return count


def create_sudoku_and_solution(number_of_prefilled=30, max_n_solutions=1,
                               one_sol=False, seed=None):
    """
    If one_sol is True then the number of prefilled will increase until there is just one solution
    """
    rng = np.random.default_rng(seed=seed)
    num_sol = -1
    n_try = 0
    while num_sol > max_n_solutions or num_sol < 1:
        sud_mat = np.zeros((9, 9), int)
        for _ in range(number_of_prefilled):
            coordinates = rng.integers(9, size=2)
            possibillities = possible_numbers(sud_mat, coordinates[0],
                                              coordinates[1])
            while sud_mat[coordinates[0], coordinates[1]] != 0 or len(
                    possibillities) == 0:
                coordinates = rng.integers(9, size=2)
                possibillities = possible_numbers(sud_mat, coordinates[0],
                                                  coordinates[1])
            sud_mat[coordinates[0], coordinates[1]] = rng.choice(
                list(possibillities))
        try:
            print('Trying to solve')
            num_sol = solve_sudoku_count_sol(sud_mat,
                                             stopping_point=max_n_solutions)
        except RuntimeError:
            num_sol = -1
        n_try += 1
        print(f'n_try: {n_try}, num_sol: {num_sol}')

    # ---This part is extra
    if one_sol is True:
        while num_sol != 1:
            print('Resetting to find one solution')
            sud_mat_2 = sud_mat.copy()
            while num_sol > 1:
                while sud_mat_2[coordinates[0], coordinates[1]] != 0 or len(
                        possibillities) == 0:
                    coordinates = rng.integers(9, size=2)
                    possibillities = possible_numbers(sud_mat_2,
                                                      coordinates[0],
                                                      coordinates[1])
                print(f'\tAdding a number')
                sud_mat[coordinates[0], coordinates[1]] = rng.choice(
                    list(possibillities))

    # ---This part is extra

    sol_sud_mat = solve_sudoku(sud_mat)
    return sud_mat, sol_sud_mat, num_sol


if __name__ == '__main__':
    sudok, sol_sudok, num = create_sudoku_and_solution(25, max_n_solutions=20,
                                                       one_sol=True)
    print(sudok)
    print(sol_sudok[0])
    print(num)