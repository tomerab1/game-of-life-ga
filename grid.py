from config import Config
import random
import ast
import copy

class Grid:
    """
    A class to represent a sparse 2D grid
    Attributes
    ----------
    ALLOWED_DIRS : list of tuple
        List of tuples representing the allowed directions for neighbor cells.
    Methods
    -------
    __init__():
        Initializes the grid as an empty dictionary.
    __len__():
        Returns the number of cells in the grid.
    grid:
        Property to get the keys of the grid dictionary.
    grid(value):
        Setter to set the grid dictionary.
    _is_in_bounds(x, y):
        Checks if the given coordinates (x, y) are within the bounds defined by Config.MAX_GRID_SIZE.
    set_cell(x, y, val=True):
        Sets the value of the cell at coordinates (x, y) to the specified value if within bounds.
    is_alive(x, y):
        Checks if the cell at coordinates (x, y) is alive (True) or dead (False).
    get_cell(x, y):
        Returns the value of the cell at coordinates (x, y) if within bounds, otherwise None.
    count_set():
        Returns the number of cells that are set in the grid.
    count_neighbors(x, y):
        Counts the number of alive neighbors for the cell at coordinates (x, y).
    __str__():
        Returns a string representation of the grid.
    """
    ALLOWED_DIRS = [
            (0, 1), (1, 0), (0, -1), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
    
    def __init__(self):
        self.gird = dict()
        
    def __len__(self):
        return len(self.gird)
    
    def copy(self):
        new_grid = Grid()
        new_grid.grid = copy.deepcopy(self.grid)
        return new_grid
        
    def get_random(self):
        return random.choice(list(self.grid.keys()))
    
    def remove_dead(self):
        self.grid = {k: v for k, v in self.grid.items() if v}
        
    @property
    def grid(self):
        return self.gird
    
    @grid.setter
    def grid(self, value):
        self.gird = value
        
    def _is_in_bounds(self, x, y):
        return 0 <= x < Config.MAX_GRID_SIZE and 0 <= y < Config.MAX_GRID_SIZE
    
    def set_cell(self, x, y, val = True):
        if not self._is_in_bounds(x, y):
            return
        self.gird[(x, y)] = val
        
    def is_alive(self, x, y):
        if not self._is_in_bounds(x, y):
            return False
        return self.gird.get((x, y), False)
    
    def get_cell(self, x, y):
        if not self._is_in_bounds(x, y):
            return None
        return self.gird.get((x, y), None)
    
    def count_set(self):
        return len(self.gird)
    
    def count_neighbors(self, x, y):
        return sum([1 for dx, dy in Grid.ALLOWED_DIRS if self.get_cell(x + dx, y + dy)])
    
    @staticmethod
    def from_string(grid_str):
        grid = Grid()
        grid.gird = ast.literal_eval(grid_str)
        return grid
    
    def __eq__(self, value):
        return self.gird == value.gird
    
    def __str__(self):
        return str(self.gird)