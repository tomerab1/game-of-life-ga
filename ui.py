import tkinter as tk
from grid import Grid
from game_of_life import GameOfLife
from config import Config


class UI:
    """
    A class to represent the User Interface for the Game of Life.
    Attributes:
    -----------
    master : tk.Tk
        The main window of the application.
    grid : Grid
        The initial grid state for the Game of Life.
    configs : list, optional
        A list of configurations for different grid states (default is None).
    cell_size : int
        The size of each cell in the grid (default is 10).
    current_config_index : int
        The index of the current configuration being displayed (default is 0).
    canvas : tk.Canvas
        The canvas widget to draw the grid.
    start_stop_button : tk.Button
        The button to start or stop the simulation.
    rewind_button : tk.Button
        The button to rewind the simulation to the initial state.
    prev_button : tk.Button
        The button to show the previous configuration (if configs are provided).
    next_button : tk.Button
        The button to show the next configuration (if configs are provided).
    info_label : tk.Label
        The label to display additional information about the current configuration.
    simulation_running : bool
        A flag to indicate whether the simulation is running (default is False).
    iteration : int
        The current iteration of the simulation (default is 0).
    Methods:
    --------
    update_canvas():
        Clears and redraws the grid on the canvas.
    update_grid(new_grid: Grid):
        Updates the grid with a new state and redraws the canvas.
    update_info():
        Updates the information label with details about the current configuration.
    toggle_simulation():
        Starts or stops the simulation.
    rewind_simulation():
        Rewinds the simulation to the initial grid state.
    run_game_of_life():
        Runs the Game of Life simulation, updating the grid state iteratively.
    show_previous_config():
        Displays the previous configuration from the configs list.
    show_next_config():
        Displays the next configuration from the configs list.
    load_current_config():
        Loads the current configuration and resets the grid and simulation state.
    """
    def __init__(self, master, grid: Grid, configs=None):
        self.master = master
        self.master.title("Game of Life")
        self.initial_grid = grid
        self.grid = grid
        self.cell_size = 10
        self.configs = configs or []
        self.current_config_index = 0

        # Create canvas with background color
        self.canvas = tk.Canvas(
            self.master,
            width=Config.MAX_GRID_SIZE * self.cell_size,
            height=Config.MAX_GRID_SIZE * self.cell_size,
            bg="#171717"
        )
        self.canvas.pack()

        # Buttons
        self.start_stop_button = tk.Button(self.master, text="Start", command=self.toggle_simulation)
        self.start_stop_button.pack()

        self.rewind_button = tk.Button(self.master, text="Rewind", command=self.rewind_simulation)
        self.rewind_button.pack()

        if self.configs:
            self.prev_button = tk.Button(self.master, text="Previous Config", command=self.show_previous_config)
            self.prev_button.pack(side=tk.LEFT)

            self.next_button = tk.Button(self.master, text="Next Config", command=self.show_next_config)
            self.next_button.pack(side=tk.RIGHT)

        # create labels to display additional information e.g max_gen, max_fitness etc.
        self.info_label = tk.Label(self.master, text="", fg="white", bg="#171717")
        self.info_label.pack()

        self.simulation_running = False
        self.iteration = 0

        self.update_canvas()
        self.update_info()

    def update_canvas(self):
        self.canvas.delete("all")
        for cell in self.grid.grid:
            i, j = cell
            self.canvas.create_rectangle(
                i * self.cell_size, j * self.cell_size,
                (i + 1) * self.cell_size, (j + 1) * self.cell_size,
                fill="#FFA500",
                outline="#FFA500"
            )

    def update_grid(self, new_grid: Grid):
        self.grid = new_grid
        self.update_canvas()

    def update_info(self):
        if self.configs:
            config = self.configs[self.current_config_index]
            self.info_label.config(
                text=f"Config {self.current_config_index + 1}/{len(self.configs)}: "
                     f"Max Gen: {config['max_gen']}, "
                     f"Max Fitness: {config['max_fitness']}, "
                     f"Max Size: {config['max_size']}"
            )
        else:
            self.info_label.config(text="No additional configurations loaded.")

    def toggle_simulation(self):
        if self.simulation_running:
            self.simulation_running = False
            self.start_stop_button.config(text="Start")
            self.master.title(f"Game of Life - Stopped at Iteration {self.iteration}")
        else:
            self.simulation_running = True
            self.start_stop_button.config(text="Stop")
            self.run_game_of_life()

    def rewind_simulation(self):
        # Reset the grid to its initial state and update the canvas
        self.simulation_running = False
        self.iteration = 0
        self.grid = self.initial_grid
        self.update_canvas()
        self.start_stop_button.config(text="Start")
        self.master.title("Game of Life - Rewinded")

    def run_game_of_life(self):
        if self.simulation_running:
            self.iteration += 1
            self.master.title(f"Game of Life - Iteration {self.iteration}")
            self.grid = GameOfLife(self.grid).run()
            self.update_grid(self.grid)
            self.master.after(60, self.run_game_of_life)

    def show_previous_config(self):
        if self.current_config_index > 0:
            self.current_config_index -= 1
            self.load_current_config()

    def show_next_config(self):
        if self.current_config_index < len(self.configs) - 1:
            self.current_config_index += 1
            self.load_current_config()

    def load_current_config(self):
        # Load the current configuration and reset the grid
        config = self.configs[self.current_config_index]
        self.grid = config["grid"]
        self.initial_grid = self.grid
        self.update_canvas()
        self.update_info()

        # Stop the simulation and reset state
        self.simulation_running = False
        self.iteration = 0
        self.start_stop_button.config(text="Start")
        self.master.title(f"Game of Life - Config {self.current_config_index + 1}")
