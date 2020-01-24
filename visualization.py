import os
import sys
import pygame
import numpy as np
# DEBUG - uncomment for consistent results
# np.random.seed(0)

from maze_generation import init_grid, generate_maze_recursive

# Consider decreasing the maze size if memory may be an 
# issue rather than increasing the recursion limit.
sys.setrecursionlimit(5000)
# Change window start position
os.environ['SDL_VIDEO_WINDOW_POS'] = '20, 50'

# Constants
n, m = 50, 50
num_cells = n * m
size = width, height = 800, 800
cell_width, cell_height = width // n, height // m
line_width = 1
delay = 0 # delay in miliseconds

# Colors
black = 0, 0, 0
white = 255, 255, 255
red = 100, 0, 0
green = 0, 100, 40
blue = 100, 100, 255
light_green = 0, 255, 100


def display(screen, grid, color_squares=False):
    """
    Displays the current grid on a pygame screen object by drawing
    each cell's walls. If color_squares is set to True, each square
    in the grid will be colored according to whether it is the start,
    the, finish, or whether or not it has been visited.
    Args:
    screen -> pygame.Screen
    grid -> List[List[Cell]]
    color_squares -> Bool
    """
    # Set the background to white
    screen.fill(white)
    # Draw the top and the right walls of each cell
    for row in grid:
        for cell in row:
            if cell.top:
                # Draw a line along the top of the cell
                start_pos = cell.x * cell_width, cell.y * cell_height - line_width
                dimensions = cell_width, line_width * 2
                pygame.draw.rect(screen, black, (start_pos, dimensions))

            if cell.right:
                # Draw a line along the right side of the cell
                start_pos = (cell.x + 1) * cell_width - line_width, cell.y * cell_height
                dimensions = line_width * 2, cell_height
                pygame.draw.rect(screen, black, (start_pos, dimensions))

            # Color the squares depending on their visited state
            if color_squares:
                # Set the fill color of the square if it has been visited
                if cell.visited or cell.start or cell.end:
                    fill_color = blue
                    if cell.solution:
                        fill_color = light_green
                    # If it is the start or stop override the color
                    if cell.start:
                        fill_color = green
                    elif cell.end:
                        fill_color = red
                    # Calculate the position of the top left corner of the square
                    top_left = cell.x * cell_width + line_width, cell.y * cell_height + line_width
                    # Calculate the width and height
                    dimensions = cell_width - line_width * 2, cell_height - line_width * 2
                    # Fill the square
                    pygame.draw.rect(screen, fill_color, (top_left, dimensions))

    # Draw the grid outline
    pygame.draw.rect(screen, black, (0, 0, width, height), line_width * 2)
   

def reset_visited_attributes(grid):
    """
    Resets the visited attributes of every cell
    in a 2d grid list.
    Args:
    grid -> List[List[Cell]]
    Returns:
    None
    """
    # Reset all cell's visited attributes
    for row in grid:
        for cell in row:
            cell.visited = False


def init_solve(grid):
    """
    Function to be run after maze is generated. Resets all 
    the visited attributes and then checks for the open
    neighbors of each cell 
    Args:
    grid -> List[List[Cell]]
    Returns:
    None
    """
    vectors_to_neighbors = ([1, 0], [0, 1], [-1, 0], [0, -1])
    # Loop through all cells in the grid
    for row in grid:
        for cell in row:
            # Reset the visited attribute of each cell
            cell.visited = False 

            for vector in vectors_to_neighbors:
                dx, dy = vector
                new_x, new_y = cell.x + dx, cell.y + dy
                # If the new x and new y are still on the grid
                if new_x >= 0 and new_x < n and new_y >= 0 and new_y < m:
                    # Get the potential neighbor and check if it is accessible
                    potential_neighbor = grid[new_y][new_x]
                    # If the neighboring cell is to the right and the dividing wall 
                    # is not in place add the neighbor to the open_neighbors list
                    if new_x > cell.x and not cell.right:
                        cell.open_neighbors.append(potential_neighbor)
                    # If the neighboring cell is to the left ""
                    elif new_x < cell.x and not potential_neighbor.right:
                        cell.open_neighbors.append(potential_neighbor)
                    # If the neighboring cell is below ""
                    elif new_y > cell.y and not potential_neighbor.top:
                        cell.open_neighbors.append(potential_neighbor)
                    # If the neighboring cell is above ""
                    elif new_y < cell.y and not cell.top:
                        cell.open_neighbors.append(potential_neighbor)

    
