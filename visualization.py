import sys
import pygame
import numpy as np

from maze_generation import init_grid, generate_maze_recursive

# Consider decreasing the maze size if memory may be an 
# issue rather than increasing the recursion limit.
import sys
sys.setrecursionlimit(10000)

# Constants
n, m = 25, 25
num_cells = n * m
size = width, height = 800, 800
cell_width, cell_height = width // n, height // m
line_width = 4
# Colors
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
light_blue = 100, 100, 255
grey = 200, 200, 200


def display(screen, grid, color_squares=False):
    # Set the background to white
    screen.fill(grey)
    # Draw the top and the right walls of each cell
    for row in grid:
        for cell in row:
            if cell.top:
                # Draw a line along the top of the cell
                # start_pos = cell.x * cell_width, cell.y * cell_height
                # end_pos = (cell.x + 1) * cell_width, cell.y * cell_height
                # pygame.draw.line(screen, black, start_pos, end_pos, line_width)

                start_pos = cell.x * cell_width, cell.y * cell_height - line_width
                dimensions = cell_width, line_width * 2
                end_pos = (cell.x + 1) * cell_width, cell.y * cell_height + line_width
                pygame.draw.rect(screen, black, (start_pos, dimensions))
            if cell.right:
                # Draw a line along the right side of the cell
                # start_pos = (cell.x + 1) * cell_width, cell.y * cell_height
                # end_pos = (cell.x + 1) * cell_width, (cell.y + 1) * cell_height
                # pygame.draw.line(screen, black, start_pos, end_pos, line_width)

                start_pos = (cell.x + 1) * cell_width - line_width, cell.y * cell_height
                dimensions = line_width * 2, cell_height
                pygame.draw.rect(screen, black, (start_pos, dimensions))

            # Color the squares depending on their visited state
            if color_squares:
                # Set the fill color of the square if it has been visited
                if cell.visited or cell.start or cell.end:
                    fill_color = light_blue
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

    # Draw the left and bottom of the entire grid
    pygame.draw.line(screen, black, (0, 0), (0, m * cell_height), line_width)
    pygame.draw.line(
        screen,
        black,
        (0, m * cell_height),
        (n * cell_width, m * cell_height),
        line_width,
    )


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

    
def solve_maze(screen, grid, cell):
    """
    Takes a grid object containing Cell objects in a 2d list,
    recursively solves the maze with backtracking starting from 
    the initially passed cell argument. Displays the progress 
    on a pygame screen object.
    Args:
    screen -> pygame.Screen
    grid -> List[List[Cell]]
    cell -> Cell
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

            # Update the display
            display(screen, grid, True)
            pygame.display.update()

            # Save the current cell and recursively call the 
            # function with the chosen random neighbor as the new cell
            original_cell = cell
            cell = rand_neighbor

            # If the path works given the random neighor cell as an argument
            # we return True, otherwise we reset the cell to the original 
            if solve_maze(screen, grid, cell):
                return True
            else:
                cell = original_cell
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



    # Game loop
    end_program = False
    while not end_program:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_program = True
                pygame.quit()
                sys.exit(0)

        solve_maze(screen, grid, start_cell)


if __name__ == "__main__":
    pygame.init()
    main()
