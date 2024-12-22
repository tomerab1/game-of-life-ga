import random
from grid import Grid
from game_of_life import GameOfLife
from grid_builder import GridBuilder
from config import Config
from typing import List
from ga_statistics import GeneticAlgorithmStatistics

class GridFitnessCalculator:
    """
    A class used to calculate the fitness of a grid in a genetic algorithm context.
    Attributes
    ----------
    cache : dict
        A class-level cache to store previously calculated fitness values.
    Methods
    -------
    getStatistics():
        Returns the best candidate, maximum fitness, maximum generation, and maximum size statistics.
    is_stable_or_oscillating(grid: Grid, history: List[Grid]) -> bool:
        Determines if the given grid is stable or oscillating based on its history.
    calculate(grid: Grid) -> float:
        Calculates the fitness of the given grid. Uses a cache to store and retrieve previously calculated values.
    """
    
    cache = {}
    
    @staticmethod
    def getStatistics():
        return GridFitnessCalculator.best_candidate, GridFitnessCalculator.max_fitness, GridFitnessCalculator.max_gen, GridFitnessCalculator.max_size

    @staticmethod
    def is_stable_or_oscillating(grid: Grid, history: List[Grid]):
        return len(history) > 2 and grid in history

    @staticmethod
    def calculate(grid: Grid):
        grid_hash = hash(str(grid))

        if grid_hash in GridFitnessCalculator.cache:
            cached_grid, fitness, gen, max_size, stable_or_oscillating = GridFitnessCalculator.cache[grid_hash]
            
            if stable_or_oscillating:
                return fitness
            
            grid_cpy = cached_grid
            history = []
        else:
            grid_cpy = grid.copy()
            history = []
            gen = 0
            max_size = 0
            fitness = 1
            stable_or_oscillating = False
        
        history.append(grid_cpy.copy())
        while gen < Config.MAX_ITERATIONS:
            if GridFitnessCalculator.is_stable_or_oscillating(grid_cpy, history):
                stable_or_oscillating = True
                break
            
            if len(grid_cpy) > max_size:
                max_size = len(grid_cpy)
                GeneticAlgorithmStatistics.set_stat("max_size", lambda x: max(x, max_size))

            gen += 1
            history.append(grid_cpy.copy())
            grid_cpy = GameOfLife(grid_cpy).run()

        fitness += gen * 0.8 + max_size * 0.2
        GeneticAlgorithmStatistics.set_stat("max_fitness", lambda x: max(x, fitness))
        GeneticAlgorithmStatistics.set_stat("max_gen", lambda x: max(x, gen))

        GridFitnessCalculator.cache[grid_hash] = (grid_cpy, fitness, gen, max_size, stable_or_oscillating)
        return fitness


class GridMutator:
    """
    A class used to perform mutations on a grid.
    Methods
    -------
    mutate(grid: Grid):
        Mutates the given grid by either removing a random cell with a 50% probability
        or adding a random cell. Ensures the grid size does not exceed the maximum
        allowed cells.
    """
    @staticmethod
    def mutate(grid: Grid):
        if random.random() < 0.5:
            center_x, center_y = grid.get_random()
            for dx, dy in random.choices(Grid.ALLOWED_DIRS):
                grid.set_cell(center_x + dx, center_y + dy)
        else:  # Remove a random cell
            random_cell = grid.get_random()
            grid.set_cell(*random_cell, False)



class GridCrossover:
    """
    A class used to represent the crossover operation between two grids in a genetic algorithm.
    """
    """
        Perform a crossover operation between two grids to produce a new grid.
        The crossover operation involves selecting a random crossover point and combining cells
        from both parent grids up to that point to create a new grid.
        Parameters:
        grid1 (Grid): The first parent grid.
        grid2 (Grid): The second parent grid.
        Returns:
        Grid: A new grid resulting from the crossover of the two parent grids.
    """
    
    @staticmethod
    def crossover(grid1: Grid, grid2: Grid):
        new_grid = Grid()
        cell_count = max(len(grid1), len(grid2))
        crossover_points = random.sample(range(cell_count), k=2)
        
        for idx, cell in enumerate(grid1.grid):
            if idx < crossover_points[0] or idx > crossover_points[1]:
                new_grid.set_cell(*cell)

        for idx, cell in enumerate(grid2.grid):
            if crossover_points[0] <= idx <= crossover_points[1]:
                new_grid.set_cell(*cell)

        return new_grid

    
class GeneticAlgorithm:
    """
    A class to represent a Genetic Algorithm for optimizing grid-based solutions.
    Attributes
    ----------
    max_iterations : int
        The maximum number of iterations (generations) to run the algorithm.
    population_size : int
        The number of individuals in the population.
    population : list
        The current population of grid-based solutions.
    best_candidate : Grid
        The best candidate found during the algorithm's execution.
    best_fitness : float
        The fitness value of the best candidate.
    best_fitness_history : set
        A set to keep track of the best fitness values found in each generation.
    Methods
    -------
    _calculate_fitness():
        Calculates the fitness for all individuals in the population.
    _select(fitness):
        Selects two individuals from the population based on their fitness using roulette wheel selection.
    _update_best_candidate(candidate, fitness):
        Updates the best candidate if the provided candidate has a higher fitness.
    run():
        Runs the genetic algorithm for the specified number of iterations and returns the best candidate found.
    """
    def __init__(self, max_cells: int, max_iterations: int, population_size: int = 10):
        self.max_iterations = max_iterations
        self.population_size = population_size
        self.population = [GridBuilder().build(max_cells) for _ in range(population_size)]
        self.best_candidate = None 
        self.best_fitness = float('-inf')

    def _calculate_fitness(self):
        # Calculate fitness for all individuals
        return [GridFitnessCalculator.calculate(genom) for genom in self.population]
    
    # roulette wheel selection
    def _select(self, fitness):
        total_fitness = sum(fitness)
        probabilities = [f / total_fitness for f in fitness]
        return random.choices(self.population, weights=probabilities, k=2)

    def _update_best_candidate(self, candidate, fitness):
        if fitness > self.best_fitness:
            self.best_fitness = fitness
            self.best_candidate = candidate
            GeneticAlgorithmStatistics.set_stat("best_candidate", str(candidate.grid))

    def run(self):
        mutation_prob = 0.01
        for gen in range(self.max_iterations):
            fitness = self._calculate_fitness()
            avg_fitness = sum(fitness) / len(fitness)
            for i, grid in enumerate(self.population):
                self._update_best_candidate(grid, fitness[i])

            print(f"gen: #{gen}: best candidate found with fitness: {self.best_fitness}")
            
            GeneticAlgorithmStatistics.add_sample("gen_sample", gen)
            GeneticAlgorithmStatistics.add_sample("fitness_sample", avg_fitness)
            
            parent1, parent2 = self._select(fitness)
            child = GridCrossover.crossover(parent1, parent2)
            
            print(abs(self.best_fitness - avg_fitness), self.best_fitness, avg_fitness)
            
            # Checking if the best fitness - avg fitness is close enough (high selection pressure) to increase mutation rate (create more variety in the population)
            if abs(self.best_fitness - avg_fitness) < 0.1:
                print("High selection pressure detected ! Increasing mutation rate")
                mutation_prob = max(0.5, mutation_prob * 2)
            
            if random.random() < mutation_prob:
                GridMutator.mutate(child)
                
            self.population.append(child)

            weakest_index = fitness.index(min(fitness))
            del self.population[weakest_index]

        return self.best_candidate
