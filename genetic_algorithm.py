import random as rnd
rnd.seed(10)

def random_initial_population(pop_size: int, rcpsp: list):
    temp_pop = []
    for _ in range(pop_size):
        temp_genotype = []
        for allele in range(len(rcpsp)):
            temp_genotype.append(allele)
        temp_pop.append(temp_genotype)
    shuffled_genotype = []
    random_pop = []
    for temp_genotype in temp_pop:
        shuffled_genotype.append(temp_genotype[0])
        temp_genotype.remove(temp_genotype[0])
        rnd.shuffle(temp_genotype)
        shuffled_genotype = shuffled_genotype + temp_genotype
        random_pop.append(sort_alleles(shuffled_genotype, rcpsp))
        shuffled_genotype = []
    return random_pop

def sort_alleles(temp_genotype: list, rcpsp: list):
    sorted_genotype = []
    sorted_genotype.append(temp_genotype[0])
    temp_genotype.remove(temp_genotype[0])
    while len(sorted_genotype) != len(rcpsp):
        for allele in temp_genotype:
            if sorted_genotype.count(allele) == 1:
                continue
            pred_assigned_before = True
            for pred in rcpsp[allele][2]:
                if pred not in sorted_genotype:
                    pred_assigned_before = False
            if pred_assigned_before:
                sorted_genotype.append(allele)
    return sorted_genotype


def crossover(cross_type: str, parent1: list, parent2: list):
    if cross_type == 'one_point':
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


def selection(sel_type: str, pop: list):
    if sel_type == 'tournament':
        return tournament_selection(pop)
    else:
        return roulette_selection(pop)


def tournament_selection(pop: list):
    parents_amount = len(pop) // 2
    parents_size = 2
    max_attempts = 5
    last_act = len(pop) - 1
    pool = []
    for _ in range(parents_amount):
        parents = []
        attempt = 0
        for _ in range(parents_size):
            individual1 = rnd.randint(0, last_act)
            individual2 = rnd.randint(0, last_act)
            while parents.count(pop[individual1][1]) == 1:
                if attempt == max_attempts:
                    break
                individual1 = rnd.randint(0, last_act)
                attempt += 1
            attempt = 0
            while parents.count(pop[individual2][1]) == 1:
                if attempt == max_attempts:
                    break
                individual2 = rnd.randint(0, last_act)
                attempt += 1
            if pop[individual1][2] <= pop[individual2][2]:
                parents.append(pop[individual1][1])
            else:
                parents.append(pop[individual2][1])
        pool.append(tuple(parents))
    return pool


def roulette_selection(pop: list):
    inverse_fittness = []
    for individual in pop:
        inverse_fittness.append(round(1 / individual[2], 4))
    sum = 0
    scopes = []
    counter = 0
    max_attempts = 5
    for value in inverse_fittness:
        scopes.append((round(sum, 4), round(sum + value, 4), counter))
        sum += value
        counter += 1
    pool = []
    parents_amount = len(pop) // 2
    for _ in range(parents_amount):
        value1 = round(rnd.uniform(0, sum - 0.001), 4)
        value2 = round(rnd.uniform(0, sum - 0.001), 4)
        need_assignments = True
        attempt = 0
        while need_assignments:
            for scope in scopes:
                if scope[0] <= value1 < scope[1]:
                    parent1 = pop[scope[2]][1]
                if scope[0] <= value2 < scope[1]:
                    parent2 = pop[scope[2]][1]
            if parent1 != parent2 or attempt == max_attempts:
                break
            value2 = round(rnd.uniform(0, sum - 1), 4)
            attempt += 1
        pool.append((parent1, parent2))
    return pool


def serial_SGS_for_activity_lists(activity_list: list,
                                  rcpsp: list, resource_capacity: int
                                  ):
    schedule = {activity_list[0]: 0}
    acts_finish_time = 0
    for act in activity_list[1:len(activity_list)]:
        duration_of_act = rcpsp[act][0]
        predecessors_finish_times = []
        considered_acts = []
        for pred in rcpsp[act][2]:
            predecessors_finish_times.append(schedule[pred])
        earliest_start_time = max(predecessors_finish_times)
        possible_start_times = list([earliest_start_time])
        for finish_time in sorted(schedule.values()):
            if earliest_start_time < finish_time:
                possible_start_times.append(finish_time)
        for time in possible_start_times:
            free_capacity = True
            if time == possible_start_times[len(possible_start_times) - 1]:
                acts_finish_time = time + duration_of_act
                break
            time_period = list(range(time, (time + duration_of_act)))
            considered_times = filter(
                lambda t: t in possible_start_times, time_period
            )
            for time_instant in considered_times:
                for planned_act in schedule.keys():
                    if ((schedule[planned_act] - rcpsp[planned_act][0])
                            <= time_instant < schedule[planned_act]):
                        considered_acts.append(planned_act)
                used_resources = 0
                for active_act_at_time_instant in considered_acts:
                    used_resources += rcpsp[active_act_at_time_instant][1]
                free_resources = resource_capacity - used_resources
                acts_resource_needs = rcpsp[act][1]
                considered_acts = []
                if acts_resource_needs > free_resources:
                    free_capacity = False
            if free_capacity:
                acts_finish_time = time + duration_of_act
                break
        schedule.update({act: acts_finish_time})
    last_act = len(rcpsp) - 1
    project_duration = schedule[last_act]
    return schedule, project_duration


def calculate_fitness(genotype: list, rcpsp: list, resource_capacity: int):
    phenotype, fitness = serial_SGS_for_activity_lists(
        genotype, rcpsp, resource_capacity)
    return phenotype, genotype, fitness


def mutation(mutation_prob: float, not_mutated_genotype: list, rcpsp: list):
    if mutation_prob == 0:
        return not_mutated_genotype
    mutated_genotype = not_mutated_genotype.copy()
    last_gene = len(mutated_genotype) - 1
    for allele in not_mutated_genotype:
        if allele == 0 or allele == last_gene:
            continue
        gene_mutate_prob = round(rnd.uniform(0, 1), 2)
        if gene_mutate_prob <= mutation_prob:
            gene = mutated_genotype.index(allele)
            next_gene = gene + 1
            if next_gene < last_gene - 1:
                temp_allele = mutated_genotype[gene]
                mutated_genotype[gene] = mutated_genotype[next_gene]
                mutated_genotype[next_gene] = temp_allele
    if check_predecessor_constraints(mutated_genotype, rcpsp):
        return mutated_genotype
    return not_mutated_genotype


def check_predecessor_constraints(mutated_genotype: list, rcpsp: list):
    temp = []
    temp.append(mutated_genotype[0])
    if temp[0] != 0:
        return False
    for gene in mutated_genotype:
        temp.append(gene)
        for pred in rcpsp[gene][2]:
            if pred not in temp:
                return False
    return True

def replacement(offspring_pop: list, parents_pop: list, elites_amount: int):
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