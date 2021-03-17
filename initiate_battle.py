import character_management
import actions
from battle_field import Field
import random

chain_blade = actions.Attack('chain_blade', 'you', 1, "4d3", 1, 2)
sword = actions.Attack('sword', 'you', 1, "2d6", 2, 4)
pike = actions.Attack('pike', 'you', 1, "1d12", 4, 6)
goblin = character_management.Character("goblin", 20, 4, 15, [sword, chain_blade])
knoll = character_management.Character("knoll", 30, 4, 14, [sword, pike])
field = Field(6, 6)


class Battle:
    def __init__(self, character_name1, character_name2, field):
        self.winner = False
        # self.character1 = character_management.load_character(character_name1)
        # self.character2 = character_management.load_character(character_name2)
        self.character1 = character_name1
        self.character2 = character_name2
        self.field = field
        self.battle_field = self.field.battle_field
        self.place_character(self.character1)
        self.place_character(self.character2)
        self.field.show_field()
        self.battle_active()

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
            print('select direction: ')
            direction = int(input('''            7 8 9
            4   6
            1 2 3
            '''))
            if direction == direction in [7, 4, 1]:
                new_column -= 1
            if direction == direction in [9, 6, 3]:
                new_column += 1
            if direction == direction in [7, 8, 9]:
                new_line -= 1
            if direction == direction in [1, 2, 3]:
                new_line += 1

            if self.field.place_exist(new_line, new_column):
                if self.field.unoccupied(new_line, new_column):
                    selected = True
        return [new_line, new_column]

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
        self.field.display_field[character.position[0]][character.position[1]] = 0
        character.position = None

    def new_position(self, character, new_position):
        """

        :param character: character that gonna had new positions (CAN BE OBJECT)
        :param new_position: position [line,column]
        :return:
        """
        character.position = new_position
        self.battle_field[new_position[0]][new_position[1]] = character
        self.field.display_field[new_position[0]][new_position[1]] = character.name[0]

    def move(self, character):
        """
        Character select movement, currently one square
        :param character: character that moves
        :return: 
        """
        print(f"{character.name} moving!  -  {character.name[0]}")
        move_direction = self.select_direction(character.position[0], character.position[1])
        self.change_position(character, move_direction)
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
                self.field.display_field[line][column] = character.name[0]
                character.position = [line, column]

    def end_battle(self):
        """
        used after winner defined
        :return: True
        """
        self.winner = True

    def character_act(self, active_character, target):
        """
        Main function for character turn
        :param active_character: currently active character
        #todo remove target and use coordinate
        :param target: of action
        :return:
        """
        print(f"{active_character.name} selecting action, he has {active_character.chp} HP")
        action = active_character.select_action()
        return action.attack(target=target)

    def check_winner(self):
        """
        check character's current hp, if <=0, other character won
        :return:
        """
        if self.character1.chp <= 0 and self.character2.chp <= 0:
            print("Draw")
            return self.end_battle()
        elif self.character1.chp <= 0:
            print("Character 2 Won!")
            return self.end_battle()
        elif self.character2.chp <= 0:
            print("Character 1 Won!")
            return self.end_battle()

    def battle_active(self):
        while not self.winner:
            self.move(self.character1)
            self.character_act(self.character1, self.character2)
            self.move(self.character2)
            self.character_act(self.character2, self.character1)
            self.check_winner()


Battle(goblin, knoll, field)
