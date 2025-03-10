import genetic_algorithm as ga
from dataset import RCPSP, RESOURCE_CAPACITY
import time
import random as rnd
rnd.seed(10)


def start_genetic_algorithm(sel_type: str, recomb_type: str,
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
    CONVERGENCE = MAX_GENERATIONS // 5
    for genotype in initial_pop:
        pop.append(ga.calculate_fitness(genotype, RCPSP, RESOURCE_CAPACITY))
    pop = sorted(pop, key=lambda x: x[2])
    for generation in range(MAX_GENERATIONS):
        temp_offspring_pop = []
        pool = ga.select(sel_type, pop)
        for parents in range(pop_size // 2):
            parents_recomb_prob = round(rnd.uniform(0, 1), 1)
            parent1, parent2 = pool[parents][0], pool[parents][1]
            if parents_recomb_prob <= recomb_prob:
                offspring1, offspring2 = ga.recombine(
                    recomb_type, parent1, parent2)
            else:
                offspring1, offspring2 = parent1, parent2
            offspring1 = ga.mutate(mutation_prob, offspring1, RCPSP)
            offspring2 = ga.mutate(mutation_prob, offspring2, RCPSP)
            temp_offspring_pop.append(offspring1)
            temp_offspring_pop.append(offspring2)
        offspring_pop = []
        for genotype in temp_offspring_pop:
            offspring_pop.append(ga.calculate_fitness(
                genotype, RCPSP, RESOURCE_CAPACITY))
        pop = ga.replace(offspring_pop, pop, elites_amount)
        if pop[0][2] == best_fitness:
            no_improvements_counter += 1
        else:
            no_improvements_counter = 0
            best_fitness = pop[0][2]
        if no_improvements_counter == CONVERGENCE:
            break
    generation += 1
    dec_place = 4
    cpu_time = round(time.process_time() - start_time, dec_place)
    # minimal project duration, generation, cpu_time and min schedule
    return pop[0][2], generation, cpu_time, pop[0][0]


def test_scenarios():
    pop_sizes = [50, 60]
    recomb_probs = [0.7, 0.9]
    mutation_probs = [0.05, 0.1]
    print('Program has been started.\n'
          'Please wait until the results will be shown.\n')
    par_combs = []
    for ps in pop_sizes:
        for rp in recomb_probs:
            for mp in mutation_probs:
                par_combs.append([ps, rp, mp])
    comb1, comb2, comb3, comb4 = [], [], [], []
    for pc in par_combs:
        init_pop = ga.generate_initial_population(pc[0], RCPSP)
        comb1.append(start_genetic_algorithm(
            'tournament', 'one_point', pc[0], pc[1], pc[2], init_pop))
        comb2.append(start_genetic_algorithm(
            'tournament', 'uniform', pc[0], pc[1], pc[2], init_pop))
        comb3.append(start_genetic_algorithm(
            'roulette', 'one_point', pc[0], pc[1], pc[2], init_pop))
        comb4.append(start_genetic_algorithm(
            'roulette', 'uniform', pc[0], pc[1], pc[2], init_pop))
    results = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for pc in range(len(par_combs)):
        for index in range(3):
            results[0][index] += comb1[pc][index]
            results[1][index] += comb2[pc][index]
            results[2][index] += comb3[pc][index]
            results[3][index] += comb4[pc][index]
    all_combs = comb1 + comb2 + comb3 + comb4
    best_result = sorted(all_combs, key=lambda x: (x[0], x[1], x[2]))[0]
    print('Best single result: ', best_result[0:3])
    print('Minimal schedule: ', best_result[3], '\n')
    all_combs = [comb1, comb2, comb3, comb4]
    operator_comb = ['Tournament and One-Point', 'Tournament and Uniform',
                     'Roulette and One-Point', 'Roulette and Uniform']
    combs_amount = len(all_combs)
    dec_point = 4
    for comb_numb in range(combs_amount):
        print(f'{operator_comb[comb_numb]}',
              '\nAvg Minimal Project Duration: ',
              results[comb_numb][0] / len(par_combs),
              '\nAvg Generations\t: ',
              results[comb_numb][1] / len(par_combs),
              '\nAvg CPU-Time\t: ',
              round(results[comb_numb][2] / len(par_combs), dec_point),
              '\n', list(map(lambda x: x[0:3], all_combs[comb_numb])), '\n')


test_scenarios()

'''
Best single result:  (48, 27, 1.0)
Minimal schedule:  {0: 0, 3: 8, 4: 2, 9: 4, 1: 6, 2: 9, 5: 13, 10: 12, 6: 13, 11: 15, 8: 22, 7: 25, 15: 27, 16: 20, 14: 32, 13: 35, 17: 30, 20: 37, 21: 33, 12: 36, 18: 42, 26: 39, 25: 40, 28: 44, 19: 43, 24: 48, 23: 48, 22: 44, 27: 48, 29: 48} 

Tournament and One-Point 
Avg Minimal Project Duration:  48.5 
Avg Generations	:  30.25 
Avg CPU-Time	:  0.7617 
 [(49, 28, 0.7188), (48, 27, 1.0), (48, 31, 0.7969), (48, 32, 0.7656), (48, 39, 0.9062), (49, 29, 0.625), (49, 30, 0.9219), (49, 26, 0.3594)] 

Tournament and Uniform 
Avg Minimal Project Duration:  49.0 
Avg Generations	:  29.375 
Avg CPU-Time	:  0.791 
 [(49, 25, 0.8594), (49, 28, 1.0781), (50, 27, 0.7188), (49, 40, 1.1875), (49, 22, 0.5469), (49, 26, 0.5156), (49, 31, 0.7344), (48, 36, 0.6875)] 

Roulette and One-Point 
Avg Minimal Project Duration:  49.0 
Avg Generations	:  28.375 
Avg CPU-Time	:  0.6973 
 [(49, 32, 1.1719), (49, 27, 0.875), (49, 31, 0.75), (49, 23, 0.5625), (49, 24, 0.5469), (49, 29, 0.4531), (49, 35, 0.6875), (49, 26, 0.5312)] 

Roulette and Uniform 
Avg Minimal Project Duration:  49.375 
Avg Generations	:  29.125 
Avg CPU-Time	:  0.7891 
 [(49, 31, 1.1562), (49, 37, 0.9688), (50, 28, 0.7812), (50, 24, 0.4844), (48, 38, 0.9688), (50, 26, 0.5781), (50, 22, 0.5625), (49, 27, 0.8125)] 
'''