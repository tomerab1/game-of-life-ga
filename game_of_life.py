from grid import Grid

class GameOfLife:
    """
    A class to represent the Game of Life.
    Attributes
    ----------
    grid : Grid
        The current state of the game grid.
    Methods
    -------
    run():
        Executes one iteration of the Game of Life and returns the new grid state.
    """
    """
        Constructs all the necessary attributes for the GameOfLife object.
        Parameters
        ----------
        grid : Grid
            The initial state of the game grid.
    """
    """
        Executes one iteration of the Game of Life.
        Returns
        -------
        Grid
            The new state of the game grid after one iteration.
    """
    def __init__(self, grid: Grid):
        self.grid = grid

    def run(self):
        new_grid = Grid()
        
        for cell in self.grid.grid:
            x, y = cell
            if self.grid.count_neighbors(x, y) in [2, 3]:
                new_grid.set_cell(x, y)
            
            for dx, dy in self.grid.ALLOWED_DIRS:
                new_x = x + dx
                new_y = y + dy
                if not self.grid.is_alive(new_x, new_y) and self.grid.count_neighbors(new_x, new_y) == 3:
                    new_grid.set_cell(new_x, new_y)
                        
        return new_grid