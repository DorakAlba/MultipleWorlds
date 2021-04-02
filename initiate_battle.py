import character_management
import actions
import time
import random
import copy
import collections
from battle_field import Field
from additional_functions import display_distance, calculate_range
from constants import RANDOM, SIMULATION

chain_blade = actions.Attack('chain blade', 'you', [2, 3], "4d3", 1, 2)
sword = actions.Attack('sword', 'you', [0, 1], "2d6", 2, 4)
pike = actions.Attack('pike', 'you', [0, 2], "1d12", 4, 6)
short_bow = actions.Attack('short bow', 'you', [5, 8], "1d8", 1, -2)


class Battle:
    def __init__(self, character1, character2, field, old=False, acting_character: int = 1):
        self.winner = False
        # self.character1 = character_management.load_character(character_name1)
        # self.character2 = character_management.load_character(character_name2)
        self.character1 = character1
        self.character2 = character2
        self.steps = 0
        self.winner_t = 0
        self.field = field
        self.battle_field = self.field.battle_field
        self.place_character(self.character1)
        self.place_character(self.character2)
        # move direction and action, later it's just gonna best best action
        self.first_move = ()
        if not SIMULATION:
            self.field.show_field()

    def run_simulation(self, will_act=1):
        self.battle_active(will_act)

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
                direction = random.randint(1, 9)
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

    def move(self, character, return_move=False, determined=False, determind_action=None):
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
            move_direction = determind_action[0]
        self.change_position(character, move_direction)
        if not SIMULATION:
            self.field.show_field()

    def place_character(self, character):
        """
        Take character and place unoccupied square on battlefield
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

    def character_act(self, active_character, target, save_move=False, determined=False, determind_action=None):
        """
        Main function for character turn
        :param active_character: currently active character
        #todo remove target and use coordinate
        :param target: of action
        :return:
        """
        self.steps += 1
        if not determined:
            if not SIMULATION:
                print(f"{active_character.name} selecting action, he has {active_character.chp} HP")
            range = calculate_range(active_character.position, target.position)
            action = active_character.select_action(range)
            if save_move:
                self.first_move = (self.first_move, action)
        else:
            action = determind_action[1]
        if action:
            if action.action_in_range(calculate_range(active_character.position, target.position)):
                action.attack(target=target)
            else:
                if not SIMULATION:
                    print(f"{active_character.name} missed! ")

    def end_game_display(self):
        # print(self.steps)
        # self.field.show_field()
        print(f'{self.character1.name} {self.character1.chp} hp  vs {self.character2.name} {self.character2.chp} hp ')

    def check_winner(self):
        """
        check character's current hp, if <=0, other character won
        :return:
        """
        if self.character1.chp <= 0 and self.character2.chp <= 0:
            print("Draw")
            self.winner_t = 0
            return self.end_battle()
        elif self.character1.chp <= 0:
            print("Character 2 Won!")
            self.winner_t = 2
            return self.end_battle()
        elif self.character2.chp <= 0:
            print("Character 1 Won!")
            self.winner_t = 1
            return self.end_battle()

    def battle_active(self, start=1):
        """
        Running turns of active characters one after another
        :return:
        """
        if start == 2:
            self.move(self.character2)
            self.character_act(self.character2, self.character1)
        while not self.winner:
            self.move(self.character1)
            # targets = self.field.get_targets()
            # display_distance(self.character1, targets)
            self.character_act(self.character1, self.character2)

            self.move(self.character2)
            self.character_act(self.character2, self.character1)
            self.check_winner()
        self.end_game_display()

    def character_turn(self, acting, determined=False, determined_action=None):
        self.last_acting = acting
        if acting == 1:
            actor = self.character1
            target = self.character2
        else:
            actor = self.character2
            target = self.character1
        self.move(actor, True, determined, determined_action)
        self.character_act(actor, target, True, determined, determined_action)
        self.check_winner()

    # def select_target(self, targets, character=None):
    #     selected = False
    #     while not selected:
    #         if character == None:
    #             selected = input(f"select target {targets.keys():  }")
    #                 if selected in targets, keys


def run_simmulation(iterations):
    start_time = time.time()
    player_count = 2
    winners = {0: 0, 1: 0, 2: 0}
    goblin = character_management.Character("goblin", 20, 4, 15, [sword, chain_blade, short_bow])
    knoll = character_management.Character("knoll", 30, 4, 14, [sword, pike])
    field = Field(6, 6)
    simulation = Battle(goblin, knoll, field)
    turn = 0
    while not simulation.winner:

        first_action_won = collections.Counter()
        first_action_lost = collections.Counter()
        for _ in range(iterations):
            rollout = copy.deepcopy(simulation)
            if turn % 2 == 0:
                active_character = 1
            else:
                active_character = 2
            if active_character == player_count:
                next_character = 1
            else:
                next_character = active_character + 1
            rollout.character_turn(active_character)
            rollout.battle_active(next_character)

            add_to_counter(rollout.winner_t, active_character, first_action_won, first_action_lost, rollout.first_move)
            winners[rollout.winner_t] += 1
        select_best_action (first_action_won, first_action_lost)
        if turn % 2 == 0:
            simulation.character_turn(1, True, first_action_won[0])
        else:
            simulation.character_turn(2, True, first_action_won[0])
        turn += 1
    print(turn)

    print("--- %s seconds ---" % (time.time() - start_time))

def select_best_action (first_action_won, first_action_lost):


def add_to_counter(winner_t, active_character, first_action_won, first_action_lost, first_move):
    if winner_t == active_character:
        first_action_won[first_move] += 1
    else:
        first_action_lost[first_move] += 1


run_simmulation(10)
