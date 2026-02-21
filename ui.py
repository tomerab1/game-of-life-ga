import tkinter as tk
from grid import Grid
from game_of_life import GameOfLife
from config import Config


class UI:
    SPEED_PRESETS = {
        "Slow": 200,
        "Normal": 60,
        "Fast": 16,
        "Ludicrous": 1,
    }

    def __init__(self, master, grid: Grid, configs=None):
        self.master = master
        self.master.title("Game of Life")
        self.initial_grid = grid
        self.grid = grid
        self.cell_size = 10
        self.configs = configs or []
        self.current_config_index = 0
        self.speed = self.SPEED_PRESETS["Normal"]

        # Create canvas with background color
        self.canvas = tk.Canvas(
            self.master,
            width=Config.MAX_GRID_SIZE * self.cell_size,
            height=Config.MAX_GRID_SIZE * self.cell_size,
            bg="#171717"
        )
        self.canvas.pack()

        # Control frame
        control_frame = tk.Frame(self.master)
        control_frame.pack()

        self.start_stop_button = tk.Button(control_frame, text="Start", command=self.toggle_simulation)
        self.start_stop_button.pack(side=tk.LEFT, padx=4)

        self.rewind_button = tk.Button(control_frame, text="Rewind", command=self.rewind_simulation)
        self.rewind_button.pack(side=tk.LEFT, padx=4)

        # Speed selector
        speed_frame = tk.Frame(self.master)
        speed_frame.pack()

        tk.Label(speed_frame, text="Speed:").pack(side=tk.LEFT)
        self.speed_var = tk.StringVar(value="Normal")
        for name in self.SPEED_PRESETS:
            tk.Radiobutton(
                speed_frame,
                text=name,
                variable=self.speed_var,
                value=name,
                command=self._on_speed_change,
            ).pack(side=tk.LEFT)

        if self.configs:
            nav_frame = tk.Frame(self.master)
            nav_frame.pack()

            self.prev_button = tk.Button(nav_frame, text="Previous Config", command=self.show_previous_config)
            self.prev_button.pack(side=tk.LEFT)

            self.next_button = tk.Button(nav_frame, text="Next Config", command=self.show_next_config)
            self.next_button.pack(side=tk.RIGHT)

        # create labels to display additional information e.g max_gen, max_fitness etc.
        self.info_label = tk.Label(self.master, text="", fg="white", bg="#171717")
        self.info_label.pack()

        self.simulation_running = False
        self.iteration = 0

        self.update_canvas()
        self.update_info()

    def _on_speed_change(self):
        self.speed = self.SPEED_PRESETS[self.speed_var.get()]

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
            self.master.after(self.speed, self.run_game_of_life)

    def show_previous_config(self):
        if self.current_config_index > 0:
            self.current_config_index -= 1
            self.load_current_config()

    def show_next_config(self):
        if self.current_config_index < len(self.configs) - 1:
            self.current_config_index += 1
            self.load_current_config()

    def load_current_config(self):
        config = self.configs[self.current_config_index]
        self.grid = config["grid"]
        self.initial_grid = self.grid
        self.update_canvas()
        self.update_info()

        self.simulation_running = False
        self.iteration = 0
        self.start_stop_button.config(text="Start")
        self.master.title(f"Game of Life - Config {self.current_config_index + 1}")
