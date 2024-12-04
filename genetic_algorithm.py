import random as rnd

rnd.seed(10)

def random_initial_population(pop_size: int , activities: list ):
    tmp_pop_lst = []
    for activity in range(pop_size):
        chromosome = []
        for gene in range(len(activities)):
            chromosome.append(gene)
        tmp_pop_lst.append(chromosome)
    tmp_chrom = []
    pop_lst = []
    for chromosome in tmp_pop_lst:
        # first gene always for the start activity
        tmp_chrom.append(chromosome[0])
        chromosome.remove(chromosome[0])

        rnd.shuffle(chromosome)
        tmp_chrom = tmp_chrom + chromosome
        pop_lst.append(sort_genes(tmp_chrom, activities))
        tmp_chrom = []
    return pop_lst

def sort_genes(tmp_chrom: list, activities: list):
    sorted_chrom = []
    sorted_chrom.append(tmp_chrom[0])
    tmp_chrom.remove(tmp_chrom[0])
    while len(sorted_chrom) != len(activities):
        for gene in tmp_chrom:
            check = True
            for predecessor in activities[gene][2]:
                if predecessor not in sorted_chrom:
                    check = False
            if check:
                sorted_chrom.append(gene)
                tmp_chrom.remove(gene)
    return sorted_chrom


def crossover(kind_of_crossover: str, father: list, mother: list):
    if kind_of_crossover == 'one-point-crossover':
        return one_point_crossover(father, mother)
    else:
        return uniform_crossover(father, mother)



def one_point_crossover(father: list, mother: list):
    child1 = []
    child2 = []

    # adjust the point where crosspoint will be
    crosspoint = rnd.randint(1, len(father) - 1)

    for gen in range(crosspoint):
        child1.append(father[gen])
        child2.append(mother[gen])

    for gen in range(len(father)):
        if child1.count(mother[gen]) == 0:
            child1.append(mother[gen])
        if child2.count(father[gen]) == 0:
            child2.append(father[gen])
    return child1, child2

def uniform_crossover(father: list, mother: list):
    child1 = []
    child2 = []
    uniform = []
    for _ in range(len(father)):
        uniform.append(rnd.randint(0, 1))
    for bit in uniform:
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

def selection(kind_of_selection: str, makespan_with_list: list):
    if kind_of_selection == 'tournament-selection':
        return tournament_selection(makespan_with_list)
    else:
        return roulette_selection(makespan_with_list)

