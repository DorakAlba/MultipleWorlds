class Field:
    def __init__(self, width, height):
        self.field = [[0 for x in range(width)] for y in range(height)]

    def place_exist(self, line, column):
        if line < len(self.field):
            if column < len(self.field[line]):
                return True
            else:
                return False
        else:
            return False