def solve_maze(screen, grid, cell, solution_order=None):
    """
    Takes a grid object containing Cell objects in a 2d list,
    recursively solves the maze with backtracking starting from 
    the initially passed cell argument. Displays the progress 
    on a pygame screen object. solution_order is used to track 
    the correct order of the algorithm. If no argument is passed
    only the order of visited cells will be visualized.
    Args:
    screen -> pygame.Screen
    grid -> List[List[Cell]]
    cell -> Cell
    solution_order -> List[] / (None)
    Returns:
    True if maze has been solved
    else False
    """

    # Base case - end is found
    if cell.end:
        return True


    # Recursive case - end has not been found

    # Pick a random unvisited neighboring cell which is accessible from the original cell 
    unvisited_neighbors = [neighbor for neighbor in cell.open_neighbors if not neighbor.visited]

    # If there are unvisited accesible neighbors, pick a random one
    if unvisited_neighbors != []:
        # Loop through the unvisited_neighbors
        for _ in range(len(unvisited_neighbors)):
            # Double check that all neighbors have not been visited already
            unvisited_neighbors = [neighbor for neighbor in cell.open_neighbors if not neighbor.visited]
            if unvisited_neighbors == []:
                return False

            # Pick a random neighbor
            rand_neighbor = np.random.choice(unvisited_neighbors)
            # Mark the cell as visited
            rand_neighbor.visited = True
            
            if type(solution_order) == list:
                # Assume it to be part of the solution
                rand_neighbor.solution = True
                # Add it to the solution order list
                solution_order.append(rand_neighbor)

            # Update the display
            display(screen, grid, True)
            pygame.display.update()
            # Add a delay
            pygame.time.delay(delay)

            # Save the current cell and recursively call the 
            # function with the chosen random neighbor as the new cell
            original_cell = cell
            cell = rand_neighbor
            
            # If the path works given the random neighor cell as an argument
            # we return True, otherwise we reset the cell to the original 
            if solve_maze(screen, grid, cell, solution_order):
                return True
            else:
                # Otherwise reset the cell and remove it from the solution order
                cell = original_cell

                if type(solution_order) == list:
                    solution_order[-1].solution = False
                    solution_order.pop()
                    
    # If there are no more unvisited accessible neighbors available then all paths 
    # down this tree have been exhausted. In this case we return False.
    else: 
        return False
            

def main():
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Maze generation")

    # Initialize the grid
    grid = init_grid(n, m)
    # Display the maze grid
    display(screen, grid)
    pygame.display.update()

    # Choose a random starting cell
    start_x, start_y = np.random.randint(n), np.random.randint(m)
    start_cell = grid[start_y][start_x]
    start_cell.start = True
    start_cell.visit()

    # Run the maze generating algorithm
    generate_maze_recursive(grid, start_cell, num_cells)

    # Pick a random end cell
    end_x, end_y = np.random.randint(n), np.random.randint(m)
    end_cell = grid[end_y][end_x]
    end_cell.end = True

    # Display the maze
    display(screen, grid, True)
    pygame.display.update()

    # Reset the visited status of the cells as well as load all of their accessible neighbors
    init_solve(grid)
    start_cell.visited = True
    solution_order = [start_cell]

    # Game loop
    end_program = False
    while not end_program:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_program = True
                pygame.quit()
                sys.exit(0)

        solve_maze(screen, grid, start_cell, solution_order)

if __name__ == "__main__":
    pygame.init()
    main()
