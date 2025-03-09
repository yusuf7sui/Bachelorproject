from schedule import serial_SGS_for_activity_lists
import random as rnd
rnd.seed(10)


def generate_initial_population(pop_size: int, rcpsp: list):
    temp_pop = []
    for _ in range(pop_size):
        temp_genotype = []
        for allele in range(len(rcpsp)):
            temp_genotype.append(allele)
        temp_pop.append(temp_genotype)
    random_pop = []
    for temp_genotype in temp_pop:
        first_gene = [temp_genotype[0]]
        temp_genotype.remove(temp_genotype[0])
        rnd.shuffle(temp_genotype)
        shuffled_genotype = first_gene + temp_genotype
        random_pop.append(sort_alleles(shuffled_genotype, rcpsp))
    return random_pop


def sort_alleles(shuffled_genotype: list, rcpsp: list):
    sorted_genotype = [shuffled_genotype[0]]
    shuffled_genotype.remove(shuffled_genotype[0])
    while len(sorted_genotype) != len(rcpsp):
        for allele in shuffled_genotype:
            if sorted_genotype.count(allele) == 1:
                continue
            pred_assigned_before = True
            for pred in rcpsp[allele][2]:
                if pred not in sorted_genotype:
                    pred_assigned_before = False
            if pred_assigned_before:
                sorted_genotype.append(allele)
    return sorted_genotype


def recombine(recomb_type: str, parent1: list, parent2: list):
    if recomb_type == 'one_point':
        return one_point_crossover(parent1, parent2)
    else:
        return uniform_crossover(parent1, parent2)


def one_point_crossover(parent1: list, parent2: list):
    offspring1, offspring2 = [], []
    crosspoint = rnd.randint(1, len(parent1) - 1)
    for gene in range(crosspoint):
        offspring1.append(parent1[gene])
        offspring2.append(parent2[gene])
    for gene in range(len(parent1)):
        if offspring1.count(parent2[gene]) == 0:
            offspring1.append(parent2[gene])
        if offspring2.count(parent1[gene]) == 0:
            offspring2.append(parent1[gene])
    return offspring1, offspring2


def uniform_crossover(parent1: list, parent2: list):
    offspring1, offspring2 = [], []
    binary_string = []
    for _ in range(len(parent1)):
        binary_string.append(rnd.randint(0, 1))
    for bit in binary_string:
        if bit == 1:
            for gene in parent1:
                if gene not in offspring1:
                    offspring1.append(gene)
                    break
            for gene in parent2:
                if gene not in offspring2:
                    offspring2.append(gene)
                    break
        if bit == 0:
            for gene in parent2:
                if gene not in offspring1:
                    offspring1.append(gene)
                    break
            for gene in parent1:
                if gene not in offspring2:
                    offspring2.append(gene)
                    break
    return offspring1, offspring2


def select(sel_type: str, pop: list):
    if sel_type == 'tournament':
        return tournament_selection(pop)
    else:
        return roulette_selection(pop)


def tournament_selection(pop: list):
    parents_amount = len(pop) // 2
    parents_size = 2
    last_gene = len(pop) - 1
    pool = []
    for _ in range(parents_amount):
        parents = []
        for _ in range(parents_size):
            individual1 = rnd.randint(0, last_gene)
            individual2 = rnd.randint(0, last_gene)
            if pop[individual1][2] <= pop[individual2][2]:
                parents.append(pop[individual1][1])
            else:
                parents.append(pop[individual2][1])
        pool.append(tuple(parents))
    return pool


def roulette_selection(pop: list):
    inverse_fitness = []
    dec_place = 4
    for individual in pop:
        inverse_fitness.append(round(1 / individual[2], dec_place))
    temp_sum = 0
    scopes = []
    counter = 0
    for val in inverse_fitness:
        scopes.append((round(temp_sum, dec_place),
                       round(temp_sum + val, dec_place), counter))
        temp_sum += val
        counter += 1
    parents_amount = len(pop) // 2
    pool = []
    for _ in range(parents_amount):
        upper_bound = temp_sum - 0.001
        val1 = round(rnd.uniform(0, upper_bound), dec_place)
        val2 = round(rnd.uniform(0, upper_bound), dec_place)
        for scope in scopes:
            if scope[0] <= val1 < scope[1]:
                parent1 = pop[scope[2]][1]
            if scope[0] <= val2 < scope[1]:
                parent2 = pop[scope[2]][1]
        pool.append((parent1, parent2))
    return pool


def calculate_fitness(genotype: list, rcpsp: list, resource_capacity: int):
    phenotype, fitness = serial_SGS_for_activity_lists(
        genotype, rcpsp, resource_capacity)
    return phenotype, genotype, fitness


def mutate(mutation_prob: float, not_mutated_genotype: list, rcpsp: list):
    mutated_genotype = not_mutated_genotype.copy()
    last_gene = len(mutated_genotype) - 1
    for gene in range(1, last_gene - 1):
        gene_mutate_prob = round(rnd.uniform(0, 1), 2)
        if gene_mutate_prob <= mutation_prob:
            next_gene = gene + 1
            temp_allele = mutated_genotype[gene]
            mutated_genotype[gene] = mutated_genotype[next_gene]
            mutated_genotype[next_gene] = temp_allele
    if check_predecessor_constraints(mutated_genotype, rcpsp):
        return mutated_genotype
    return not_mutated_genotype


def check_predecessor_constraints(mutated_genotype: list, rcpsp: list):
    temp = [mutated_genotype[0]]
    for gene in mutated_genotype[1:len(mutated_genotype)]:
        temp.append(gene)
        for pred in rcpsp[gene][2]:
            if pred not in temp:
                return False
    return True


def replace(offspring_pop: list, parents_pop: list, elites_amount: int):
    offspring_pop_size = len(offspring_pop)
    best_offsprings_amount = offspring_pop_size - elites_amount
    sorted_parents_pop = sorted(parents_pop, key=lambda x: x[2])
    sorted_offspring_pop = sorted(offspring_pop, key=lambda x: x[2])
    new_parents_pop = []
    elites = sorted_parents_pop[0:elites_amount]
    new_parents_pop += elites
    best_offsprings = sorted_offspring_pop[0:best_offsprings_amount]
    new_parents_pop += best_offsprings
    new_parents_pop = sorted(new_parents_pop, key=lambda x: x[2])
    return new_parents_pop
