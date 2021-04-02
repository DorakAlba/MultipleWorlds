from constants import RANDOM, SIMULATION

class Field:
    def __init__(self, width: int, height: int):
        """
        Generate battlefield for game
        :param width: of future field
        :param height: of future field
        """
        self.battle_field = [[0 for x in range(width)] for y in range(height)]

    def place_exist(self, line: int, column: int):
        """
        Check if such coordinate exists
        :param line: oX of squares
        :param column: oY of squares
        :return: True if it's place exists
        """
        if line < len(self.battle_field):
            if column < len(self.battle_field[line]):
                return True
            else:
                return False
        else:
            return False

    def unoccupied(self, line, column):
        """
        Check if square free free other characters
        :param line:
        :param column:
        :return:
        """
        if self.battle_field[line][column] == 0:
            return True
        else:
            return False

    def show_field(self):
        """
        display current field
        :arg"""
        display = ""
        for line in self.battle_field:
            for value in line:
                if value == 0:
                    display += (f" | {value}")
                else:
                    display += (f" | {value.name[0]}")
            display += " | \n"
        print(display)

    def get_targets(self):
        targets = {}
        for line in range(len(self.battle_field)):
            for column in range(len(self.battle_field[line])):
                objective = self.battle_field[line][column]
                if objective != 0:
                    targets[objective.name] = objective
        return targets
# def move(self, line: int, column: int):
# field = Field(5, 5)
# field.get_targets()
