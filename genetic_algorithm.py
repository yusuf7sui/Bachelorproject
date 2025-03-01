import random as rnd

rnd.seed(10)
import dataset as dt

def random_initial_population(pop_size: int, rcpsp: list):
    tmp_pop = []
    for _ in range(pop_size):
        tmp_genotype = []
        for gene in range(len(rcpsp)):
            tmp_genotype.append(gene)
        tmp_pop.append(tmp_genotype)
    shuffled_genotype = []
    random_population = []
    for tmp_genotype in tmp_pop:
        shuffled_genotype.append(tmp_genotype[0])
        tmp_genotype.remove(tmp_genotype[0])
        rnd.shuffle(tmp_genotype)
        shuffled_genotype = shuffled_genotype + tmp_genotype
        print(shuffled_genotype)
        random_population.append(sort_genes(shuffled_genotype, rcpsp))
        shuffled_genotype = []
    return random_population

def sort_genes(tmp_genotype: list, rcpsp: list):
    sorted_genotype = []
    sorted_genotype.append(tmp_genotype[0])
    tmp_genotype.remove(tmp_genotype[0])
    while len(sorted_genotype) != len(rcpsp):
        for gene in tmp_genotype:
            if sorted_genotype.count(gene) == 1:
                continue
            check = True
            for predecessor in rcpsp[gene][2]:
                if predecessor not in sorted_genotype:
                    check = False
            if check:
                sorted_genotype.append(gene)
    print(sorted_genotype)
    return sorted_genotype

#initial = random_initial_population(2, dt.BASE_RCPSP)

def crossover(kind_of_crossover: str, father: list, mother: list):
    if kind_of_crossover == 'one-point':
        return one_point_crossover(father, mother)
    else:
        return uniform_crossover(father, mother)

def one_point_crossover(father: list, mother: list):
    child1 = []
    child2 = []
    print(father)
    print(mother)

    crosspoint = rnd.randint(1, len(father) - 1)
    print(crosspoint, 'crosspoint included gene 0 as index 1')

    for gene in range(crosspoint):
        child1.append(father[gene])
        child2.append(mother[gene])

    for gene in range(len(father)):
        if child1.count(mother[gene]) == 0:
            child1.append(mother[gene])
        if child2.count(father[gene]) == 0:
            child2.append(father[gene])
    return child1, child2

#test: print(one_point_crossover(initial[0], initial[1]))

def uniform_crossover(father: list, mother: list):
    child1 = []
    child2 = []
    binary_string = []
    for _ in range(len(father)):
        binary_string.append(rnd.randint(0, 1))
    print(father, 'f')
    print(mother, 'm')
    print(binary_string)
    for bit in binary_string:
        if bit == 1:
            for gene in father:
                if gene not in child1:
                    child1.append(gene)
                    break
            for gene in mother:
                if gene not in child2:
                    child2.append(gene)
                    break
        if bit == 0:
            for gene in mother:
                if gene not in child1:
                    child1.append(gene)
                    break
            for gene in father:
                if gene not in child2:
                    child2.append(gene)
                    break
    return child1, child2

#print(uniform_crossover(initial[0], initial[1]))

def selection(kind_of_selection: str, individuals_with_fitness: list):
    if kind_of_selection == 'tournament':
        return tournament_selection(individuals_with_fitness)
    else:
        return roulette_selection(individuals_with_fitness)

