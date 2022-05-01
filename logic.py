from random import seed
from puzzle_generator import Puzzle_Generator, choice
from funcs import is_grid_ok

seed(42)

the_trials = {}
amount = 10
for x in range(amount):
    the_trials[x] = Puzzle_Generator('hard', verbose=1, id=x)

dif_sol_count = 0
for x in the_trials:
    print('\n\n')
    print('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    print(f'--------------------------------------------------------------------------------------------Test #{the_trials[x].id+1}------------------------------------------------------------------------------------------------------')
    print('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    print(f'\nSolved Grid:\n   0  1  2  3  4  5  6  7  8\n\n0 {the_trials[x].grid[0]}\n1 {the_trials[x].grid[1]}\n2 {the_trials[x].grid[2]}\n3 {the_trials[x].grid[3]}\n4 {the_trials[x].grid[4]}\n5 {the_trials[x].grid[5]}\n6 {the_trials[x].grid[6]}\n7 {the_trials[x].grid[7]}\n8 {the_trials[x].grid[8]}')
    print(f'\nIs the grid valid (no repeated number in row, column or box)? {is_grid_ok(the_trials[x].grid)}')
    
    print(f'\nPuzzle:\n{the_trials[x].puzzle[0]}\n{the_trials[x].puzzle[1]}\n{the_trials[x].puzzle[2]}\n{the_trials[x].puzzle[3]}\n{the_trials[x].puzzle[4]}\n{the_trials[x].puzzle[5]}\n{the_trials[x].puzzle[6]}\n{the_trials[x].puzzle[7]}\n{the_trials[x].puzzle[8]}')
    solution_attempt = the_trials[x].solve_grid(the_trials[x].puzzle)[0]
    print(f'\nAttempting to solve..\nThe solution attempt is as expected: {solution_attempt == the_trials[x].grid}')
    #print(f'\n Solution attempt: \n{solution_attempt[0]}\n{solution_attempt[1]}\n{solution_attempt[2]}\n{solution_attempt[3]}\n{solution_attempt[4]}\n{solution_attempt[5]}\n{solution_attempt[6]}\n{solution_attempt[7]}\n{solution_attempt[8]}\n')
    if the_trials[x].grid != solution_attempt:
        dif_sol_count += 1

print(f'---------------------There were {dif_sol_count} unexpected solutions out of {amount}.')