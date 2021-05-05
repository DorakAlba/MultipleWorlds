import character_management
import actions
import time
import random
import copy
import collections
from battle_field import Field
from additional_functions import display_distance, calculate_range, find_next_actor
from running_simmulations import select_best_action, add_to_counter
from constants import RANDOM, SIMULATION


class Battle:
    def __init__(self, team1: list, team2: list, field, old=False, acting_character: int = 1):
        self.winner = False
        self.show_actions = False
        # self.character1 = character_management.load_character(character_name1)
        # self.character2 = character_management.load_character(character_name2)
        self.characters = {1: [], 2: []}

        for character in team1:
            character.alive = True
            character.team = 1
            self.characters[1].append(character)
        for character in team2:
            character.alive = True
            character.team = 2
            self.characters[2].append(character)

        self.team_sizes = [len(self.characters[1]), len(self.characters[2])]
        self.starting_team_sizes = [len(self.characters[1]), len(self.characters[2])]

        self.battle_order = []
        for t1, t2 in zip(self.characters[1], self.characters[2]):
            self.battle_order.append(t1)
            self.battle_order.append(t2)
        difference = len(self.characters[1]) - len(self.characters[2])
        if abs(difference) > 0:
            if difference > 0:
                self.battle_order.extend(self.characters[1][len(self.characters[2]):])
            else:
                self.battle_order.extend(self.characters[2][len(self.characters[1]):])

        self.count_steps = 0
        self.winner_team = 0  # 1\2 - teams, 0 draw
        self.field = field
        self.battle_field = self.field.battle_field
        for team in self.characters.values():
            for character in team:
                self.place_character(character)
        # todo delete below
        # self.place_character(self.character1)
        # self.place_character(self.character2)

        # move direction and action, later it's just gonna select best action
        self.first_move = ()
        if not SIMULATION:
            self.field.show_field()

    def select_direction(self, line, column):
        """
        Select direction using NumPad, working only if № lines or column constant
        It check if it's exist and unoccupied using other functions
        :param line:
        :param column:
        :return: return [new_line, new_column]
        """
        # todo move this function somewhere else
        selected = False
        option = [number for number in range(0, 10)]  # for simulation
        while not selected:
            new_line = line
            new_column = column
            if not SIMULATION:
                self.field.show_field()
            if not SIMULATION:
                print('select direction: ')
            if not RANDOM:
                direction = int(input('''            7 8 9
            4   6
            1 2 3
                '''))

            else:
                direction = random.choice(option)
            if direction == 0:
                return (line, column)
            if direction == direction in [7, 4, 1]:
                new_column -= 1
            if direction == direction in [9, 6, 3]:
                new_column += 1
            if direction == direction in [7, 8, 9]:
                new_line -= 1
            if direction == direction in [1, 2, 3]:
                new_line += 1
            if new_column >= 0 and new_line >= 0:
                if self.field.place_exist(new_line, new_column):
                    if self.field.unoccupied(new_line, new_column):
                        selected = True
                    else:
                        option.remove(direction)
                else:
                    option.remove(direction)
        return (new_line, new_column)

    def same_direction(self, new_direction, old_direction):
        if new_direction > old_direction:
            return True
        else:
            return False

    def change_position(self, character, new_position):
        """
        updates position inside character and MAPs
        :param character: character that change position (CAN BE OBJECT)
        :param new_position: [line, column] of new location
        """

        self.clear_position(character)
        self.new_position(character, new_position)

    def clear_position(self, character):
        """
        remove character from field
        :param character: character that removed from field
        """
        self.battle_field[character.position[0]][character.position[1]] = 0
        character.position = None

    def new_position(self, character, new_position):
        """

        :param character: character that gonna had new positions (CAN BE OBJECT)
        :param new_position: position [line,column]
        :return:
        """
        character.position = new_position
        self.battle_field[new_position[0]][new_position[1]] = character

    def move(self, character, return_move=False, determined=False, determined_action=None):
        """
        Character select movement, currently one square
        :param character: character that moves
        :return: 
        """
        if not determined:
            if not SIMULATION:
                print(f"{character.name} moving!  -  {character.name[0]}")
            move_direction = self.select_direction(character.position[0], character.position[1])
            if return_move == True:
                # self.first_move.append(move_direction)
                self.first_move = (move_direction)
        else:
            try:
                move_direction = determined_action[0]
            except TypeError as err:
                print(err)
        self.change_position(character, move_direction)
        if not SIMULATION:
            self.field.show_field()

    def place_character(self, character):
        """
        Take character and on place unoccupied square on battlefield
        character.position = [line, column]
        :param character: added character
        :return:
        """
        selected = False
        while not selected:
            line = random.randrange(len(self.battle_field))
            column = random.randrange(len(self.battle_field[line]))
            if self.field.unoccupied(line, column):
                selected = True
                self.battle_field[line][column] = character
                character.position = [line, column]

    def end_battle(self):
        """
        used after winner defined
        :return: True
        """
        self.winner = True

    def find_targets(self, actor):
        enemies = []
        allies = []
        for character in self.battle_order:
            if character.team != actor.team and character.alive is True:
                enemies.append(character)
            if character.team == actor.team and character.name != actor.name and character.alive is True:
                allies.append(character)
        return allies, enemies

    def target_type(self, allies: list, enemies: list, target):
        """
        Identifying type of target ally\enemy
        :param allies:
        :param enemies:
        :param target:
        :return:
        """
        if target in enemies:
            return 'enemy'
        else:
            return 'ally'

    def character_act(self, active_character, save_move=False, determined=False, determined_action=None, target=None):
        """
        Main function for character turn
        :param active_character: currently active character
        #todo remove target and use coordinate
        :param target: of action
        :return:
        """
        self.count_steps += 1
        # searching for targets
        friendly_characters, enemy_characters = self.find_targets(active_character)
        # all targets
        targets = (friendly_characters + enemy_characters)

        if not determined:
            target_type = None
            if not SIMULATION:
                print(f"{active_character.name} selecting action, he has {active_character.chp} HP")
            # select random target
            target_index = random.randint(0, len(targets) - 1)
            target = targets[target_index]
            target_type = self.target_type(friendly_characters, enemy_characters, target)
            # calculate range between target and active character
            range_a = calculate_range(active_character.position, target.position)
            # return action and it's index
            action, attack_index = active_character.select_action(target_type, distance=range_a)
            if save_move:
                self.first_move = (self.first_move, attack_index, target_index)
        # if actions preselected
        else:
            target = targets[determined_action[2]]
            selected_action = determined_action[1]
            action, attack_index = active_character.select_action(attack_index=selected_action)
        if action:
            if action.action_in_range(calculate_range(active_character.position, target.position)):
                action.use_action(target=target, show_action=self.show_actions, dexterity=active_character.dexterity)
            else:
                if not SIMULATION:
                    print(f"{active_character.name} missed! ")
        self.check_dead(target)

    def end_game_display(self):
        None

    # print(self.steps)
    # self.field.show_field()
    # print(f'{self.character1.name} {self.character1.chp} hp  vs {self.character2.name} {self.character2.chp} hp ')

    def display(self):
        print(self.count_steps)
        self.field.show_field()
        for character in self.battle_order:
            print(f"{character.name} has {character.chp}")
        # print(f'{self.character1.name} {self.character1.chp} hp  vs {self.character2.name} {self.character2.chp} hp ')

    def check_dead(self, character):
        if character.chp <= 0:
            team = character.team - 1
            self.team_sizes[team] -= 1
            character.alive = False
            self.clear_position(character)
            # self.battle_order.remove(character)

    def check_winner(self):
        """
        check character's current hp, if <=0, other character won
        :return:
        """

        # if self.character1.chp <= 0 and self.character2.chp <= 0:
        if self.team_sizes[0] == 0 and self.team_sizes[1] == 0:
            if not SIMULATION:
                print("Draw")
            self.winner_team = 0
            return self.end_battle()
        elif self.team_sizes[0] == 0:
            # elif self.character1.chp <= 0:
            if not SIMULATION:
                print("Team 2 Won!")
            self.winner_team = 2
            return self.end_battle()
        elif self.team_sizes[1] == 0:
            # elif self.character2.chp <= 0:
            if not SIMULATION:
                print("Team 1 Won!")
            self.winner_team = 1
            return self.end_battle()

    def battle_active(self, start=0):
        """
        Running turns of active characters one after another.
        Check winner, calling end_game display
        :return:
        """
        while not self.winner:
            for actor_index in range(start, len(self.battle_order)):
                actor = self.battle_order[actor_index]
                if actor.alive:
                    self.move(actor)
                    self.character_act(actor)
                self.check_winner()
            start = 0
        self.end_game_display()

    def character_turn(self, acting, determined=False, determined_action=None):
        """function that take's planned actions and execute them
        :param acting: number of character that acting
        :param determined:
        :param determined_action:
        :return:
        """
        self.last_acting = acting  # save character, that acted last
        if determined_action:
            self.show_actions = True
        actor = self.battle_order[acting]
        self.move(character=actor, return_move=True, determined=determined, determined_action=determined_action)
        self.character_act(active_character=actor, save_move=True, determined=determined,
                           determined_action=determined_action)
        self.show_actions = False
        self.check_winner()


