import random as rnd

rnd.seed(10)
import  dataset as dt
#Initilize population with permutation based codes
def random_initial_population(pop_size: int, activities: list):
    tmp_pop = []
    for _ in range(pop_size):
        tmp_genotype = []
        for gene in range(len(activities)):
            tmp_genotype.append(gene)
        tmp_pop.append(tmp_genotype)
    shuffled_genotype = []
    random_population = []
    for tmp_genotype in tmp_pop:
        # first gene always for the start activity
        shuffled_genotype.append(tmp_genotype[0])
        # so we delete first element every single chrom
        tmp_genotype.remove(tmp_genotype[0])
        rnd.shuffle(tmp_genotype) # mutable
        shuffled_genotype = shuffled_genotype + tmp_genotype
        print(shuffled_genotype)
        random_population.append(sort_genes(shuffled_genotype, activities))
        shuffled_genotype = []
    return random_population

# Maybe sort alleles instead of genes later on
def sort_genes(tmp_genotype: list, activities: list):
    sorted_genotype = []
    sorted_genotype.append(tmp_genotype[0])
    tmp_genotype.remove(tmp_genotype[0])
    while len(sorted_genotype) != len(activities):
        for gene in tmp_genotype:
            # here now instead of remove do it this way to have correct order (because remove in for loop not good)
            if sorted_genotype.count(gene) == 1:
                continue
            check = True
            for predecessor in activities[gene][2]:
                if predecessor not in sorted_genotype:
                    check = False
            if check:
                sorted_genotype.append(gene)
    print(sorted_genotype)
    return sorted_genotype

# test initial = random_initial_population(2, dt.base_data)

def crossover(kind_of_crossover: str, father: list, mother: list):
    if kind_of_crossover == 'one-point-crossover':
        return one_point_crossover(father, mother)
    else:
        return uniform_crossover(father, mother)

def one_point_crossover(father: list, mother: list):
    child1 = []
    child2 = []
    print(father)
    print(mother)

    # adjust the point where crosspoint will be
    crosspoint = rnd.randint(1, len(father) - 1)
    print(crosspoint, 'crossp')

    for gen in range(crosspoint):
        child1.append(father[gen])
        child2.append(mother[gen])

    for gen in range(len(father)):
        if child1.count(mother[gen]) == 0:
            child1.append(mother[gen])
        if child2.count(father[gen]) == 0:
            child2.append(father[gen])
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

#test: print(uniform_crossover(initial[0], initial[1]))

def selection(kind_of_selection: str, individuals_with_fitness: list):
    if kind_of_selection == 'tournament-selection':
        return tournament_selection(individuals_with_fitness)
    else:
        return roulette_selection(individuals_with_fitness)

