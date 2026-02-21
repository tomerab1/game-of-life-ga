from config import Config
import random
import ast
import copy

class Grid:
    """
    A class to represent a sparse 2D grid
    """
    ALLOWED_DIRS = [
            (0, 1), (1, 0), (0, -1), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

    def __init__(self):
        self.gird = dict()

    def __len__(self):
        return len(self.gird)

    def __hash__(self):
        return hash(frozenset(self.gird.items()))

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

    def clear(self):
        """Remove all cells from the grid."""
        self.gird.clear()

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

    def get_bounding_box(self):
        """Return (min_x, min_y, max_x, max_y) of all alive cells."""
        if not self.gird:
            return (0, 0, 0, 0)
        alive = [k for k, v in self.gird.items() if v]
        if not alive:
            return (0, 0, 0, 0)
        xs = [c[0] for c in alive]
        ys = [c[1] for c in alive]
        return (min(xs), min(ys), max(xs), max(ys))

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
