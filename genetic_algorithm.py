import random as rd


class Population:
    def __init__(self, population_size=8, total_stats=10):
        # todo possily replace with dictionary and safe best results
        self.population = []
        self.total_stats = total_stats
        self.population_size = population_size
        for creature in range(population_size):
            self.population.append(CharacterStats(total_stats=total_stats))
        self.new_population = []
        self.candidates = {}

    def new_generation(self):
        """
        Create new population
        :return:
        """
        self.population = self.new_population
        self.new_population = []
        self.candidates = {}
        # todo add best candidate from past population and best overall
        # self.new_population.append(best_man_ever.key)
        # if best_man_ever.key != best_man.key:
        # self.new_population.append(best_man.key)

        # self.candidates[best_man_last_year]=1

    def sort_candidates(self):
        """
        Sorting candidates in order they prioritized for selection
        :return:
        """
        self.candidates = {k: v for k, v in sorted(self.candidates.items(), key=lambda item: item[1], reverse=True)}

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

    def choices_no_replacement(self, population, weights, k=1):
        # population = list(population)
        # weights = list(weights)
        result = []
        for n in range(k):
            pos = rd.choices(range(len(population)), weights, k=1)[0]
            result.append(population[pos])
            del population[pos], weights[pos]
        return result

    def stohastic_universal_sampling(self):
        candidates, probability = self.stohastic_scoring()
        # todo define it
        child_needed = self.population_size - 4
        # parents = rd.sample(candidates, child_needed,p=probability)
        future_parents = self.choices_no_replacement(candidates, probability, child_needed)
        return future_parents

    def stohastic_scoring(self):
        score_thresholds = {}
        max = 0
        for candidate, value in self.candidates.items():
            max += value
            score_thresholds[candidate] = value
        for candidate, value in score_thresholds.items():
            score_thresholds[candidate] = value / max
        return list(score_thresholds.keys()), list(score_thresholds.values())


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

    def mutate_stats(self, threshold=0.7):
        """increase one stat and decrease other stat, with some threshold"""
        if rd.random() > threshold:
            keys = rd.sample(self.stat_names, 2)
            self.stat_names[keys[0]] += 1
            self.stat_names[keys[1]] -= 1

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
        """Calculate how many free stats available"""
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


p = Population()
for character in p.population:
    p.candidates[character] = rd.random()
# print(p.candidates.values())
p.sort_candidates()
# print(p.candidates)
print(p.stohastic_universal_sampling())
