import random as rd


class CharacterStats:
    def __init__(self, agility: int = 1, vitality: int = 1, dexterity: int = 1, strength: int = 1,
                 wisdom: int = 1,
                 intellect: int = 1, total_stats=13):
        self.total_stats = total_stats
        self.agility = agility
        self.vitality = vitality
        self.dexterity = dexterity
        self.strength = strength
        self.wisdom = wisdom
        self.intellect = intellect
        self.stat_names = {'agility': agility, 'vitality': vitality, 'dexterity': dexterity, 'strength': strength,
                           'wisdom': wisdom, 'intellect': intellect}
        self.calc_allocated_stats()
        self.randomly_distribute_stats()

    def select_random_stat(self):
        random_stat = rd.choice(list(self.stat_names))
        return random_stat

    def change_random_stat(self, increase=True):
        stat_to_raise = self.select_random_stat()
        if increase is True:
            self.stat_names[stat_to_raise] += 1
        else:
            self.stat_names[stat_to_raise] -= 1
        self.calc_allocated_stats()

    def randomly_distribute_stats(self):
        while self.free_stats > 0:
            self.change_random_stat(increase=True)
        while self.free_stats < 0:
            self.change_random_stat(increase=False)

    def calc_allocated_stats(self):
        self.free_stats = self.total_stats - self.calc_stat_sum()

    def calc_stat_sum(self):
        stat_sum = 0
        for key in self.stat_names:
            stat_sum += self.stat_names[key]
        return stat_sum

    def display_stats(self):
        """
        displaying all stats of character
        :return:
        """
        print(self.total_stats,
              self.agility,
              self.vitality,
              self.dexterity,
              self.strength,
              self.wisdom,
              self.intellect, )


stats = CharacterStats()
print(stats.stat_names)
stats.randomly_distribute_stats()
print(stats.stat_names)

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
