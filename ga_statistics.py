class GeneticAlgorithmStatistics:
    """
    A class to maintain and update statistics for a Genetic Algorithm.
    Attributes:
        statistics (dict): A dictionary to store various statistics of the Genetic Algorithm.
            - "max_gen" (int): The maximum generation number.
            - "max_fitness" (float): The maximum fitness value.
            - "max_size" (int): The maximum size of the population.
            - "best_candidate" (Any): The best candidate solution.
            
        statistics_history (dict): A dictionary to store the history of various statistics.
            - "max_gen" (list): The history of maximum generation numbers.
            - "max_fitness" (list): The history of maximum fitness values.
    Methods:
        set_stat(key, value):
            Sets the value of a specific statistic.
        update_stat(key, callable):
            Updates the value of a specific statistic using a callable function.
        get_stats():
            Returns the current statistics dictionary.
        get_history(key):
            Returns the history of a specific statistic.
        add_to_history(key, value):
            Adds a value to the history of a specific statistic.
    """
    statistics = {
        "max_gen": 0,
        "max_fitness": 0,
        "max_size": 0,
        "best_candidate": None
    }
    
    statistics_samples = {
        "gen_sample": [],
        "fitness_sample": []
    }
    
    @staticmethod
    def get_samples():
        return GeneticAlgorithmStatistics.statistics_samples
    
    @staticmethod
    def add_sample(key, value):
        GeneticAlgorithmStatistics.statistics_samples[key].append(value)
    
    @staticmethod
    def set_stat(key, value):
        # Check whether value is a function, if so invoke it
        if callable(value):
            GeneticAlgorithmStatistics.statistics[key] = value(GeneticAlgorithmStatistics.statistics[key])
        else:
            GeneticAlgorithmStatistics.statistics[key] = value
    
    @staticmethod
    def get_stats():
        return GeneticAlgorithmStatistics.statistics
