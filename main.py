import random

from genetic_algorithm import random_initial_population, selection, crossover, calculate_fitness, mutate, replace

import dataset as dt

def run_genetic_algorithm(kind_of_selection: str, kind_of_crossover: str, pop_size: int, recomb_prob: float, mutate_rate: float, initial_pop: list[list]):
    ACTIVITIES = dt.base_data
    parents_pop = initial_pop.copy()
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
    print('Nedded Generations: ', generation)
    return makespan_with_list[0][2], generation # return minimal_makespan and amount of needed generations

#print(run_genetic_algorithm(20, 'test', 'test', 0.75, 0.01))

def test_scenarios(data: list):
    mutation_rate = [0.01, 0.1]
    recombination_probability = [0.5, 0.75]
    population_size = [8, 8]

    operator_comb = []
    for po in population_size:
        for rp in recombination_probability:
            for mr in mutation_rate:
                operator_comb.append([po, rp, mr])

    first_comb = []
    second_comb = []
    third_comb = []
    fourth_comb = []
    for param in operator_comb:
        initial = random_initial_population(param[0], dt.base_data)
        first_comb.append(run_genetic_algorithm('one_point_crossover', 'tournament_selection', param[0], param[1], param[2], initial))
        second_comb.append(run_genetic_algorithm('uniform_crossover', 'tournament_selection', param[0], param[1], param[2], initial))
        third_comb.append(run_genetic_algorithm('one_point_crossover', 'roulette_method', param[0], param[1], param[2], initial))
        fourth_comb.append(run_genetic_algorithm('uniform_crossover', 'roulette_method', param[0], param[1], param[2], initial))
    a1, b1, c1, d1 = 0, 0, 0, 0
    a2, b2, c2, d2 = 0, 0, 0, 0
    for z in range(8):
        a1 += first_comb[z][0]
        b1 += second_comb[z][0]
        c1 += third_comb[z][0]
        d1 += fourth_comb[z][0]
        a2 += first_comb[z][1]
        b2 += second_comb[z][1]
        c2 += third_comb[z][1]
        d2 += fourth_comb[z][1]
    print('One-Point_AND_Tournament: \t', 'Avg Makespan: ',  a1 / 8, ' Avg Generation: ', a2 / 8, first_comb)
    print('Uniform_AND_Tournament: \t', 'Avg Makespan: ', b1 / 8, ' Avg Generation: ', b2 / 8, second_comb)
    print('One-Point_AND_Roulette: \t', 'Avg Makespan: ', c1 / 8, ' Avg Generation: ', c2 / 8, third_comb)
    print('Uniform_AND_Roulette: \t', 'Avg Makespan: ', d1 / 8, ' Avg Generation: ', d2 / 8, fourth_comb)

test_scenarios(dt.base_data)