def tournament_selection(individuals_with_fitness: list):
    upper_bound = len(individuals_with_fitness) - 1
    pool = []
    all_same = any(individuals_with_fitness[indx][1] == individuals_with_fitness[0][1]
                   for indx in range(len(individuals_with_fitness)))
    for _ in range(len(individuals_with_fitness) // 2):
        parent_pair = []
        #always two times for corresponding paremtpair
        for _ in range(2):
            value1 = rnd.randint(0, upper_bound)
            value2 = rnd.randint(0, upper_bound)
            print('values', value1, value2)
            while parent_pair.count(individuals_with_fitness[value1][1]) == 1 and not all_same:
                value1 = rnd.randint(0, upper_bound)
            while parent_pair.count(individuals_with_fitness[value2][1]) == 1 and not all_same:
                value2 = rnd.randint(0, upper_bound)
            print('valuessafe', value1, value2)
            if individuals_with_fitness[value1][2] <= individuals_with_fitness[value2][2]:
                parent_pair.append(individuals_with_fitness[value1][1])
            else:
                parent_pair.append(individuals_with_fitness[value2][1])
        if parent_pair[0] == parent_pair[1]:
            print('Parents are same')
        pool.append(tuple(parent_pair))
    print(all_same)
    return pool

def roulette_selection(individuals_with_fitness: list):
    inverse_fittness = []
    #print(individuals_with_fitness, 'individuals_with_fitness', )
    INVERSE_VALUE = 100
    for item in individuals_with_fitness:
        inverse_fittness.append(INVERSE_VALUE - item[2]) #2 because of the makespans
    sum = 0
    ranges = []
    counter = 0
    attempts = 5
    parent1: list
    parent2: list
    #print(individuals_with_fitness, ' iiii')
    for value in inverse_fittness:
        ranges.append((sum, sum + value, counter))
        sum += value
        counter += 1
    pool = []
    for _ in range(len(individuals_with_fitness) // 2):
        value1 = rnd.randint(0, sum - 1)
        value2 = rnd.randint(0, sum - 1)
        check = True
        attempt = 0
        while check:
            for element in ranges:
                if element[0] <= value1 < element[1]:
                    parent1 = individuals_with_fitness[element[2]][1]
                if element[0] <= value2 < element[1]:
                    parent2 = individuals_with_fitness[element[2]][1]
            if parent1 != parent2 or attempt == attempts:
                break
            value2 = rnd.randint(0, sum - 1)
            attempt += 1
        pool.append((parent1, parent2))
    if (parent1 == parent2):
        print('Parent are same!')
    return pool

'''
initial = random_initial_population(2, dt.BASE_RCPSP)
pairs = []
cnt = 10
for ind in initial:
    pairs.append(([], ind, cnt))
    cnt += 10
#print(roulette_selection(pairs), 'Roulette_selection_results')
for _ in range(100):
    #print(roulette_selection(pairs), 'Roulette_selection_results')
    print(tournament_selection(pairs), 'tournament_selection_results')
'''

def serial_SGS_with_activity_lists(activity_list: list, rcpsp: list, resource_capacity: int):
    schedule = {activity_list[0]: 0} # finish time for corresponding sj's
    finish_time_of_act = 0
    for act in activity_list[1:len(activity_list)]:
        duration_of_act = rcpsp[act][0]
        # corresponding finish time
        acts_predecessors = []
        active_activities = []
        for pred in rcpsp[act][2]:
            acts_predecessors.append(schedule[pred])
        earliest_finish_time_of_act = max(acts_predecessors) + duration_of_act # eventually just delete this one here
        earliest_start_time_of_act = earliest_finish_time_of_act - duration_of_act
        possible_start_times = list([earliest_start_time_of_act])
        for finish_time in sorted(schedule.values()):
            if earliest_start_time_of_act < finish_time:
                possible_start_times.append(finish_time)
        for time in possible_start_times:
            free_capacity = True
            if time == possible_start_times[len(possible_start_times) - 1]:
                finish_time_of_act = time + duration_of_act
                break
            possible_starts = list(range(time, (time + duration_of_act)))
            time_period = filter(lambda t: t in possible_start_times, possible_starts)
            for time_instant in time_period:
                for already_planned_act in schedule.keys():
                    if ((schedule[already_planned_act] - rcpsp[already_planned_act][0])
                            <= time_instant < schedule[already_planned_act]):
                        active_activities.append(already_planned_act)
                sum_of_resources = 0
                for active_act in active_activities:
                    sum_of_resources += rcpsp[active_act][1]
                free_resources = resource_capacity - sum_of_resources
                needed_resource_of_act = rcpsp[act][1]
                active_activities = []
                if needed_resource_of_act > free_resources:
                    free_capacity = False
            if free_capacity:
                finish_time_of_act = time + duration_of_act
                break
        schedule.update({act: finish_time_of_act})
    makespan = schedule[len(rcpsp) - 1] # instead of sum so lesser resources needed
    print(schedule, activity_list, makespan, "schedule, activity_list and makespan")
    return schedule, makespan

#test_activity_list = [0, 7, 1, 13, 4, 3, 16, 17, 2, 6, 19, 5, 14, 8, 15, 9, 10, 12, 11, 18, 20]
#print(serial_SGS_with_activity_lists(test_activity_list, dt.BASE_RCPSP, dt.RESOURCE_CAPACITY))

def calculate_fitness(genotype: list, rcpsp: list, resource_capacity: int):
    phenotype, fitness = serial_SGS_with_activity_lists(genotype, rcpsp, resource_capacity)
    return phenotype, genotype, fitness

def mutate(mutate_rate: float, not_mutated_genotype: list, rcpsp: list):
    if mutate_rate == 0:
        return not_mutated_genotype
    mutated_genotype = not_mutated_genotype.copy()
    for act in not_mutated_genotype:
        if act == 0 or act == len(mutated_genotype) - 1:
            continue
        p = round(rnd.uniform(0, 1), 3)
        if p <= mutate_rate:
            gene1 = mutated_genotype.index(act)
            # -2 to because last index should not be changeable
            if gene1 + 1 < len(mutated_genotype) - 1:
                gene2 = gene1 + 1
            else:
                gene2 = gene1 - 1
            temp_mem = mutated_genotype[gene1]
            mutated_genotype[gene1] = mutated_genotype[gene2]
            mutated_genotype[gene2] = temp_mem
    print(mutated_genotype, 'Mutated_genotype')
    print(not_mutated_genotype, 'non_mutated_genotype')
    print(check_precedessors(mutated_genotype, rcpsp), 'predecessors check')
    if check_precedessors(mutated_genotype, rcpsp):
        if not_mutated_genotype != mutated_genotype:
            print('Successfully_mutation!')
        else:
            print('Mutation same as ')
        return mutated_genotype
    print('No mutation')
    return not_mutated_genotype

def check_precedessors(mutate_list: list, rcpsp: list):
    temp = []
    temp.append(mutate_list[0])
    if temp[0] != 0:
        return False
    for gene in mutate_list:
        temp.append(gene)
        for pred in rcpsp[gene][2]:
            if pred not in temp:
                return False
    return True

'''
test_activity_list = [0, 7, 1, 13, 4, 3, 16, 17, 2, 6, 19, 5, 14, 8, 15, 9, 10, 12, 11, 18, 20]
for _ in range(20):
    test_result = mutate(0.1, test_activity_list, dt.BASE_RCPSP)
    print(test_result)
    print('')
'''

def replace(children_pop: list, parents_with_fitness: list, rcpsp: list, pop_size: int, resource_cap: int, elitism_amount: int):
    childrens_pop_size = len(children_pop)
    children_with_fitness = []
    for genotype in children_pop:
        children_with_fitness.append(calculate_fitness(genotype, rcpsp, resource_cap))
    child_list = sorted(children_with_fitness, key=lambda x: x[2])
    parents_list = sorted(parents_with_fitness, key=lambda x: x[2])
    print(elitism_amount, 'elitism before')
    new_population = []

    print(elitism_amount, 'elitism amount and needed minimum:', pop_size - childrens_pop_size)
    if elitism_amount < pop_size - childrens_pop_size:
        elitism_amount = pop_size - childrens_pop_size

    print(elitism_amount, 'elitism afterwards')
    pop_size -= elitism_amount

    for individual_with_fitness in parents_list:
        new_population.append(individual_with_fitness)
        elitism_amount -= 1
        if elitism_amount == 0:
            break

    print('Pop size: ', pop_size)

    for individual_with_fitness in child_list:
        new_population.append(individual_with_fitness)
        pop_size -= 1
        if pop_size == 0:
            break

    print('Pop after: ', len(new_population))
    individuals_with_fitness = sorted(new_population, key=lambda x: x[2])
    return individuals_with_fitness