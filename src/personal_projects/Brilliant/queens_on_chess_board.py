from pprint import pprint


class QueensOfChess:
    """
    A class that solves the eight queens problem
    Using the
    """
    def __init__(self, dim=8):
        self.dim = dim  # x, y and number of queens
        self.queen = 'Q'
        self.open = 'O'
        self.taken = 'X'

        self.tiles = set()
        for n in range(self.dim):
            for m in range(self.dim):
                self.tiles.add((n, m))

        self.open_tiles = set()
        self.taken_tiles = set()
        self.queen_tiles = set()

        self.board = {}

        self.reset_board_and_tiles()

        self.solutions = []
        self.num_sol = 0

    def reset_tiles(self):
        self.open_tiles = self.tiles.copy()
        self.taken_tiles = set()
        self.queen_tiles = set()

    def reset_board(self):
        self.board = {}

    def reset_board_and_tiles(self):
        self.reset_tiles()
        self.reset_board()

    def place_queen(self, loc):
        if loc in self.open_tiles:
            self.update_all_tiles(loc)
        else:
            raise ValueError('The location is not open')

    def place_queens(self, list_of_locs):
        for loc in list_of_locs:
            self.place_queen(loc)

    def reset_and_place_queens(self, list_of_locs):
        self.reset_board_and_tiles()
        self.place_queens(list_of_locs)

    def update_board(self):
        # Makes the whole board open
        for n in range(self.dim):
            for m in range(self.dim):
                self.board[(n, m)] = self.open

        # Fills in the taken tiles
        for loc in self.taken_tiles:
            self.board[loc] = self.taken

        # Fills in the queen tiles
        for loc in self.queen_tiles:
            self.board[loc] = self.queen

    def update_taken_tiles(self, loc):
        """

        Parameters
        ----------
        loc
            The location of the queen

        Returns
        -------

        """
        loc_row = loc[0]
        loc_col = loc[1]

        # Rows and cols
        for i in range(self.dim):
            self.taken_tiles.add((loc_row, i))
            self.taken_tiles.add((i, loc_col))

        # Diagonal
        for i in range(self.dim):
            locs = [(loc_row - i, loc_col - i), (loc_row - i, loc_col + i),
                    (loc_row + i, loc_col - i), (loc_row + i, loc_col + i)]
            for loc_ in locs:
                if loc_ in self.tiles:
                    self.taken_tiles.add(loc_)

        self.taken_tiles = self.taken_tiles - self.queen_tiles

    def update_open_tiles(self):
        self.open_tiles = self.open_tiles - self.taken_tiles - self.queen_tiles

    def update_queen_tiles(self, loc):
        self.queen_tiles.add(loc)

    def update_all_tiles(self, loc):
        self.update_queen_tiles(loc)
        self.update_taken_tiles(loc)
        self.update_open_tiles()

    def print_board(self):
        self.update_board()
        for n in range(self.dim - 1, -1, -1):
            print([self.board[(m, n)] for m in range(self.dim)])
        print('\n')

    def find_solutions(self, print_solutions=False):
        self.recursion_queens(self.dim - 1, print_solutions)
        return self.solutions

    def recursion_queens(self, col, print_solutions=False):
        # print(f'In recursion for the {col}th queen')
        queens_uptil_now = self.queen_tiles.copy()
        if col >= 0:
            col -= 1
            for i in range(self.dim):
                self.reset_and_place_queens(queens_uptil_now)
                loc = (i, col + 1)
                if loc in self.open_tiles:
                    self.place_queen(loc)
                    self.recursion_queens(col, print_solutions)
        else:
            if len(self.queen_tiles) == self.dim:
                self.solutions.append(self.queen_tiles)
                self.num_sol += 1
                if print_solutions:
                    print(f'The {self.num_sol}. solution for board {self.dim} '
                          f'\n')
                    self.print_board()
                self.reset_and_place_queens(queens_uptil_now)


def find_number_of_solutions_for_different_sizes(max_size_board):
    solutions_dict = {}
    for board_size in range(1, max_size_board + 1):
        q = QueensOfChess(board_size)
        sol = q.find_solutions(True)
        print(f'Board of size {board_size} has {len(sol)} solutions')
        solutions_dict[str(board_size)] = len(sol)
    return solutions_dict


if __name__ == '__main__':
    n = 6
    q = QueensOfChess(n)
    sol = q.find_solutions(True)
    print(f'{n}x{n} with {n} queens has {len(sol)} solutions.')