def tournament_selection(makespan_with_list: list):
    length = len(makespan_with_list) - 1
    pool = []
    for k in range((length + 1) // 2):
        a = rnd.randint(0, length)
        b = rnd.randint(0, length)
        first_parent: list
        if makespan_with_list[a][2] <= makespan_with_list[b][2]:
            first_parent = makespan_with_list[a][1]
        else:
            first_parent = makespan_with_list[b][1]
        c = rnd.randint(0, length)
        d = rnd.randint(0, length)
        while makespan_with_list[c][1] != makespan_with_list[d][1] != first_parent:
            c = rnd.randint(0, length)
            d = rnd.randint(0, length)
        second_parent: list
        if makespan_with_list[c][2] <= makespan_with_list[d][2]:
            second_parent = makespan_with_list[c][1]
        else:
            second_parent = makespan_with_list[d][1]
        pool.append((first_parent, second_parent))
    return pool

'''
As like in tournament the same
'''
def roulette_selection(makespan_with_list: list):
    lis2 = []
    maximization_constant = 100
    for item in makespan_with_list:
        lis2.append(maximization_constant - item[2]) #2 because of the makespans
    sum = 0
    tup = []
    cnt = 0
    first_parent: list
    second_parent: list
    for b in lis2:
        tup.append((sum, sum + b, cnt))
        sum += b
        cnt += 1
    pool = []
    for c in range(len(lis2) // 2):
        r = rnd.randint(0, sum - 1)
        r2 = rnd.randint(0, sum - 1)
        for a in tup:
            if a[0] <= r < a[1]:
                # [a[2]] because the chromosome index is calculated above cnt
                first_parent = makespan_with_list[a[2]][1]
            if a[0] <= r2 < a[1]:
                second_parent = makespan_with_list[a[2]][1]
        pool.append((first_parent, second_parent))
    return pool

def serial_SGS_with_activity_lists(g_lst: list, activities: list, rk: int):
    sj: list = [g_lst[0]] # activity number and finish_time
    Fj = [0]
    Fg = {sj[0]: Fj[0]} # finish time for corresponding sj's
    fj = 0
    for j in g_lst[1:len(g_lst)]:
        # duration of j
        pj = activities[j][0]
        # finish time
        fh = []
        At = [] # j E J fj - pij <= t <Fj
        for a in activities[j][2]:
            fh.append(Fg[a])
        EFj = max(fh) + pj
        EFj_as_start = EFj - pj
        t = list([EFj_as_start])
        for x in sorted(Fj):
            if EFj_as_start < x:
                t.append(x)
        for tt in t:
            free_capacity = True # maybe change n to something better like resource....
            if tt == t[len(t) - 1]: # if last possible in t then
                fj = tt + pj
                break
            idx = g_lst.index(j)
            for c in range(tt, (tt + pj)):
                for jj in g_lst[1:idx]:
                    if (Fg[jj] - activities[jj][0]) <= c < Fg[jj]:
                        At.append(jj)
                rkl = 0
                for bb in At:
                    rkl += activities[bb][1]
                capacity = rk - rkl
                rkj = activities[j][1]
                At = []
                if rkj > capacity:
                    free_capacity = False
            if free_capacity:
                fj = tt + pj
                break
        Fj.append(fj)
        sj.append(j)
        Fg.update({j: fj})
    makespan = max(Fj) # it's actually here from all Fj's... not the predecessors of last one
    print(Fg, activities, makespan, "finish_times fg, activities and makespan")
    return Fg, makespan

def calculate_fitness(chromosome: list, activities: list, resource_capacity: int):
    finish_times, makespan = serial_SGS_with_activity_lists(chromosome, activities, resource_capacity)
    return finish_times, chromosome, makespan


def mutate(mutate_rate: float, not_mutated_chrom: list, activity_list: list):
    if mutate_rate == 0:
        return not_mutated_chrom
    mutated_chrom = not_mutated_chrom.copy()
    for act in not_mutated_chrom:
        p = round(rnd.uniform(0, 1), 3)
        if p <= mutate_rate:
            gene1 = not_mutated_chrom.index(act)
            scnd = rnd.randint(0, len(not_mutated_chrom) - 1)
            gene2 = not_mutated_chrom.index(scnd)
            # if its not equal skip while loop
            while gene1 == gene2:
                gene2 = not_mutated_chrom.index(rnd.randint(0, len(not_mutated_chrom) - 1))
            mutated_chrom[gene1] = not_mutated_chrom[gene2]
            mutated_chrom[gene2] = not_mutated_chrom[gene1]
    #If predecessors-condition is true than return mutated_chromosome, else the not mutated chromosome
    if check_precedessors(mutated_chrom, activity_list):
        return mutated_chrom
    return not_mutated_chrom

def check_precedessors(mutate_list: list, activity_list: list):
    temp = []
    temp.append(mutate_list[0])
    if temp[0] != 0:
        return False
    for a in mutate_list:
        temp.append(a)
        for b in activity_list[a][2]:
            if b not in temp:
                return False
    return True

def replace(children_pop: list, makespan_of_parents: list, activities: list, pop: int, rk: int, elitsm_amount: int):
    makespan_of_children = []
    for a in children_pop:
        makespan_of_children.append(calculate_fitness(a, activities, rk))
    child_list = sorted(makespan_of_children, key=lambda x: x[2])
    parents_list = sorted(makespan_of_parents, key=lambda x: x[2])

    makespan_as_parents_list = []

    if elitsm_amount <= pop - len(children_pop):
        elitsm_amount = pop - len(children_pop)

    for c in parents_list:
        makespan_as_parents_list.append(c)
        elitsm_amount -= 1
        if elitsm_amount == 0:
            break

    pop -= elitsm_amount

    for b in child_list:
        makespan_as_parents_list.append(b)
        pop -= 1
        if pop == 0:
            break

    makespan_as_parents_list = sorted(makespan_as_parents_list, key=lambda x: x[2])
    return makespan_as_parents_list   # finish_times, parent_pop, makespan