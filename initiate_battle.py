import character_management
import actions
from battle_field import Field
import random

chain_blade = actions.Attack('chain_blade', 'you', 1, "4d3", 1, 2)
sword = actions.Attack('sword', 'you', 1, "2d6", 2, 4)
pike = actions.Attack('pike', 'you', 1, "1d12", 4, 6)
goblin = character_management.Character("goblin", 20, 4, 15, [sword, chain_blade])
knoll = character_management.Character("knoll", 30, 4, 14, [sword, pike])
field = Field(6, 6).field


class Battle:
    def __init__(self, character_name1, character_name2, field):
        self.winner = False
        # self.character1 = character_management.load_character(character_name1)
        # self.character2 = character_management.load_character(character_name2)
        self.character1 = character_name1
        self.character2 = character_name2
        self.field = field.copy()
        self.display_field = self.field.copy()
        self.place_character(self.character1)
        self.place_character(self.character2)
        self.show_field()
        self.battle_active()

    def select_direction(self, line, column):
        # todo move this function somewhere else
        selected = False
        while not selected:
            new_line = line.copy()
            new_column= column.copy()
            direction = int(input('''7 8 9
                                     4   6
                                     1 2 3'''))
            if direction == direction in [7, 4, 1]:
                new_line -= 1
            if direction == direction in [9, 6, 3]:
                new_line += 1
            if direction == direction in [7, 8, 9]:
                new_column += 1
            if direction == direction in [1, 2, 3]:
                new_column -= 1


            if self.field.place_exist(new_line, new_column):
                if self.unoccupied(new_line, new_column):
                    selected = True

    def show_field(self):
        """
        print current display_field for
        :arg"""
        display = ""
        for line in self.field:
            for value in line:
                if value == 0:
                    display += (f" | {value}")
                else:
                    display += (f" | {value.name[0]}")
            display += " | \n"
        print(display)

    def place_character(self, character):
        selected = False
        while not selected:
            line = random.randrange(len(self.field))
            column = random.randrange(len(self.field[line]))
            if self.unoccupied(line, column):
                selected = True
                self.field[line][column] = character
                # self.display_field[line][column] = character.name[0]
                character.position = [line, column]

    def unoccupied(self, line, column):
        if self.field[line][column] == 0:
            return True
        else:
            return False

    def end_battle(self):
        self.winner = True

    def character_act(self, active_character, target):
        print(f"{active_character.name} selecting action, he has {active_character.chp} HP")
        action = active_character.select_action()
        return action.attack(target=target)

    def check_winner(self, character1, character2):
        if character1.chp <= 0 and character2.chp <= 0:
            print("Draw")
            return self.end_battle()
        elif character1.chp <= 0:
            print("Character 2 Won!")
            return self.end_battle()
        elif character2.chp <= 0:
            print("Character 1 Won!")
            return self.end_battle()

    def battle_active(self):
        while not self.winner:
            self.character_act(self.character1, self.character2)
            self.check_winner(self.character1, self.character2)
            self.character_act(self.character2, self.character1)
            self.check_winner(self.character1, self.character2)




Battle(goblin, knoll, field)
