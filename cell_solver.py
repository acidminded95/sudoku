from random import choice
from funcs import get_cols, check_box, nums

class Cell_Solver():
    def __init__(self, row, col, grid, verbose=0):
        self.row = row
        self.col = col
        self.grid = grid
        self.cols = get_cols(self.grid)
        self.box = check_box(self.row, self.col, self.grid)
        self.attempt = 0
        self.options = nums.copy()
        self.filter_options(self.grid)

        if verbose:
            print(f'\n\nInitialized: {self} \n Original options: {self.options}')

    def __str__(self) -> str:
        return f'Cell solver for cell located at: row {self.row}, column {self.col}'

    def reset_solver(self, grid):
        self.grid = grid
        self.cols = get_cols(self.grid)
        self.box = check_box(self.row, self.col, self.grid)
        self.attempt = 0
        self.options = nums.copy()
        self.filter_options(grid)

    def filter_options(self, grid, verbose=0):
        if verbose:
            verbose-=1
        for x in nums:
            if x in self.options:
                cols = get_cols(grid)
                box = check_box(self.row, self.col, grid)
                if verbose:
                    print(f'Checking option: {x}')
                if x in grid[self.row]:
                    if verbose:
                        print(f'Removing {x} as it is already in row: {self.grid[self.row]}')
                    self.options.remove(x)
                elif x in cols[self.col]:
                    if verbose:
                        print(f'Removing {x} as it is already in column: {self.cols[self.col]}')
                    self.options.remove(x)
                elif x in box:
                    if verbose:
                        print(f'Removing {x} as it is already in box: {self.box}')
                    self.options.remove(x)
                else:
                    if verbose:
                        print(f'Option {x} is viable!')
        if verbose:
            print(f'Options after filter: {self.options}')

    def select_attempt(self, grid, verbose=0):
        if verbose:
            verbose-=1
            print(f'\n\n({self.row},{self.col})----Selecting attempts----\n--Options (before attempt filter): {self.options}\n\n')
        self.filter_options(grid, verbose=verbose)

        try:
            self.attempt = choice(self.options)
            self.options.remove(self.attempt)
            if verbose:
                print(f'\nCurrent attempt for cell ({self.row}{self.col}) is {self.attempt}. Remaining options: {self.options}')
            return self.attempt
        except IndexError:
            if verbose:
                print(f'\nOptions for cell ({self.row},{self.col}) were exhausted. Rolling back on main loop.')
            return 'no_suitable_num'