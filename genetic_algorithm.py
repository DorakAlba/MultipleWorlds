import random as rd


class Population:
    def __init__(self, population_size=8, total_stats=10):
        # todo possily replace with dictionary and safe best results
        self.population = []
        self.total_stats = total_stats
        for creature in range(population_size):
            self.population.append(CharacterStats(total_stats=total_stats))
        self.new_population = []

    def new_generation(self):
        """
        Create new population
        :return:
        """
        self.population = self.new_population
        self.new_population = []

    def define_pairs(self):
        pass

    def crossover(self, creature1, creature2):
        cutting_point = rd.randint(1, len(creature1))

        child1 = creature1.stat_list()[0:cutting_point] + creature2.stat_list()[cutting_point:-1]
        child2 = creature2.stat_list()[0:cutting_point] + creature1.stat_list()[cutting_point:-1]
        child1 = CharacterStats(*child1, total_stats=self.total_stats)
        child2 = CharacterStats(*child2, total_stats=self.total_stats)
        child1.mutate_stats()
        child2.mutate_stats()
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

    def stat_list(self):
        stats = []
        for key in self.stat_names:
            stats.append(self.stat_names[key])
        return stats

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
        """
        Calculate amount of free or borrowed stats
        :return:
        """
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


