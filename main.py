import random as rnd
import time
import genetic_algorithm as ga
from dataset import RCPSP, RESOURCE_CAPACITY
rnd.seed(10)


def run_genetic_algorithm(sel_type: str, cross_type: str,
                          pop_size: int, recomb_prob: float,
                          mutation_prob: float, initial_pop: list
                          ):
    start_time = time.process_time()
    initial_pop = initial_pop.copy()
    no_improvements_counter = 0
    best_fitness = -1
    generation = 0
    pop = []
    elites_amount = pop_size // 5
    MAX_GENERATIONS = 100
    GENERATIONS_UNTIL_CONVERGENCE = MAX_GENERATIONS // 5

    for genotype in initial_pop:
        pop.append(ga.calculate_fitness(genotype, RCPSP, RESOURCE_CAPACITY))

    for generation in range(MAX_GENERATIONS):
        if no_improvements_counter == GENERATIONS_UNTIL_CONVERGENCE:
            break
        temp_offspring_pop = []
        pool = ga.selection(sel_type, pop)
        for parents in range(pop_size // 2):
            parents_recomb_prob = round(rnd.uniform(0, 1), 1)
            parent1, parent2 = pool[parents][0], pool[parents][1]
            if parents_recomb_prob <= recomb_prob:
                offspring1, offspring2 = ga.crossover(
                    cross_type, parent1, parent2
                )
            else:
                offspring1, offspring2 = parent1, parent2
            offspring1 = ga.mutation(mutation_prob, offspring1, RCPSP)
            offspring2 = ga.mutation(mutation_prob, offspring2, RCPSP)
            temp_offspring_pop.append(offspring1)
            temp_offspring_pop.append(offspring2)
        offspring_pop = []
        for genotype in temp_offspring_pop:
            offspring_pop.append(ga.calculate_fitness(
                genotype, RCPSP, RESOURCE_CAPACITY)
            )
        pop = ga.replacement(offspring_pop, pop, elites_amount)
        if pop[0][2] == best_fitness:
            no_improvements_counter += 1
        else:
            no_improvements_counter = 0
            best_fitness = pop[0][2]
    generation += 1
    cpu_time = time.process_time() - start_time
    print('Operators: ', sel_type, cross_type, '\nCPU-Time: ', cpu_time)
    print('Generation: ', generation, '\nMinimal Project Size: ', pop[0][2], '\n')
    # minimal project duration, generation, cpu_time and min schedule
    return pop[0][2], generation, cpu_time, pop[0][0]


def test_scenarios():
    pop_sizes = [50, 100]
    recomb_probs = [0.6, 0.9]
    mutation_probs = [0.03, 0.07]

    if any(value < 2 or 100 < value or value % 2 != 0 for value in pop_sizes):
        raise ValueError('Choose even population sizes between 2 and 100')
    if any(value < 0 or 1 < value for value in recomb_probs):
        raise ValueError('Choose recombination probabilities between 0 and 1')
    if any(value < 0 or 1 < value for value in mutation_probs):
        raise ValueError('Choose mutation probabilities between 0 and 1')
    if any(len(x) == 0 for x in [pop_sizes, recomb_probs, mutation_probs]):
        raise IndexError('Parameter lists should not be empty')

    par_combs = []
    for ps in pop_sizes:
        for rp in recomb_probs:
            for mp in mutation_probs:
                par_combs.append([ps, rp, mp])

    comb1, comb2, comb3, comb4 = [], [], [], []
    for pc in par_combs:
        print('Used parameters', pc, '\n')
        init_pop = ga.random_initial_population(pc[0], RCPSP)
        comb1.append(run_genetic_algorithm(
            'tournament', 'one_point', pc[0], pc[1], pc[2], init_pop))
        comb2.append(run_genetic_algorithm(
            'tournament', 'uniform', pc[0], pc[1], pc[2], init_pop))
        comb3.append(run_genetic_algorithm(
            'roulette', 'one_point', pc[0], pc[1], pc[2], init_pop))
        comb4.append(run_genetic_algorithm(
            'roulette', 'uniform', pc[0], pc[1], pc[2], init_pop))

    results = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for pc in range(len(par_combs)):
        for index in range(3):
            results[0][index] += comb1[pc][index]
            results[1][index] += comb2[pc][index]
            results[2][index] += comb3[pc][index]
            results[3][index] += comb4[pc][index]

    print('All_results', results)
    all_combs = comb1 + comb2 + comb3 + comb4
    min_schedule = sorted(all_combs, key=lambda x: x[0])[0][3]
    print('Minimal Schedule: ', min_schedule, '\n')

    all_combs = [comb1, comb2, comb3, comb4]
    operator_comb = ['Tournament AND One-Point', 'Tournament AND Uniform',
                     'Roulette AND One-Point', 'Roulette AND Uniform']
    combs_amount = len(all_combs)

    for comb_numb in range(combs_amount):
        print(f'{operator_comb[comb_numb]}',
              '\nAvg Minimal Project Duration: ',
              results[comb_numb][0] / len(par_combs),
              '\nAvg Generations\t: ',
              results[comb_numb][1] / len(par_combs),
              '\nAvg CPU-Time\t: ',
              round(results[comb_numb][2] / len(par_combs), 4),
              '\n', list(map(lambda x: x[0:3], all_combs[comb_numb])), '\n'
              )


test_scenarios()
