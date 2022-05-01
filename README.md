# Sudoku app  ** *Work in Progress* **
This project consist in developing an app where one can play sudoku puzzles at different difficulties, time the games, have a record of the best times and personalize the GUI color scheme.


## Program's logic
Before meddling with the GUI, I had to develop the logic behind the app: a python program that can quickly generate a sudoku puzzle at a given difficulty (easy, medium or hard) with a guaranteed unique solution. My approach to attain this is by using Object Oriented Programming (OOP), defining two type of objects: a 'Puzzle_Generator' and a 'Cell_ Solver', being the first one the one in charge of returning the solvable puzzle and the second one a secondary object that aids the first one to achieve it's purpose with the help of a backtracking algorithm.


### Puzzle_Generator
Each Puzzle_Generator object has 4 properties: '.difficulty', '.id', '.grid' and '.puzzle'. 
They also have 4 methods: 'generate_solvers()', '.solve_grid()', '.get_puzzle_ready()' and '.look_for_more_solutions()'.

The first step for a Puzzle_Generator in order to obtain a solvable puzzle is to create a completely filled valid sudoku grid (i.e. a 9x9 grid filled with numbers 1 to 9 without repeating a number in a row, column or it's corresponding 3x3 box). 

When initialized, a Puzzle_Generator receives as an argument the difficulty desired for the puzzle, which is stored in the '.difficulty' property. It can also receive optional 'id' and 'verbose' arguments for testing and debugging purposes (the ID and verbose are '0' by default). Then, it creates an empty 9x9 grid (filled with 0's: **whenever a cell is filled with a '0' in this program, it means the cell is empty**), which is stored as the property '.grid' and then passed to the 'solve_grid()' method of the object, that returns a completely filled valid sudoku grid. 

After obtaining the completely filled valid sudoku grid (the solution to the puzzle), each row of it is copied into a new grid that is stored in the object property '.puzzle'. Then, the method '.get puzzle_ready()' is called, which turns the '.puzzle' grid into the actual puzzle by removing cellls from it (one or two at a time, depending on the difficulty of the puzzle) and making sure after each removal that the puzzle still has a unique solution, for which it uses the '.look_for_more_solutions()' method each time a number is removed from the grid.

#### .generate_solvers()
The generate_solvers() method recieves a grid (be it an empty one or a puzzle), which then it reads and, for every position where it encounters a '0', it generates a Cell_Solver object with that position and appends it to a list that is later returned when the whole grid has been read.

#### .solve_grid()
The .solve_grid() method implements a backtracking algorithm that recieves a grid (be it an empty one or a puzzle) and makes a copy of it which is later returned as the solved grid. It can also recieve an 'ignore' argument that is supposed to be a Cell_Solver object, and, if passed, the method ignores the current attempt from the ignored solver when trying to solve the grid, this is used when trying to find a second solution for a puzzle. If this method can not find a solution for the grid passed it returns the flag 'no_solution_found'.

This method starts by creating a list of solvers for the grid to solve with the help of the .generate_solvers() method. After getting the solvers ready, the solvers list is sorted by the number of options available for each solver, being the ones with the least options available at the beginning of the list. 

Then, a loop is started taking each solver from the sorted list and running its '.select_attempt()' method. For each loop:
	- If .select_attempt() returns a number, the loop procceeds with the next solver. When the grid is filled, the method returns a tuple with two elements: the solved grid and the list of solvers (each with their remaining options in case there were options left).
	- If .select_attempt() returns 'no_suitable_number', the loop rolls back to the previous solver and runs it's 'select_attempt()' method again in order to try with one of it's remaining options.
	- When rolling back leads to a solver with no options left, the loop keeps rolling back until it finds a solver with more options available and tries with one of those.
	- If the loop is rolling back and founds that there are no options left in any of the solvers, the solve_grid() method returns the flag 'no_solution_found'.

#### .get_puzzle_ready()
The .get_puzzle_ready() is a method that takes no arguments and works with the properties of the Puzzle_Generator object. 
It starts by defining the amount of hints to be given in the finished puzzle (the fixed numbers in the grid presented to the user) according to the .difficulty property and the following dictionary:

	- Easy: from 40 to 45 hints
	- Medium: from 35 to 39 hints
	- Hard: from 30 to 34 hints

After this, the method creates a list of pairs of symmetric cells to be removed from the puzzle in order to reach the desired number of hints. If the number of solvable cells to be created is odd, the center cell of the grid is the first one to be removed. Then, a loop is started in which a random pair of symmetric cells is selected from the list and removed from the grid, turning their locations into solvable cells. After each removal, the '.look_for_more_solutions()' method is called to make sure that, after removing those cells, the puzzle still has a unique solution:
	- If a second solution is found, the pair of cells removed from the puzzle is restored (using the model of the original grid), the rejected cells are stored in a list called 'rejected_pairs' and the loop continues, trying to remove another pair of symmetrical cells.
	- If the solution found is the expected one (the original filled grid) and the solvers that helped to find it had no options left, the loop continues trying to remove another pair of cells.
	- If the solution found is the expected one (the original filled grid) and the solvers that helped to find it had more options left, then a second loop is initiated trying to find yet another solution until the options left are exhausted (this last loop is contained in the function 'exhaust_options()').

This loops continues until the desired number of solvable cells is achieved or the list of symmetric pairs of cells is exhausted, in which case the algorithm will begin to try and remove individual cells from the 'rejected_pairs' list in order to complete the desired number of solvable cells. 

In the unlikely case that the algorithm can not remove any more individual cells, it will return the puzzle as it is, still with a unique solution and with the maximum amount of cells removed without causing a second possible solution to appear.

#### .look_for_more_solutions()
The look_for_more_solutions() method recieves a puzzle and an expected solution for that. This method runs the passed puzzle through the .solve_grid() method and determines whether the solution generated is equal to the expected solution or if a new solution was found.

If no solution was found by the .solve_grid() method, .look_for_more_solutions() returns a flag: the string 'no_solution_found'.

In case a solution was found, this method returns a list with 3 items. The first item is a code for the result of the function:
	- If the solution obtained is as expected we can get: 'no_options_left' or 'options_remaining', depending on whether there are or there are not options left on the solvers returned by the solve_grid() function.
	- If the solution obtained is not the expected one, the code is 'another_solution_found', in this case the attempted pair removal must be reverted.

The second item on the list would be a list of the completed solvers from the returned solution, i.e. those that had only one option and is the one they attempted. If there were no options left in any solver, the length of this list should be the same as the number of solvable cells in the puzzle.

The third item on the list would be a list of the unsolved or remaining solvers for the returned solution, those that had options left or whose only option was deduced after another solver made an attempt with more options still available. If there were no options left in any solver, the length of this list should be 0.


### Cell_Solver
A Cell_Solver instance is created for every empty cell of a puzzle when the program tries to solve it.

Each Cell_Solver object has 8 properties: '.row', '.col', '.grid', '.rows', '.cols', '.box', '.attempt' and '.options'.

These properties contain information about the location in the grid from the cell that the solver is trying to solve (.row & .col). The whole grid organized by rows (.grid) and by columns (.cols) and the 3x3 box of the cell to solve (.box). The '.options' property contains a list of the numbers that are not already present in the cell's row, column or box. Finally, the '.attempt' property contains a random number from the available options that is proposed by the solver as an attempt to solve the cell (this property is 0 by default).

Also, the Cell_Solver has 3 methods: '.reset_solver()', '.filter_options()' and '.select_attempt()'.

#### .reset_solver()
This method recieves a grid as an argument and restores the solver's grid as well as it's options available according to the passed grid. It also turns it's current attempt to 0. This method is used when the backtracing algorithm needs to revert a path taken when attempting to solve a puzzle.

#### .filter_options()
These methods receives a grid as an argument and checks the cell's row, column and box in the passed grid looking for numbers already present in any of those in order to remove them from the cell's options.

#### .select_attempt()
This method receives a grid and starts by calling the filter_options() method with the passed grid as the argument, this with the purpose of taking into account recent changes to the puzzle (present in the passed grid). Then, it randomly chooses a number from the cell's available options and returns it. If the list of options is empty, the method returns the flag string 'no_suitable_num'.


### Notes
In the current version of the logic, I tried to make it so that, besides having a unique solution, the hints in the puzzle are scattered symmetrically throughout the grid. This approach worked fine with puzzles with a lot of hints and little solvable cells (beginner, easy and medium difficulty puzzles). But, as the number of solvable cells incremented, the algorithm struggled to find symmetric pairs of cells.

The .solve_grid() method can be greatly improved by implementing more discarding criteria to be applied right after selecting the attempts for the solvers with only one option and before starting the loop that brute forces the solution. Said loop must be left as a last resort as it significantly increases the running time of the function.

Once the .solve_grid() method is improved, I am planning on incorporating two more difficulties with even harder puzzles, as those available right now can be too easy for experienced players. This needs to be implemented later because currently it an unacceptable amount of time for the backtracking algorithm to solve puzzles with more empty cells.



# Program's GUI
Until now I've only sketched what will be the program's graphic user interface using python's library Tkinter.