def run_simmulation(iterations: int, team1: list, team2: list, field_size: list):
    start_time = time.time()
    player_count = len(team1) + len(team2)
    winners = {0: 0, 1: 0, 2: 0}  # count total amount of wins
    field = Field(field_size[0], field_size[1])
    simulation = Battle(team1, team2, field)
    turn = 0
    while not simulation.winner:

        first_action_won = collections.Counter()
        first_action_lost = collections.Counter()
        current_actor = turn % player_count  # find current acting character
        next_actor = find_next_actor(current_actor, player_count)
        if simulation.battle_order[current_actor].alive:
            for _ in range(iterations):
                rollout = copy.deepcopy(simulation)  # create copy of simmulation
                rollout.character_turn(current_actor)  # play out turn of active character, saving result
                # todo fix out of index
                rollout.battle_active(next_actor)

                add_to_counter(rollout.winner_team, rollout.battle_order[current_actor].team, first_action_won,
                               first_action_lost,
                               rollout.first_move)  # giving score to next action, depending on end_game condition
                winners[rollout.winner_team] += 1
                # rollout.display()
            best_action = select_best_action(first_action_won, first_action_lost)
            simulation.character_turn(acting=current_actor, determined=True, determined_action=best_action)
            simulation.display()
        turn += 1
    print(turn)

    print("--- %s seconds ---" % (time.time() - start_time))

    # def select_target(self, targets, character=None):
    #     selected = False
    #     while not selected:
    #         if character == None:
    #             selected = input(f"select target {targets.keys():  }")
    #                 if selected in targets, keys


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
goblin1 = character_management.Character("goblin1", 4, 2, 1, 1, wisdom=1, moves=[sword, chain_blade, healing_bottle])
goblin2 = character_management.Character("goblin2", 4, 2, 1, 1, wisdom=1, moves=[sword, chain_blade, healing_bottle])
goblin3 = character_management.Character("goblin3", 4, 2, 1, 1, wisdom=1, moves=[sword, chain_blade, healing_bottle])
knoll1 = character_management.Character("knoll1", 4, 4, 2, 3, wisdom=1, moves=[sword, pike, lick_wound])
knoll2 = character_management.Character("knoll2", 4, 4, 2, 3, wisdom=1, moves=[sword, pike, lick_wound])
### CHARACTERS ###

run_simmulation(30, [goblin1, goblin2, goblin3], [knoll1, knoll2], field_size=[4, 4])
