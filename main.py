import random
import time
from genetic_algorithm import random_initial_population, selection, crossover, calculate_fitness, mutate, replace
import dataset as dt

# Genetic Algorithm runs with corresponding parameters
def run_genetic_algorithm(kind_of_selection: str, kind_of_crossover: str, pop_size: int, recomb_prob: float, mutate_rate: float, initial_pop: list):
    start_time = time.process_time()
    initial_population = initial_pop.copy() #because needed for other combinations
    MAX_GENERATIONS = 100
    elitism_amount = pop_size // 5

    individuals_with_fitness = []
    for genotype in initial_population:
        individuals_with_fitness.append(calculate_fitness(genotype, dt.BASE_RCPSP, dt.RESOURCE_CAPACITY))

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
                child1 = mutate(mutate_rate, child1, dt.BASE_RCPSP)
                child2 = mutate(mutate_rate, child2, dt.BASE_RCPSP)
                children_pop.append(child1)
                children_pop.append(child2)
        individuals_with_fitness = replace(children_pop, individuals_with_fitness, dt.BASE_RCPSP, pop_size, dt.RESOURCE_CAPACITY, elitism_amount)

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
    population_sizes = [10, 20]
    recombination_probabilities = [0.4, 0.7]
    mutation_rates = [0.001, 0.01]

    parameter_comb = []
    for ps in population_sizes:
        for rp in recombination_probabilities:
            for mr in mutation_rates:
                parameter_comb.append([ps, rp, mr])

    first_comb = []
    second_comb = []
    third_comb = []
    fourth_comb = []
    cnt = 0
    for pc in parameter_comb:
        initial = random_initial_population(pc[0], dt.BASE_RCPSP)
        first_comb.append(run_genetic_algorithm(
            'tournament','one-point', pc[0], pc[1], pc[2], initial))
        second_comb.append(run_genetic_algorithm(
            'tournament', 'uniform', pc[0], pc[1], pc[2], initial))
        third_comb.append(run_genetic_algorithm(
            'roulette', 'one-point', pc[0], pc[1], pc[2], initial))
        fourth_comb.append(run_genetic_algorithm(
            'roulette', 'uniform', pc[0], pc[1], pc[2], initial))
        print(pc, ' param')
        print(cnt, 'cnt')
        cnt += 1

    avg_results = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for pc in range(len(parameter_comb)):
        for res in range(3):
            avg_results[0][res] += first_comb[pc][res]
            avg_results[1][res] += second_comb[pc][res]
            avg_results[2][res] += third_comb[pc][res]
            avg_results[3][res] += fourth_comb[pc][res]
            print(pc, 'Parameter comb')

    print(avg_results, first_comb, 'Tests')

    # calculate minimal schedule and print
    all_comb = first_comb + second_comb + third_comb + fourth_comb
    min_schedule = sorted(all_comb, key=lambda x: x[0])
    print('Minimal schedule: ', min_schedule[0][3])

    all_comb = [first_comb, second_comb, third_comb, fourth_comb]
    combinations = ['Tournament_AND_One-Point', 'Tournament_AND_Uniform', 'Roulette_AND_One-Point', 'Roulette_AND_Uniform']
    # calculate average results for all combinations and print
    for comb_numb in range(4):
        print(f'{combinations[comb_numb]}\n', 'Avg Makespan\t: ', avg_results[comb_numb][0] / 8,
              'Avg Generation-Amount\t: ', avg_results[comb_numb][1] / 8, ' Avg CPU-Time\t: ',
              round(avg_results[comb_numb][2] / 8, 4), '\n', list(map(lambda x: x[0:3], all_comb[comb_numb])))


test_scenarios()