import sys
import pygame

from maze_generation import init_grid, generate_maze_recursive

# Constants
n, m = 10, 10
num_cells = n * m
size = width, height = 800, 800
cell_width, cell_height = width // n, height // m
line_width = 2
# Colors
black = 0, 0, 0
white = 255, 255, 255


def display(screen, grid):
    # Set the background to white
    screen.fill(white)
    # Draw the top and the right walls of each cell
    for row in grid:
        for cell in row:
            if cell.top:
                # Draw a line along the top of the cell
                start_pos = cell.x * cell_width, cell.y * cell_height
                end_pos = (cell.x + 1) * cell_width, cell.y * cell_height
                pygame.draw.line(screen, black, start_pos, end_pos, line_width)
            if cell.right:
                # Draw a line along the right side of the cell
                start_pos = (cell.x + 1) * cell_width, cell.y * cell_height
                end_pos = (cell.x + 1) * cell_width, (cell.y + 1) * cell_height
                pygame.draw.line(screen, black, start_pos, end_pos, line_width)
    # Draw the left and bottom of the entire grid
    pygame.draw.line(screen, black, (0, 0), (0, m * cell_height), line_width)
    pygame.draw.line(
        screen,
        black,
        (0, m * cell_height),
        (n * cell_width, m * cell_height),
        line_width,
    )


def main():
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Maze generation")

    # Initialize the maze grid
    grid = init_grid(n, m)
    # Display the maze grid
    display(screen, grid)
    pygame.display.update()

    # Choose a random starting cell
    cell = grid[5][5]
    cell.visit()
    list_of_grids = []
    # Run the maze generating algorithm
    generate_maze_recursive(grid, cell, num_cells, list_of_grids)
    print(len(list_of_grids))

    # Game loop
    end_program = False
    while not end_program:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_program = True
                pygame.quit()
                sys.exit(0)

        # Display the grid again
        display(screen, grid)
        pygame.display.update()

        # for grid in list_of_grids:
        #     display(screen, grid)
        #     pygame.time.sleep(50)


if __name__ == "__main__":
    pygame.init()
    main()
