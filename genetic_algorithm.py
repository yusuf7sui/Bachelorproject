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


def crossover(kind_of_crossover: str):
    if kind_of_crossover == 'one_point':
        one_point_crossover()
    else:
        uniform_crossover()



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

def selection(kind_of_selection: str):
    if kind_of_selection == 'roulette':
        roulette_selection()
    else:
        tournament_selection()

def roulette_selection():
    pass

def tournament_selection():
    pass


def calculate_fitness():
    # call serial_SGS_with_activity_lists() to calculate fitness
    # fitness corresponds the makespan
    pass

def serial_SGS_with_activity_lists():
    pass

def mutate(mutate_rate: float):
    # switch a gene from every chromosome if mutation probability is given

    pass

def replace():
    pass