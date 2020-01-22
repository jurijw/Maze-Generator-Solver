import numpy as np

class Cell:

    def __init__(self, x, y):
        # Set the position of the cell
        self.x = x
        self.y = y
        # Set the right and top cell walls to be True
        self.right = True
        self.top = True

        # Attributes for maze generation
        self.visited = False
        self.neighbors = [] # list of neighboring cells

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"

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


def generate_maze(grid, start_pos):
    x, y = start_pos

    cell = grid[y][x]
    # Pick a random unvisited neighbor
    unvisited_neighbors = [neighbor for neighbor in cell.neighbors if not neighbor.visited]
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
        cell.top = False
    else:
        # Otherwise the neighbor must lie below the original cell
        # In this case we break its top wall
        rand_neighbor.top = False

    # Set the neighbors visited attribute to True 
    rand_neighbor.visited = True

    # Recurse with the neighbor as the new starting cell

