import random as rd


class Population:
    def __init__(self, population_size=8, total_stats=10):
        #todo possily replace with dictionary and safe best results
        self.population = []
        for creature in range(population_size):
            self.population.append(CharacterStats(total_stats=total_stats))
        self.new_population = []

    def new_generation(self):
        self.population = self.new_population
        self.new_population = []

    def define_pairs(self):
        pass

    def crossover(self, creature1, creature2):
        #todo crossover
        child1.mutate_stats
        child2.mutate_stats
        self.new_population.extend([child1, child2])


class CharacterStats:
    def __init__(self, agility: int = 1, vitality: int = 1, dexterity: int = 1, strength: int = 1,
                 wisdom: int = 1,
                 intellect: int = 1, total_stats=10):
        self.total_stats = total_stats
        self.stat_names = {'agility': agility, 'vitality': vitality, 'dexterity': dexterity, 'strength': strength,
                           'wisdom': wisdom, 'intellect': intellect}
        self.calc_allocated_stats()
        self.randomly_distribute_stats()
        self.score = None

    def select_random_stat(self):
        random_stat = rd.choice(list(self.stat_names))
        return random_stat

    def mutate_stats(self, child, threshold=0.7):
        """increase one stat and decrease other stat, with some threshold"""
        if rd.random() > threshold:
            keys = rd.sample(child.key(), 2)
            child[keys[0]] += 1
            child[keys[1]] -= 1

    def change_random_stat(self, increase=True):
        stat_to_raise = self.select_random_stat()
        if increase is True:
            self.stat_names[stat_to_raise] += 1
        else:
            self.stat_names[stat_to_raise] -= 1
        self.calc_allocated_stats()

    def randomly_distribute_stats(self):
        """distribute excessive free stats, or take away random stats"""
        while self.free_stats > 0:
            self.change_random_stat(increase=True)
        while self.free_stats < 0:
            self.change_random_stat(increase=False)

    def calc_allocated_stats(self):
        self.free_stats = self.total_stats - self.calc_stat_sum()

    def calc_stat_sum(self):
        """Calcukate how many free stats available"""
        stat_sum = 0
        for key in self.stat_names:
            stat_sum += self.stat_names[key]
        return stat_sum

    def display_stats(self):
        """
        displaying all stats of character
        :return:
        """
        print(self.stat_names)


pop = Population(total_stats=100)
for char in pop.population:
    char.display_stats()
#
#     stats = [strength, dexterity, vitality, agility]
#     for g in range(total):
#         stats[random.randint(0, len(stats) - 1)] += 1
#     return stats
#
# def initiate_population(number: int, total_stats: int):
#     population = []
#     for species in range(number):
#         population.append(initiate_stats(total_stats))
#     return population
#
# def mutate_stats(character_stats, probability=0.25):
#     if random.random() < probability:
#         character_stats[random.randint] += 1
#         character_stats[random.randint] -= 1
#     return character_stats
#
# def crossover(a, b):
#     if random.random() <= 0.5:
#         a, b = b, a
#     child = []
#     place_of_cut = len(a) // 2
#     new_a = a[0:place_of_cut].copy()
#     new_a_tail = a[place_of_cut:].copy()
#     new_b = b[place_of_cut:].copy()
#     mapping = {new_b[i]: new_a_tail[i] for i in range(len(new_a_tail))}
#     for a1 in range(len(new_a)):
#         while new_a[a1] in new_b:
#             new_a[a1] = mapping[new_a[a1]]
#
#     # Here we gonna fix repetition of genes
#     # child.extend(new_a)
#     # child.extend(new_b)
#     print(new_a)
#     print(new_a)
#     child = new_a + new_b
#     # breeding for our solutions
#     return child
#
# def crossover(a, b):
#     perfect_child
#     for parameter in range(len(a))
#
#     population = initiate_population(4, 5)
#
# print(population)
# child = crossover(population[0], population[1])
# print(child)
