import random
import time
from genetic_algorithm import random_initial_population, selection, crossover, calculate_fitness, mutate, replace
import dataset as dt

# Genetic Algorithm runs with corresponding parameters
def run_genetic_algorithm(kind_of_selection: str, kind_of_crossover: str, pop_size: int, recomb_prob: float, mutate_rate: float, initial_pop: list):
    start_time = time.process_time()
    ACTIVITIES = dt.base_data
    initial_population = initial_pop.copy() #because needed for other combinations
    RESOURCE_CAPACITY = dt.RESOURCE_CAPACITY
    MAX_GENERATIONS = 100
    ELITISM_AMOUNT = pop_size // 5

    individuals_with_fitness = []
    for genotype in initial_population:
        individuals_with_fitness.append(calculate_fitness(genotype, ACTIVITIES, RESOURCE_CAPACITY))

    count_of_no_improvement = 1
    makespan_before = -1
    generation = 0
    for generation in range(MAX_GENERATIONS):
        # until a convergence or maximum of generations is reached
        if MAX_GENERATIONS // 10 == count_of_no_improvement:
            break

        children_pop = []
        pool = selection(kind_of_selection, individuals_with_fitness)
        for pair in range(pop_size // 2):
            pairs_recombine_prob = round(random.uniform(0, 1), 3)
            if pairs_recombine_prob <= recomb_prob:
                child1, child2 = crossover(kind_of_crossover, pool[pair][0], pool[pair][1])
                child1 = mutate(mutate_rate, child1, ACTIVITIES)
                child2 = mutate(mutate_rate, child2, ACTIVITIES)
                children_pop.append(child1)
                children_pop.append(child2)
        individuals_with_fitness = replace(children_pop, individuals_with_fitness, ACTIVITIES, pop_size, RESOURCE_CAPACITY, ELITISM_AMOUNT)

        if individuals_with_fitness[0][2] == makespan_before:
            count_of_no_improvement += 1
        else:
            count_of_no_improvement = 0
            makespan_before = individuals_with_fitness[0][2]
        print("#####", generation, "######")
        print(individuals_with_fitness[0][2])
    print(individuals_with_fitness[0][0])
    print(individuals_with_fitness[0][1])  # makespan_list[0][1] as the best parent
    # In python possible to use variable in for-loop afterwards
    print('Nedded Generations: ', generation)
    finish_time = time.process_time() - start_time
    print('CPU Time:', finish_time)
    return individuals_with_fitness[0][2], generation, finish_time, individuals_with_fitness[0][0]
# maybe also return the finish time [0][0], with genotypes as dict to safe the best results and then return it back

# temporary test: print(run_genetic_algorithm(20, 'test', 'test', 0.75, 0.01))
# Function to test possible scenarios
def test_scenarios():
    mutation_rate = [0.001, 0.01]
    recombination_probability = [0.4, 0.7]
    population_size = [10, 20]

    parameter_comb = []
    for ps in population_size:
        for rp in recombination_probability:
            for mr in mutation_rate:
                parameter_comb.append([ps, rp, mr])

    first_comb = []
    second_comb = []
    third_comb = []
    fourth_comb = []
    cnt = 0
    for param in parameter_comb:
        initial = random_initial_population(param[0], dt.base_data)
        first_comb.append(run_genetic_algorithm('one_point_crossover','tournament_selection', param[0], param[1], param[2], initial))
        second_comb.append(run_genetic_algorithm('uniform_crossover', 'tournament_selection', param[0], param[1], param[2], initial))
        third_comb.append(run_genetic_algorithm('one_point_crossover', 'roulette_method', param[0], param[1], param[2], initial))
        fourth_comb.append(run_genetic_algorithm('uniform_crossover', 'roulette_method', param[0], param[1], param[2], initial))
        print(param, ' param')
        print(cnt, 'cnt')
        cnt += 1


    avg_results = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for para_comb in range(len(parameter_comb)):
        for res in range(3):
            avg_results[0][res] += first_comb[para_comb][res]
            avg_results[1][res] += second_comb[para_comb][res]
            avg_results[2][res] += third_comb[para_comb][res]
            avg_results[3][res] += fourth_comb[para_comb][res]
            print(para_comb, ' Paracomb')

    print(avg_results[0], avg_results[1], avg_results[2], first_comb, 'Tests')

    # calculate minimal schedule and print
    all_comb = first_comb + second_comb + third_comb + fourth_comb
    min_schedule = sorted(all_comb, key=lambda x: x[0])
    print('Minimal Schedule: ', min_schedule[0][3])

    all_comb = [first_comb, second_comb, third_comb, fourth_comb]
    combinations = ['One-Point_AND_Tournament', 'Uniform_AND_Tournamnt', 'One-Point_AND_Roulette', 'Uniform_AND_Roulette']
    # calculate average results for all combinations and print
    for comb_numb in range(4):
        print(f'{combinations[comb_numb]}\n', 'Avg Makespan\t: ', avg_results[comb_numb][0] / 8, 'Avg Generation\t: ',
                    avg_results[comb_numb][1] / 8, ' Avg CPU\t: ',
                    round(avg_results[comb_numb][2] / 8, 4), '\n', list(map(lambda x: x[0:3], all_comb[comb_numb])))

test_scenarios()