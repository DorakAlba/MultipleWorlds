import actions
import character_management
from additional_functions import find_next_actor
from initiate_battle import Battle
from battle_field import Field
from genetic_algorithm import CharacterStats
from action_evaluation import select_simulation_action
import time
import collections
import copy
import action_evaluation


class Simulation:
    def __init__(self, n_simulations=10, iterations=1000):
        self.n_simulations = n_simulations
        self.iterations = iterations
        self.score = 0

    def simulations(self):
        for _ in range(self.n_simulations):
            self.score += self.run_simulation()
        self.score /= self.n_simulations

    def run_simulation(self, team1: list, team2: list, field_size: list):
        start_time = time.time()
        player_count = len(team1) + len(team2)
        winners = {0: 0, 1: 0, 2: 0}  # count total amount of wins
        field = Field(field_size[0], field_size[1])
        simulation = Battle(team1, team2, field)
        turn = 0
        while not simulation.winner:

            # first_action_won = collections.Counter()
            # first_action_lost = collections.Counter()
            action_scores = {}

            current_actor = turn % player_count  # find current acting character
            next_actor = find_next_actor(current_actor, player_count)
            if simulation.battle_order[current_actor].alive:  # check if character live
                for _ in range(self.iterations):
                    rollout = copy.deepcopy(simulation)  # create copy of simulation
                    rollout.character_turn(acting=current_actor)  # play out turn of active character, saving result
                    rollout.battle_active(next_actor)

                    # action_evaluation.add_to_counter(rollout.winner_team, rollout.battle_order[current_actor].team,
                    #                                  first_action_won,
                    #                                  first_action_lost,
                    #                                  rollout.first_move)  # giving score to next action, depending on end_game condition

                    if rollout.first_move not in action_scores: #move () [Score,Number of simulations]
                        action_scores[rollout.first_move] = [0, 0]
                    action_scores[rollout.first_move][0]+=rollout.score #increase score
                    action_scores[rollout.first_move][1]+=1 #increase amount of simulations

                    winners[rollout.winner_team] += 1
                    # rollout.display()
                selected_acton = action_evaluation.select_simulation_action(action_scores, self.iterations)
                # best_action = action_evaluation.select_best_action(first_action_won, first_action_lost)
                simulation.character_turn(acting=current_actor, determined=True, determined_action=list(selected_acton))
                simulation.display()
                # todo return score
            turn += 1

        print("--- %s seconds ---" % (time.time() - start_time))


### ATTACKS ###
chain_blade = actions.Attack('chain blade', [2, 3], "4d3", 1, 2)
sword = actions.Attack('sword', [0, 1], "2d6", 2, 4)
pike = actions.Attack('pike', [0, 2], "1d12", 4, 6)
short_bow = actions.Attack('short bow', [5, 8], "1d8", 1, -2)
### ATTACKS ###
### ACTIONS ###
lick_wound = actions.Healing('lick wound', a_range=[0, 1], healing_dice="2d4", healing_flat=1)
healing_bottle = actions.Healing('healing bottle', a_range=[2, 5], healing_dice="1d4", healing_flat=0)
### ACTIONS ###


### CHARACTERS ###
goblin1 = character_management.Character("goblin1", agility=4, vitality=2, dexterity=1, strength=1, wisdom=1,
                                         intellect=1,
                                         moves=[chain_blade, short_bow, healing_bottle])
goblin2 = character_management.Character("goblin2", agility=4, vitality=2, dexterity=1, strength=1, wisdom=1,
                                         intellect=1,
                                         moves=[chain_blade, short_bow, healing_bottle])
goblin3 = character_management.Character("goblin3", agility=4, vitality=2, dexterity=1, strength=1, wisdom=1,
                                         intellect=1,
                                         moves=[sword, chain_blade, short_bow, healing_bottle])
knoll1 = character_management.Character("knoll1", agility=4, vitality=4, dexterity=2, strength=3, wisdom=1, intellect=1,
                                        moves=[pike, lick_wound])
knoll2 = character_management.Character("knoll2", agility=4, vitality=4, dexterity=2, strength=3, wisdom=1, intellect=1,
                                        moves=[pike, lick_wound])
knoll_mini = character_management.Character("knollm", agility=1, vitality=2, dexterity=2, strength=1, wisdom=1,
                                            intellect=1,
                                            moves=[pike, lick_wound])
### CHARACTERS ###

### GENETIC ALGORITHM ###

boris_stats = CharacterStats().stat_names
boris = character_management.Character("b", agility=boris_stats['agility'], vitality=boris_stats['vitality'],
                                       dexterity=boris_stats['dexterity'], strength=boris_stats['strength'],
                                       wisdom=boris_stats['wisdom'], intellect=boris_stats['intellect'],
                                       moves=[pike, lick_wound])
### GENETIC ALGORITHM ###


sim = Simulation(10, 100)
sim.run_simulation([goblin1, goblin2, goblin3], [knoll1, knoll_mini], field_size=[3, 3])
