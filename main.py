from genetic_algorithm import random_initial_population, selection, crossover

import dataset as dt

def run_genetic_algorithm(max_generations: int, pop_size: int, activities: list = dt.base_data):
    parents_pop = random_initial_population(pop_size, activities)

    for generation in range(max_generations):
        # select parent with selection operators

        # do crossover-operation

        # replace old population with new population

        # until a convergence or maximum of generations
        pass
    pass