def tournament_selection(individuals_with_fitness: list):
    size = len(individuals_with_fitness) - 1
    pool = []
    for _ in range((size + 1) // 2):
        parent_pair = []
        #always two times for corresponding paremtpair
        for _ in range(2):
            a = rnd.randint(0, size)
            b = rnd.randint(0, size)
            while parent_pair.count(individuals_with_fitness[a][1]) == 1:
                a = rnd.randint(0, size)
            while parent_pair.count(individuals_with_fitness[b][1]) == 1 or a == b:
                b = rnd.randint(0, size)
            if individuals_with_fitness[a][2] <= individuals_with_fitness[b][2]:
                parent_pair.append(individuals_with_fitness[a][1])
            else:
                parent_pair.append(individuals_with_fitness[b][1])
        pool.append(tuple(parent_pair))
    return pool

def roulette_selection(individuals_with_fitness: list):
    inverse_fittness = []
    print(individuals_with_fitness, 'sss', )
    inverse_const = 100
    for item in individuals_with_fitness:
        inverse_fittness.append(inverse_const - item[2]) #2 because of the makespans
    sum = 0
    tup = [] #maybe other name for variable
    counter = 0
    first_parent: list  # maybe optimize it
    second_parent: list
    for value in inverse_fittness:
        tup.append((sum, sum + value, counter))
        sum += value
        counter += 1
    pool = []
    for _ in range(len(inverse_fittness) // 2):
        r1 = rnd.randint(0, sum - 1)
        r2 = rnd.randint(0, sum - 1)
        while abs(r1 - r2) <= min(inverse_fittness):
            r2 = rnd.randint(0, sum - 1)
        for a in tup:
            if a[0] <= r1 < a[1]:
                # [a[2]] because the genotype index is calculated above cnt
                first_parent = individuals_with_fitness[a[2]][1]
            if a[0] <= r2 < a[1]:
                second_parent = individuals_with_fitness[a[2]][1]
        pool.append((first_parent, second_parent))
    return pool

'''
initial = random_initial_population(4, dataset.base_data)
pairs = []
cnt = 10
for ind in pairs:
    tupelss.append(([], ind, cnt))
    cnt += 10
print(roulette_selection(tupelss), 'Rouelette_selection_results')
print(tournament_selection(tupelss), 'tournament_selection_results')
'''

def serial_SGS_with_activity_lists(activity_list: list, activities: list, resource_capacity: int):
    schedule = {activity_list[0]: 0} # finish time for corresponding sj's
    finish_time_of_act = 0
    for act in activity_list[1:len(activity_list)]:
        duration_of_act = activities[act][0]
        # corresponding finish time
        acts_predecessors = []
        active_activities = []
        for pred in activities[act][2]:
            acts_predecessors.append(schedule[pred])
        earliest_finish_time_of_act = max(acts_predecessors) + duration_of_act
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
                    if ((schedule[already_planned_act] - activities[already_planned_act][0])
                            <= time_instant < schedule[already_planned_act]):
                        active_activities.append(already_planned_act)
                sum_of_resources = 0
                for active_act in active_activities:
                    sum_of_resources += activities[active_act][1]
                free_resources = resource_capacity - sum_of_resources
                needed_resource_of_act = activities[act][1]
                active_activities = []
                if needed_resource_of_act > free_resources:
                    free_capacity = False
            if free_capacity:
                finish_time_of_act = time + duration_of_act
                break
        schedule.update({act: finish_time_of_act})
    makespan = schedule[len(activities) - 1] # instead of sum so lesser resources needed
    print(schedule, activities, makespan, "schedule, activities and makespan")
    return schedule, makespan

test_activity_list = [0, 7, 1, 13, 4, 3, 16, 17, 2, 6, 19, 5, 14, 8, 15, 9, 10, 12, 11, 18, 20]
print(serial_SGS_with_activity_lists(test_activity_list, dt.base_data, dt.RESOURCE_CAPACITY))

def calculate_fitness(genotype: list, activities: list, resource_capacity: int):
    phenotype, fitness = serial_SGS_with_activity_lists(genotype, activities, resource_capacity)
    return phenotype, genotype, fitness

def mutate(mutate_rate: float, not_mutated_genotype: list, activity_list: list):
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
    #If predecessors-condition is true than return mutated_chromosome, else the not mutated chromosome
    print(mutated_genotype, 'Mutated_genotype')
    print(not_mutated_genotype, 'non_mutated_genotype')
    print(check_precedessors(mutated_genotype, activity_list), 'Mutate')
    if check_precedessors(mutated_genotype, activity_list):
        if not_mutated_genotype != mutated_genotype:
            print('Successfully_mutation!')
        return mutated_genotype
    return not_mutated_genotype

def check_precedessors(mutate_list: list, activity_list: list):
    temp = []
    temp.append(mutate_list[0])
    if temp[0] != 0:
        return False
    for gene in mutate_list:
        temp.append(gene)
        for pred in activity_list[gene][2]:
            if pred not in temp:
                return False
    return True

'''
test_activity_list = [0, 7, 1, 13, 4, 3, 16, 17, 2, 6, 19, 5, 14, 8, 15, 9, 10, 12, 11, 18, 20]
for a in range(20):
    b = mutate(0.5, test_schedule, dt.base_data)
    print(b)
    print('')
'''

def replace(children_pop: list, parents_with_fitness: list, activities: list, pop_size: int, resource_cap: int, elitism_amount: int):
    childrens_pop_size = len(children_pop)
    children_with_fitness = []
    for genotype in children_pop:
        children_with_fitness.append(calculate_fitness(genotype, activities, resource_cap))
    child_list = sorted(children_with_fitness, key=lambda x: x[2])
    parents_list = sorted(parents_with_fitness, key=lambda x: x[2])
    print(elitism_amount, 'elitism before')
    new_population = []
    # If elitms amount is to small cause of recombinations didn't happen often,
    # increse eltitsm_amount to have initial population size in next generation
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

    print('Pop size: ', pop_size, elitism_amount)

    for individual_with_fitness in child_list:
        new_population.append(individual_with_fitness)
        pop_size -= 1
        if pop_size == 0:
            break

    print('fitness: ', len(new_population))
    individuals_with_fitness = sorted(new_population, key=lambda x: x[2])
    return individuals_with_fitness   # finish_times, parent_pop, makespan