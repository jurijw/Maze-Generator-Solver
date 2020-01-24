# Maze-Generator-Solver
Python program to generate mazes and solve them using backtracking. Uses pygame to visualize backtracking algorithm in progress.

Inspired by [u/Enguzelharf](https://www.reddit.com/user/Enguzelharf/)'s [reddit post](https://www.reddit.com/r/Python/comments/empp5x/oc_updated_version_of_my_recent_maze_finding/)

Two seperate python files are contained. 

maze_generation.py will generate a random n * m maze.
It also contains a `print_board(grid)` function, which displays the maze in the commandline, which can be useful for debugging.

The main file, visualization.py contains several functions to display the maze, solve the maze, and display the algorithm's solving process in real-time.
It will not run without maze_generation.py!

During the visualization, cells are marked depending on their state.
* White if unvisited
* Blue if visited
* Light green if part of current path
* Dark green if start
* Red if Finish

`n` and `m` - the number of cells in a row and column, respectively, are set to a default of 50 each. In order to allow for this, as well as even bigger mazes,
python's maximum recursion limit has been exceeded using `sys.setrecursionlimit()`. 

A delay between each step can be introduced by setting `delay` to the desired amount of delay in miliseconds.

Lastly, pygame may crash if you do not let the algorithm find its way to the end. Just force quit it in this case.
