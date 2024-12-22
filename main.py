import tkinter as tk
import sys
from ga import GeneticAlgorithm
from config import Config
from ui import UI
from ga_statistics import GeneticAlgorithmStatistics
from json_serde import JsonSerde
from grid import Grid
import matplotlib.pyplot as plt

def print_usage():
    print("Usage: python main.py [--load-configs | --run-ga]")

def plot_statistics_history(samples):
    generations = samples["gen_sample"]
    fitness = samples["fitness_sample"]

    plt.figure(dpi=150)
    plt.plot(generations, fitness, linestyle='-', linewidth=1, label="Fitness")
    
    plt.title("Genetic Algorithm Fitness Over Generations")
    plt.xlabel("Generation")
    plt.ylabel("Average Fitness")
    plt.grid()
    plt.legend()
    plt.show()

def handle_load_configs():
    serde = JsonSerde("configs.json")
    objs = serde.deserialize()
    
    # Convert the deserialized objects to the expected format
    configs = [
        {
            **stat,
            "grid": Grid.from_string(stat["best_candidate"])
        }
            for stat in objs
        ]
    initial_grid = configs[0]["grid"] if configs else Grid()

    root = tk.Tk()
    UI(root, initial_grid, configs=configs)
    root.mainloop()    

def handle_run_ga():
    # Run genetic algorithm
    algo = GeneticAlgorithm(Config.MAX_CELLS, 250, 50)
    sparse_grid = algo.run()

    # Save statistics
    statistics = GeneticAlgorithmStatistics.get_stats()
    serde = JsonSerde("configs.json")
    serde.serialize(statistics)
    
    # store the statistics about the current run of the ga in the expected format
    configs = [statistics]
    root = tk.Tk()
    UI(root, sparse_grid, configs=configs)
    root.mainloop()

def main():
    # This option loads the best configurations from a file and allows to browse between them
    if len(sys.argv) > 1 and sys.argv[1] == "--load-configs":
        handle_load_configs()  
    # This option runs the genetic algorithm to find the best configurations and stores the in the file
    elif len(sys.argv) > 1 and sys.argv[1] == "--run-ga":
        handle_run_ga()
        plot_statistics_history(GeneticAlgorithmStatistics.get_samples())
    else:
        print_usage()

if __name__ == "__main__":
    main()
