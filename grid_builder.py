import random
from config import Config
from grid import Grid

class GridBuilder:
    """
    A class used to build and initialize a grid with a specified number of cells.
    Methods
    -------
    build(num_cells: int) -> Grid
        Static method that constructs a grid with the specified number of cells.
    """
    """
        Constructs a grid with the specified number of cells.
        Parameters
        ----------
        num_cells : int
            The number of cells to be set in the grid.
        Returns
        -------
        Grid
            A grid object with the specified number of cells set.
    """
    @staticmethod
    def build(num_cells: int) -> Grid:
        grid = Grid()
        
        radius = 5
        while grid.count_set() < num_cells:
            random_x, random_y = random.randint(Config.MAX_GRID_SIZE // 2 - radius, Config.MAX_GRID_SIZE // 2 + radius), random.randint(Config.MAX_GRID_SIZE // 2 - radius, Config.MAX_GRID_SIZE // 2 + radius)
            grid.set_cell(random_x, random_y)
        
        return grid