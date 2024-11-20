def crossover(kind_of_crossover: str):
    if kind_of_crossover == 'one_point':
        one_point_crossover()
    else:
        uniform_crossover()

def one_point_crossover():
    pass

def uniform_crossover():
    pass

def selecttion(kind_of_selection: str):
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