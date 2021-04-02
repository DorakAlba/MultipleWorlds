import random


def initiate_stats(total_stats: int):
    total = total_stats
    strength = 1
    dexterity = 1
    vitality = 1
    agility = 1

    stats = [strength, dexterity, vitality, agility]
    for g in range(total):
        stats[random.randint(0, len(stats) - 1)] += 1
    return stats


def initiate_population(number: int, total_stats: int):
    population = []
    for species in range(number):
        population.append(initiate_stats(total_stats))
    return population


def mutate_stats(character_stats, probability=0.25):
    if random.random() < probability:
        character_stats[random.randint] += 1
        character_stats[random.randint] -= 1
    return character_stats


def crossover(a, b):
    if random.random() <= 0.5:
        a, b = b, a
    child = []
    place_of_cut = len(a) // 2
    new_a = a[0:place_of_cut].copy()
    new_a_tail = a[place_of_cut:].copy()
    new_b = b[place_of_cut:].copy()
    mapping = {new_b[i]: new_a_tail[i] for i in range(len(new_a_tail))}
    for a1 in range(len(new_a)):
        while new_a[a1] in new_b:
            new_a[a1] = mapping[new_a[a1]]

    # Here we gonna fix repetition of genes
    # child.extend(new_a)
    # child.extend(new_b)
    print(new_a)
    print(new_a)
    child = new_a + new_b
    # breeding for our solutions
    return child


def crossover(a, b):
    perfect_child
    for parameter in range(len(a))



    population = initiate_population(4, 5)
print(population)
child = crossover(population[0], population[1])
print(child)
