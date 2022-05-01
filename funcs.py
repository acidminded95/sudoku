def get_cols(grid):
    cols = []
    for i in range (0,9):
        col = []
        for row in grid:
            col.append(row[i])
        cols.append(col)
    return cols


def check_box(row, col, grid):
    box = []
    if row<3:
        if col<3:
            for i in range(0,3):
                box.append(grid[i][0:3])
        elif col<6:
            for i in range(0,3):
                box.append(grid[i][3:6])
        else:  
            for i in range(0,3):
                box.append(grid[i][6:9])
    elif row<6:
        if col<3:
            for i in range(3,6):
                box.append(grid[i][0:3])
        elif col<6:
            for i in range(3,6):
                box.append(grid[i][3:6])
        else:  
            for i in range(3,6):
                box.append(grid[i][6:9])
    else:
        if col<3:
            for i in range(6,9):
                box.append(grid[i][0:3])
        elif col<6:
            for i in range(6,9):
                box.append(grid[i][3:6])
        else:  
            for i in range(6,9):
                box.append(grid[i][6:9])
    box = (box[0] + box[1] + box[2])
    return box


def is_grid_full(grid):
    for row in range(0,9):
        for col in range(0,9):
            if grid[row][col]==0:
                return False
    return True


def is_grid_ok(grid):
    cols = get_cols(grid)
    for row in grid:
        if len(set(row)) != 9:
            return(f'Oops, something went wrong. There are not 9 different values in row {row}.\nGrid rows: {grid}\nGrid cols: {cols}')
    for col in cols:
        if len(set(col)) != 9:
            return(f'Oops, something went wrong. There are not 9 different values in col {col}.\nGrid rows: {grid}\nGrid cols: {cols}')
    box_roots = [[0,0,grid],[0,3,grid],[0,6,grid],[3,0,grid],[3,3,grid],[3,6,grid],[6,0,grid],[6,3,grid],[6,6,grid]]
    boxes = []
    for box in box_roots:
        boxes.append(check_box(box[0],box[1],box[2]))
    for box in boxes:
        if len(set(box)) != 9:
            return(f'Oops, something went wrong. There are not 9 different values in box.\nGrid rows: {grid}\nGrid cols: {cols}')
    return True

def exhaust_options(puzzle_generator, completed_solvers, remaining_solvers, removable, amount_of_removables, list_of_rejected, verbose=0):
    ignoring=True
    run_count = 1
    if amount_of_removables == 2:
        first = removable[0]
        second = removable[1]
    # Create new puzzle with completed solvers and ignoring the selected attempt at first solver with more options available
    # Loop through remaining solvers until another solution is found or there are no more remaining solvers
    while remaining_solvers != []:
        run_count+=1             
        if verbose:
            print(f'\nRun # {run_count} for puzzle # {puzzle_generator.id}.Creating new puzzle from previous puzzle, but with cells that had no remaining options solved.')
        
        new_puzzle = []
        for row in puzzle_generator.puzzle:
            new_puzzle.append(row.copy())
        for solver in completed_solvers:
            new_puzzle[solver.row][solver.col] = solver.attempt
        
        if verbose:
            print(f'\nHere is the puzzle proposed to check for a solution in run # {run_count} for puzzle # {puzzle_generator.id}:\n   0  1  2  3  4  5  6  7  8\n')
            for x in range (0,9):
                print(f'{x} {new_puzzle[x]}')
            print(f'\n\nThis is the recieved list of remaining solvers at run # {run_count} ({len(remaining_solvers)}):')
            for solver in remaining_solvers:
                print(f'# {remaining_solvers.index(solver)} Solver cell: ({solver.row},{solver.col}) Attempt: {solver.attempt} Options: {solver.options}')
        
        # Try to solve the new puzzle ignoring the attempt at first solver with more options if the ignoring flag is true
        # If the 'ignoring' flag is False,this solves the new puzzle trying to find remaining options
        if verbose:
            print('\n\nStarting search for another solution..')
        if ignoring:
            new_run = puzzle_generator.look_for_more_solutions(new_puzzle, expected_solution=puzzle_generator.grid, run=run_count, verbose=verbose, ignore=remaining_solvers[0])
        else:
            new_run = puzzle_generator.look_for_more_solutions(new_puzzle, expected_solution=puzzle_generator.grid, run=run_count, verbose=verbose) 
        if verbose:
            print(f'\nFinished run # {run_count} for another solution. Result: {new_run}')

        if new_run == 'no_solution_found':
            if verbose:
                print(f'There were no alternative solutions found in run # {run_count}.\n Moving first remaining solver to solved solvers and testing for more options..')
            completed_solvers.append(remaining_solvers[0])
            remaining_solvers.pop(0)

            ignoring = False

        elif new_run[0] == 'no_options_left':
            #remaining_solvers = new_run[2]
            return amount_of_removables
            #####solvable_cells +=2

        elif new_run[0] == 'another_solution_found':
            if verbose:
                solvers = new_run[1]
                alternative_solution = []
                for row in new_puzzle:
                    alternative_solution.append(row.copy())
                for solver in solvers:
                    alternative_solution[solver.row][solver.col] = solver.attempt
                print('Original grid:\t\t\t\tPuzzle:\t\t\t\t\tAlternative solution:')
                for x in range(0,9):
                    print(f'{puzzle_generator.grid[x]}\t{puzzle_generator.puzzle[x]}\t{alternative_solution[x]}')

            if amount_of_removables == 2:
                list_of_rejected.append(removable[0])
                list_of_rejected.append(removable[1])
                puzzle_generator.puzzle[first[0]][first[1]] = puzzle_generator.grid[first[0]][first[1]]
                puzzle_generator.puzzle[second[0]][second[1]] = puzzle_generator.grid[second[0]][second[1]]
                if verbose:
                    print(f'\nCells ({first[0]},{first[1]}) & ({second[0]},{second[1]}) were not removed from puzzle')
            else:
                list_of_rejected.append(removable)
                puzzle_generator.puzzle[removable[0]][removable[1]] = puzzle_generator.grid[removable[0]][removable[1]]
                if verbose:
                    print(f'\nCell ({removable[0]},{removable[1]}) was not removed from puzzle')
            #remaining_solvers = []
            return 0
            
        elif new_run[0] == 'options_remaining':
            ignoring = True
            for completed_solver in new_run[1]:
                completed_solvers.append(completed_solver)
            remaining_solvers = new_run[2]
    #return amount_of_removables



# Some constants needed throughout the app

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
level_dict = {'easy': [40, 41, 42, 43, 44, 45],'medium': [35, 36, 37, 38, 39], 'hard': [30, 31, 32, 33, 34]}
#level_dict = {'beginner': [40, 41, 42, 43, 44, 45],'easy': [35, 36, 37, 38, 39], 'medium': [30, 31, 32, 33, 34], 'hard': [25, 26, 27, 28, 29], 'expert': [20, 21, 22, 23, 24]}
