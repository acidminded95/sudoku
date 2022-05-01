from cell_solver import Cell_Solver, get_cols, choice
from funcs import level_dict, exhaust_options

class Puzzle_Generator():
    def __init__(self, difficulty, verbose=0, id=0):
        self.difficulty = difficulty
        self.id = id 
        self.grid = []
        self.puzzle = []
        
        for i in range(9):
            self.grid.append([0 for x in range(9)])
        self.grid = self.solve_grid(self.grid)[0]

        for row in self.grid:
            self.puzzle.append(row.copy())
        self.get_puzzle_ready(verbose=verbose)

    def generate_solvers(self, grid):
        solvers = []
        for row in range(0,9):
            for col in range(0,9):
                if grid[row][col] == 0:
                    solvers.append(Cell_Solver(row, col, grid))
        return solvers
                       
    def solve_grid(self, grid, verbose=0, ignore=None):
        if verbose:
            verbose-=1

        solved_grid =[]
        for row in grid:
            solved_grid.append(row.copy())

        solvers = self.generate_solvers(solved_grid)

        if ignore:
            if verbose:
                print(f'\nIgnoring option {ignore.attempt} in solver for cell ({ignore.row},{ignore.col}) if it is among its options.')
            for solver in solvers:
                if solver.row == ignore.row:
                    if solver.col == ignore.col:
                        if verbose:
                            print(f'Current options for cell ({solver.row},{solver.col}): {solver.options} Removing {ignore.attempt} if present..')
                        if ignore.attempt in solver.options:
                            solver.options.remove(ignore.attempt)
                            if verbose:
                                print(f'Options left at cell ({solver.row},{solver.col}): {solver.options}')

        solvers_count = len(solvers)
        solvers.sort(key= lambda x: len(x.options))
        
        if verbose:
            print(f'\nSolving grid with {solvers_count} empty spaces:\n')
            sorted = {}
            for x in solvers:
                sorted[f'({x.row},{x.col})'] = x.options
            if verbose:
                print(f'Dict of sorted solvers with their options: {sorted}')

        # Loop through the solvers and try to get a solution from them
        current_solver = 0
        while (current_solver < solvers_count):
            solver = solvers[current_solver]
            attempt = solver.select_attempt(solved_grid, verbose)

            if attempt != 'no_suitable_num':
                    solved_grid[solver.row][solver.col] = attempt
                    current_solver += 1
            else:
                if current_solver==0:
                    return 'no_solution_found'
                else:
                    solved_grid[solver.row][solver.col] = 0
                    solver.reset_solver(grid)
                    current_solver -= 1
        return solved_grid, solvers
    
    def look_for_more_solutions(self, puzzle, expected_solution, run, verbose=0, ignore=None):
        if verbose:
            verbose -=1
            print(f'Trying to solve puzzle. Run # {run}')
        x = self.solve_grid(puzzle, verbose, ignore=ignore)
        if x == 'no_solution_found':
            return 'no_solution_found'
        solution, returned_solvers = x[0], x[1]
        if verbose:
            print(f'\n\nFinished run # {run}.')
        if solution == expected_solution:
            if verbose:
                print('The solution was as expected')
                print(f'{len(returned_solvers)} solvers were returned:\n')
            
            solvers_with_more_options = []
            solver_count = 0
            for solver in returned_solvers:
                if verbose:
                    print(f'Solver # {solver_count}: ({solver.row},{solver.col}). Current attempt: {solver.attempt}. Options left: {solver.options}')
                if solver.options != []:
                    solvers_with_more_options.append(solver)                  
                solver_count+=1

            if solvers_with_more_options == []:
                completed_solvers = returned_solvers
                solvers_remaining = solvers_with_more_options
                if verbose:
                    print('\nThere are no options left in the solvers. Proceeding to next removal.')                    
                return 'no_options_left', completed_solvers, solvers_remaining
            else:
                if verbose:
                    print('\nThere are options remaining in the solvers.. Need to look for a another solution.')
                first_solver_remaining = returned_solvers.index(solvers_with_more_options[0])
                if verbose:
                    print(f'The first solver with more solutions is at index: {first_solver_remaining}. Dividing list of solvers...\n')
                completed_solvers = returned_solvers[:first_solver_remaining]
                solvers_remaining = returned_solvers[first_solver_remaining:]
                return 'options_remaining', completed_solvers, solvers_remaining
        else:
            if verbose:
                print('Another solution was found!')
            return 'another_solution_found', returned_solvers
    
    def get_puzzle_ready(self, verbose=0):
        if verbose:
            #verbose-=1
            print(f'\n** GETTING PUZZLE # {self.id} READY **\n')

        # Determine the amount of hints in the puzzle (numbers in the grid) according to difficulty
        total_hints = choice(level_dict[self.difficulty])
        if verbose:
            print(f'Difficulty: {self.difficulty.capitalize()}\nNumber of hints: {total_hints} (random number selected from {level_dict[self.difficulty]})')
            print(f'Number of solvable cells needed: {81-total_hints}')

        # Create symmetric pairs of cells in the grid in order to remove them one by one, checking each time if there's still a unique solution, to end up with a symmetric puzzle
        symmetric_pairs = []
        for i in range(40):
            symmetric_pairs.append([[i//9,i%9],[(80-i)//9,(80-i)%9]])
        remaining_cells = []
        rejected_cells = []

        # Start selecting the solvable cells
        solvable_cells = 0

        # Adds the center cell of the grid as a solvable cell if the total amount of solvable cells is an odd number
        # (if total_hints is even, the total of solvable cells must be odd as their sum is 81)
        if total_hints%2 ==0:
            self.puzzle[4][4] = 0
            solvable_cells +=1

        # Check if a pair of symmetric cells can be removed without leading to a puzzle with multiple solutions. Loops until reaching desired amount of solvable cells
        while (total_hints+solvable_cells) < 81:
            try:
                if verbose:
                    print(f'\n\n--------------Solvable cells until now: {solvable_cells}/{81-total_hints}')
                
                pair_to_remove = choice(symmetric_pairs)
                first, second = pair_to_remove[0], pair_to_remove[1]
                if verbose:
                    print(f'\nAttempting to remove cells ({first[0]},{first[1]}) & ({second[0]},{second[1]})\n')

                self.puzzle[first[0]][first[1]] = 0
                self.puzzle[second[0]][second[1]] = 0
                
                if verbose:
                    # Display the puzzle without the selected pair of symmetrical cells
                    print(f'Puzzle # {self.id} progress ({solvable_cells+2} empty spaces) for puzzle # {self.id}:\n   0  1  2  3  4  5  6  7  8\n')
                    for x in range (0,9):
                        print(f'{x} {self.puzzle[x]}')
                
                run = self.look_for_more_solutions(self.puzzle, expected_solution=self.grid, run=1, verbose=verbose)
                
                if verbose:
                    print(f'\nFinished search for first solution for puzzle # {self.id}. Result: {run[0]}')

                if run == 'no_solution_found':
                    print('An error has ocurred: No solution was found at first attempt to solve the puzzle')
                elif run[0] == 'no_options_left':
                    solvable_cells +=2
                elif run[0] == 'another_solution_found':
                    if verbose:
                        solvers = run[1]
                        alternative_solution = []
                        for row in self.puzzle:
                            alternative_solution.append(row.copy())
                        for solver in solvers:
                            alternative_solution[solver.row][solver.col] = solver.attempt
                        print(f'An alternative solution to the puzzle was found.\n\nOriginal grid:\t\t\tPuzzle:\t\t\tAlternative solution:')
                        for x in range(0,9):
                            print(f'{self.grid[x]}\t{self.puzzle[x]}\t{alternative_solution[x]}')
                    
                    remaining_cells.append(pair_to_remove[0])
                    remaining_cells.append(pair_to_remove[1])
                    self.puzzle[first[0]][first[1]] = self.grid[first[0]][first[1]]
                    self.puzzle[second[0]][second[1]] = self.grid[second[0]][second[1]]
                    if verbose:
                        print(f'\nCells ({first[0]},{first[1]}) & ({second[0]},{second[1]}) were not removed from puzzle')

                elif run[0] == 'options_remaining':
                    solvable_cells+= (exhaust_options(self, run[1], run[2], pair_to_remove, 2, remaining_cells, verbose=verbose))
                    
                symmetric_pairs.remove(pair_to_remove)
                if verbose:
                    print(f'\nOptions from pairs_to_remove left: {len(symmetric_pairs)}\n\n')
            
            except IndexError:
                try:
                    #if verbose:
                    print(f'No more symmetric pairs left. Attempting to remove individual cells from rejected pairs to complete puzzle # {self.id}.')
                    
                    if verbose:
                        print(f'There are {len(remaining_cells)} single cells left to try and remove..')
                    cell_to_remove = choice(remaining_cells)
                    if verbose:
                        print(f'\nAttempting to remove individual cell ({cell_to_remove[0]},{cell_to_remove[1]})\n')
                    self.puzzle[cell_to_remove[0]][cell_to_remove[1]] = 0
                
                    if verbose:
                        # Display the puzzle without the selected cell
                        print(f'Puzzle # {self.id} progress ({solvable_cells+1} empty spaces):\n   0  1  2  3  4  5  6  7  8\n')
                        for x in range (0,9):
                            print(f'{x} {self.puzzle[x]}')
                    
                    run_count = 1
                    run = self.look_for_more_solutions(self.puzzle, expected_solution=self.grid, run=run_count, verbose=verbose)
                    if verbose:
                        print(f'\nFinished search for first solution for puzzle # {self.id}. Result: {run[0]}')

                    if run == 'no_solution_found':
                        print('An error has ocurred: No solution was found at first attempt to solve the puzzle')
                    
                    elif run[0] == 'no_options_left':
                        solvable_cells +=1
                    
                    elif run[0] == 'another_solution_found':
                        if verbose:
                            solvers = run[1]
                            alternative_solution = []
                            for row in self.puzzle:
                                alternative_solution.append(row.copy())
                            for solver in solvers:
                                alternative_solution[solver.row][solver.col] = solver.attempt
                            print(f'An alternative solution to the puzzle was found.\n\nOriginal grid:\t\t\tPuzzle:\t\t\tAlternative solution:')
                            for x in range(0,9):
                                print(f'{self.grid[x]}\t{self.puzzle[x]}\t{alternative_solution[x]}')

                        self.puzzle[cell_to_remove[0]][cell_to_remove[1]] = self.grid[cell_to_remove[0]][cell_to_remove[1]]
                        if verbose:
                            print(f'\nCell ({cell_to_remove[0]},{cell_to_remove[1]}) was not removed from puzzle')

                    elif run[0] == 'options_remaining':
                        solvable_cells+=(exhaust_options(self, run[1], run[2], cell_to_remove, 1, rejected_cells, verbose=verbose))

                    remaining_cells.remove(cell_to_remove)
                    if verbose:
                        print(f'\nOptions from remaining_cells left: {len(remaining_cells)}\n\n')
                except IndexError:
                    print('Could not remove desired number of cells. Returning puzzle with maximum number of cells removed.')
                    solvable_cells = 81 - total_hints


        if verbose:
            print('\n** PUZZLE READY **\n')