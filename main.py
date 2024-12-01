import random

from genetic_algorithm import random_initial_population, selection, crossover, calculate_fitness, mutate

import dataset as dt

def run_genetic_algorithm(pop_size: int, kind_of_selection: str, kind_of_crossover: str, recomb_prob: float, mutate_rate: float):
    ACTIVITIES = dt.base_data
    parents_pop = random_initial_population(pop_size, ACTIVITIES)
    RESOURCE_CAPACITY = dt.RESOURCE_CAPACITY
    MAX_GENERATIONS = 100

    makespan_with_list = []
    for chromosome in parents_pop:
        makespan_with_list.append(calculate_fitness(chromosome, ACTIVITIES, RESOURCE_CAPACITY))

    cnt = 0
    makespan_before = 0
    needed_generations = MAX_GENERATIONS
    for generation in range(MAX_GENERATIONS):
        if MAX_GENERATIONS // 4 == cnt:
            needed_generations += generation + 1
            break

        children_pop = []
        pool = selection(kind_of_selection, makespan_with_list)
        for gene in range(pop_size):
            recomb_prob_for_pair = random.uniform(0, 1)
            if recomb_prob_for_pair <= recomb_prob:
                child1, child2 = crossover(kind_of_crossover, pool[gene][0], pool[gene][1])
                child1 = mutate(mutate_rate, child1, ACTIVITIES)
                child2 = mutate(mutate_rate, child2, ACTIVITIES)
                children_pop.append(child1)
                children_pop.append(child2)
        # replace old population with new population
        # until a convergence or maximum of generations

        if makespan_with_list[0][2] == makespan_before:
            cnt += 1
        else:
            cnt = 0
            makespan_before = makespan_with_list[0][2]
    # return minimal_makespan and amount of needed generations
    pass