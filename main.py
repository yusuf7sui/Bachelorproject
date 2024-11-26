from genetic_algorithm import random_initial_population, selection, crossover, calculate_fitness

import dataset as dt

def run_genetic_algorithm(max_generations: int, pop_size: int, recource_capacity: int, kind_of_selection: str, kind_of_crossover: str, activities: list = dt.base_data):
    parents_pop = random_initial_population(pop_size, activities)

    makespan_with_list = []
    for chromosome in parents_pop:
        makespan_with_list.append(calculate_fitness(chromosome, activities, recource_capacity))

    cnt = 0
    makespan_before = 0
    needed_generations = 100
    for generation in range(max_generations):
        if max_generations // 4 == cnt:
            needed_generations += generation + 1
            break

        children_pop = []
        for gene in range(pop_size):
            pool = selection(kind_of_selection, makespan_with_list)
            # by probability make crossover-operators
            # select parent with selection operators

            # do crossover-operation

            # mutate child
        # replace old population with new population
        # until a convergence or maximum of generations
        if makespan_with_list[0][2] == makespan_before:
            cnt += 1
        else:
            cnt = 0
            makespan_before = makespan_with_list[0][2]
    # return minimal_makespan and amount of needed generations
    pass