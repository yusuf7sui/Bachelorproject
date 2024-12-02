import random

from genetic_algorithm import random_initial_population, selection, crossover, calculate_fitness, mutate, replace

import dataset as dt

def run_genetic_algorithm(pop_size: int, kind_of_selection: str, kind_of_crossover: str, recomb_prob: float, mutate_rate: float):
    ACTIVITIES = dt.base_data
    parents_pop = random_initial_population(pop_size, ACTIVITIES)
    RESOURCE_CAPACITY = dt.RESOURCE_CAPACITY
    MAX_GENERATIONS = 100
    ELITSM_AMOUNT = pop_size // 4

    makespan_with_list = []
    for chromosome in parents_pop:
        makespan_with_list.append(calculate_fitness(chromosome, ACTIVITIES, RESOURCE_CAPACITY))

    count_of_no_improvement = 1
    makespan_before = -1
    for generation in range(MAX_GENERATIONS):
        if MAX_GENERATIONS // 4 == count_of_no_improvement:
            break

        children_pop = []
        pool = selection(kind_of_selection, makespan_with_list)
        for parent_pair in range(pop_size // 2): # because 2 childs max per parent_pair
            recomb_prob_for_pair = round(random.uniform(0, 1), 3)
            if recomb_prob_for_pair <= recomb_prob:
                child1, child2 = crossover(kind_of_crossover, pool[parent_pair][0], pool[parent_pair][1])
                child1 = mutate(mutate_rate, child1, ACTIVITIES)
                child2 = mutate(mutate_rate, child2, ACTIVITIES)
                children_pop.append(child1)
                children_pop.append(child2)
        makespan_with_list = replace(children_pop, makespan_with_list, ACTIVITIES, pop_size, RESOURCE_CAPACITY, ELITSM_AMOUNT)

        # until a convergence or maximum of generations
        if makespan_with_list[0][2] == makespan_before:
            count_of_no_improvement += 1
        else:
            count_of_no_improvement = 0
            makespan_before = makespan_with_list[0][2]
        print("#####", generation, "######")
        print(makespan_with_list[0][2])
    print(makespan_with_list[0][0])
    print(makespan_with_list[0][1])  # makespan_list[0][1] as the best parent
    # In python possible to use variable in for-loop afterwards
    return makespan_with_list[0][2], generation # return minimal_makespan and amount of needed generations

#print(run_genetic_algorithm(20, 'test', 'test', 0.75, 0.01))