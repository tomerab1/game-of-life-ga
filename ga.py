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
    Supports multiple mutation strategies.
    """
    @staticmethod
    def mutate(grid: Grid, strategy: str = "default"):
        if strategy == "aggressive":
            # Mutate multiple cells at once
            num_mutations = random.randint(2, 5)
            for _ in range(num_mutations):
                GridMutator._single_mutate(grid)
        elif strategy == "swap":
            # Remove one cell and add another
            if len(grid) > 0:
                old_cell = grid.get_random()
                grid.set_cell(*old_cell, False)
                new_x = random.randint(0, Config.MAX_GRID_SIZE)
                new_y = random.randint(0, Config.MAX_GRID_SIZE)
                grid.set_cell(new_x, new_y)
        else:
            GridMutator._single_mutate(grid)

    @staticmethod
    def _single_mutate(grid: Grid):
        if random.random() < 0.5:
            center_x, center_y = grid.get_random()
            for dx, dy in random.choices(Grid.ALLOWED_DIRS):
                grid.set_cell(center_x + dx, center_y + dy)
        else:
            random_cell = grid.get_random()
            grid.set_cell(*random_cell, False)


class GridCrossover:
    """
    A class used to represent the crossover operation between two grids.
    Supports uniform and two-point crossover.
    """

    @staticmethod
    def crossover(grid1: Grid, grid2: Grid, method: str = "two_point"):
        if method == "uniform":
            return GridCrossover._uniform_crossover(grid1, grid2)
        return GridCrossover._two_point_crossover(grid1, grid2)

    @staticmethod
    def _two_point_crossover(grid1: Grid, grid2: Grid):
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

    @staticmethod
    def _uniform_crossover(grid1: Grid, grid2: Grid):
        new_grid = Grid()
        all_cells = set(grid1.grid) | set(grid2.grid)

        for cell in all_cells:
            if random.random() < 0.5:
                new_grid.set_cell(*cell)

        return new_grid


class GeneticAlgorithm:
    """
    A class to represent a Genetic Algorithm for optimizing grid-based solutions.
    Now uses tournament selection and elitism.
    """
    def __init__(self, max_cells: int, max_iterations: int, population_size: int = 10):
        self.max_iterations = max_iterations
        self.population_size = population_size
        self.population = [GridBuilder().build(max_cells) for _ in range(population_size)]
        self.best_candidate = None
        self.best_fitness = float('-inf')
        self.stagnation_counter = 0
        self.last_best_fitness = float('-inf')

    def _calculate_fitness(self):
        return [GridFitnessCalculator.calculate(genom) for genom in self.population]

    def _tournament_select(self, fitness):
        """Tournament selection - pick TOURNAMENT_SIZE random individuals, return the best."""
        selected = []
        for _ in range(2):
            tournament_indices = random.sample(range(len(self.population)), Config.TOURNAMENT_SIZE)
            best_idx = max(tournament_indices, key=lambda i: fitness[i])
            selected.append(self.population[best_idx])
        return selected

    def _update_best_candidate(self, candidate, fitness):
        if fitness > self.best_fitness:
            self.best_fitness = fitness
            self.best_candidate = candidate
            GeneticAlgorithmStatistics.set_stat("best_candidate", str(candidate.grid))

    def _get_elite(self, fitness):
        """Return the top ELITISM_COUNT individuals."""
        paired = list(zip(fitness, self.population))
        paired.sort(key=lambda x: x[0], reverse=True)
        return [individual for _, individual in paired[:Config.ELITISM_COUNT]]

    def _adapt_mutation_rate(self, mutation_rate, avg_fitness):
        """Increase mutation rate when population converges (stagnation detection)."""
        if abs(self.best_fitness - self.last_best_fitness) < 0.001:
            self.stagnation_counter += 1
        else:
            self.stagnation_counter = 0

        self.last_best_fitness = self.best_fitness

        if self.stagnation_counter > 10:
            return min(Config.MAX_MUTATION_RATE, mutation_rate * 2)

        return Config.INITIAL_MUTATION_RATE

    def run(self):
        mutation_rate = Config.INITIAL_MUTATION_RATE

        for gen in range(self.max_iterations):
            fitness = self._calculate_fitness()
            avg_fitness = sum(fitness) / len(fitness)

            for i, grid in enumerate(self.population):
                self._update_best_candidate(grid, fitness[i])

            GeneticAlgorithmStatistics.add_sample("gen_sample", gen)
            GeneticAlgorithmStatistics.add_sample("fitness_sample", avg_fitness)

            # Preserve elite individuals
            elite = self._get_elite(fitness)

            # Build new population
            new_population = list(elite)

            while len(new_population) < self.population_size:
                parent1, parent2 = self._tournament_select(fitness)

                if random.random() < Config.CROSSOVER_RATE:
                    child = GridCrossover.crossover(parent1, parent2)
                else:
                    child = parent1.copy()

                # Determine mutation strategy based on stagnation
                if self.stagnation_counter > 20:
                    strategy = "aggressive"
                elif self.stagnation_counter > 10:
                    strategy = "swap"
                else:
                    strategy = "default"

                if random.random() < mutation_rate:
                    GridMutator.mutate(child, strategy)

                new_population.append(child)

            self.population = new_population
            mutation_rate = self._adapt_mutation_rate(mutation_rate, avg_fitness)

        return self.best_candidate
