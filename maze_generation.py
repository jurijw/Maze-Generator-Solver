import numpy as np
from copy import deepcopy

# DEBUG: uncomment to get consistent results when debugging
# np.random.seed(0)

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
        and increase the count of total visited cells by 1.
        Returns:
        None
        """
        self.visited = True
        Cell.visited_cells += 1


def init_grid(n, m):
    """
    Generate a grid of Cell objects with their right and top
    (wall) properties set to True (default) 
    Args:
    n, m -> Int
    Returns:
    List[List[Cell]]
    """
    # 2D placeholder array for Cell objects
    grid = [[None for _ in range(n)] for _ in range(m)]

    # Populate the n * m grid with completely filled walls
    for i in range(n):
        for j in range(m):
            grid[j][i] = Cell(i, j)

    # Loop through the grid once more and add each cell's neighbors
    # to their neighbors attribute - This will come in handy
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
    
    # Return the grid filled with Cell objects
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
                print("  ", end="")
        print()
    

def generate_maze_recursive(grid, cell, num_cells, list_of_grids=None):
    """
    Takes a 2d grid list populated with Cell objects and recursively 
    generates a maze starting from the position of the cell object passed
    to the function as an argument. The num_cells argument is passed in 
    order to easily check if all cells have been visited meaning the maze
    is completely generated. Optionally a list_of_grids list may be passed
    in order to record the progress of the algorithm.
    Args:
    grid -> List[List[Cell]]
    cell -> Cell 
    num_cells -> Int
    (list_of_grids -> List[])
    """
    # Base case - No unvisited cells are left / the maze has been fully generated

    # Check if all cells have been visited, if so the maze is complete
    if Cell.visited_cells == num_cells:
        return True

    # Recursive case - there are unvisited cells
    
    # A list containing the unvisited neighbors of the current cell
    unvisited_neighbors = [
        neighbor for neighbor in cell.neighbors if not neighbor.visited
    ]

    # If there are unvisited neighbors
    if len(unvisited_neighbors) > 0:
        for _ in range(len(unvisited_neighbors)):

            # Double check that all unvisited neighbors are actually unvisited.
            # It could be that in a recursive call they were visited but the list
            # in this scope wasn't updated 
            unvisited_neighbors = [
                neighbor for neighbor in cell.neighbors if not neighbor.visited
            ]
            # If no neighbors are unvisited return False
            if len(unvisited_neighbors) == 0:
                return False

            # Otherwise pick a random unvisited neighbor/cell
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
            # remove the neighbor from the list of unvisited neighbors
            unvisited_neighbors.remove(rand_neighbor)

            # DEBUG: uncomment to print the board every time a cell is updated
            #        (must be run from the maze_generation.py file)
            # if __name__ == "__main__":
            #     print_grid(grid)

            # If list_of_grids is of type list append a copy of the grid to it 
            # This may be used to track the progress of the algorithm
            if type(list_of_grids) == list:
                list_of_grids.append(deepcopy(grid))

            # Save the current cell as the original and set the randomly chosen 
            # neighboring cell as the new cell to be used.
            original_cell = cell
            cell = rand_neighbor

            # Recurse with the neighbor as the new starting cell and return
            # True if another unvisited neighboring cell can be found
            if generate_maze_recursive(grid, cell, num_cells):
                return True
            else:
                # Otherwise reset the cell to the original cell and loop 
                # through the other unvisited neighbors for the cell 
                cell = original_cell

    # In the case that no more unvisited neighbors exist we return False and
    # backtrack to the last possible cell with unvisited neighbors
    else:
        return False