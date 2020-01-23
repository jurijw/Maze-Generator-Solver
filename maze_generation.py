import numpy as np
from copy import deepcopy

# DEBUG
np.random.seed(0)


class Cell:
    # Number of visited cells
    visited_cells = 0

    def __init__(self, x, y):
        # Set the position of the cell
        self.x = x
        self.y = y
        # Set the right and top cell walls to be True
        self.right = True
        self.top = True

        # Attributes for maze generation
        self.visited = False
        self.neighbors = []  # list of neighboring cells

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"

    def visit(self):
        """
        Set the visited state of the cell to True
        and increase the count of visited cells by 1.
        """
        self.visited = True
        Cell.visited_cells += 1


def init_grid(n, m):
    """
    Generate a grid of Cell objects with their right and top
    properties set to True (default) 
    """
    # Placeholder array
    grid = [[None for _ in range(n)] for _ in range(m)]
    # Populate the n * m grid with completely filled walls
    for i in range(n):
        for j in range(m):
            grid[j][i] = Cell(i, j)
    # Loop through the grid once more and add each cells neighbors
    # to their neighbors attribute
    for j, row in enumerate(grid):
        for i, cell in enumerate(row):
            vectors_to_neighbors = ([1, 0], [0, 1], [-1, 0], [0, -1])
            for vector in vectors_to_neighbors:
                dx, dy = vector
                new_x, new_y = i + dx, j + dy
                # If new x and new y are not off the grid add the
                # according cell to neighbors
                if new_x >= 0 and new_x < n and new_y >= 0 and new_y < m:
                    cell.neighbors.append(grid[new_y][new_x])
    return grid

def print_grid(grid):
    """
    Takes a grid object and prints the given maze 
    configuration in the commandline.
    Args:
    grid -> List[List[Cell]]
    Returns:
    None
    """
    print(" ", end="")
    for i in range(len(grid)):
        print(str(i), end=" ")
    print()
    for j, row in enumerate(grid):
        print(str(j), end="")
        for cell in row:
            if cell.top and cell.right:
                print("\u203e|", end="")
            elif cell.top:
                print("\u203e ", end="")
            elif cell.right:
                print(" |", end="")
            else:
                print("  ")
        print()
    

def generate_maze_recursive(grid, cell, num_cells, list_of_grids=None):

    # Base case - No unvisited cells are left
    # (i.e number of visited cells equals number of cells in the grid)
    if Cell.visited_cells == num_cells:
        return True

    # Recursive case - there are unvisited cells
    unvisited_neighbors = [
        neighbor for neighbor in cell.neighbors if not neighbor.visited
    ]

    # If there are unvisited neighbors
    if len(unvisited_neighbors) > 0:
        # Pick a random unvisited neighbor
        rand_neighbor = np.random.choice(unvisited_neighbors)

        # Break the wall between the two chosen cells
        if rand_neighbor.x > cell.x:
            # If the randomly chosen cell is to the right then break the
            # right wall of the original cell
            cell.right = False
        elif rand_neighbor.x < cell.x:
            # If the randomly chosen cell is to the left then break its right wall
            rand_neighbor.right = False
        elif rand_neighbor.y > cell.y:
            # If the randomly chosen neighbor is above break the
            # original cell's top wall
            rand_neighbor.top = False
        else:
            # Otherwise the neighbor must lie below the original cell
            # In this case we break its top wall
            cell.top = False

        # Set the neighbors visited attribute to True
        rand_neighbor.visit()

        # DEBUG: print the board
        print_grid(grid)
        # print()
        # pause = input("press any key to continue")

        # If list_of_grids is of type list append a copy of the grid to it 
        if type(list_of_grids) == list:
            list_of_grids.append(deepcopy(grid))

        # Recurse with the neighbor as the new starting cell
        # and return True
        if generate_maze_recursive(grid, rand_neighbor, num_cells):
            return True

    # In the case that no more unvisited neighbors exist we return False and must
    # backtrack to the last possible cell containing unvisited neighbors
    else:
        return False

def main():
    grid = init_grid(10, 10)
    print_grid(grid)
    cell = grid[5][5]
    cell.visit()
    generate_maze_recursive(grid, cell, 100)

if __name__ == "__main__":
    main()
