
# Project Title

An implementation of a genetic algorithm that finds long-lived configurations (Metushelachs) in Conway's Game of Life.

## Features

- **Genetic Algorithm (GA):** Implementation and statistics tracking.
- **Grid Management:** Includes grid building and operations.
- **Game of Life:** Simulation of Conway's Game of Life.
- **UI:** Interactive user interface for visualizing operations.
- **JSON Serialization:** Handling configuration and statistics using JSON.

## Project Structure

- `config.py`: Contains configuration settings for the project.
- `ga.py`: Implements genetic algorithm logic.
- `game_of_life.py`: Simulates Conway's Game of Life.
- `ga_statistics.py`: Tracks and analyzes GA statistics.
- `grid.py`: Manages grid operations.
- `grid_builder.py`: Constructs and configures grids.
- `json_serde.py`: Handles JSON serialization and deserialization.
- `main.py`: Entry point of the application.
- `requirements.txt`: Lists Python dependencies.
- `configs.json`: Stores the initial game of life configurations that the ga found.
- `ui.py`: Implements the user interface.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your_username/your_repo_name.git
   ```
2. Navigate to the project directory:
   ```bash
   cd your_repo_name
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application using:
```bash
python main.py
```

## Requirements

Ensure you have Python 3.8 or higher installed. All dependencies are listed in `requirements.txt`.

## License

This project is proprietary and all rights are reserved by the author. The following restrictions apply:

- Academic Integrity: This code may not be copied, reused, or submitted as part of any coursework, academic projects, or other assignments without explicit, written permission from the author.

- Non-Commercial Use: This code may not be used for commercial purposes.

- No Redistribution: Redistribution of this code in any form, modified or unmodified, is strictly prohibited.

- Personal Use Only: The code is provided for personal review and educational purposes only.

- No Permissions Granted: No permissions will be granted for any use beyond personal review.

## Acknowledgments

- Inspiration: Conway's Game of Life.
- Libraries used: Listed in `requirements.txt`.
