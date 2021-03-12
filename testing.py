import create_class
import dice
import queue


class Game:
    def __init__(self):
        self.gameOver = False
        self.round = 0

    def newRound(self):
        self.round += 1
        print("\n***   Round: %d   ***\n" % (self.round))

    # Check if either or both Players is below zero health
    def checkWin(self, player, opponent):
        if player.health < 1 and opponent.health > 0:
            self.gameOver = True
            print("You Lose")
        elif opponent.health < 1 and player.health > 0:
            self.gameOver = True
            print("You Win")
        elif player.health < 1 and ai.health < 1:
            self.gameOver = True
            print("*** Draw ***")


class Character:
    def __init__(self, name, arm_class, mhp, chp, m_spd, moves):
        self.name = name
        self.arm_class = arm_class
        self.mhp = mhp
        self.chp = chp
        self.m_spd = m_spd

        self.moves = moves


class Move:
    """
    ml_rng: could be melee, range
    """

    def __init__(self, name: str, ml_rng: str, accuracy: int, reach: int, type: str, dx: str, flat: int):
        self.name = name
        self.ml_rng = ml_rng
        self.accuracy = accuracy
        self.reach = reach
        self.type = type
        self.dx = dice.roll(dx)
        self.flat = flat


scimitar = Move("scimitar", "melee", +4, 1, "chopping", "1d6", 2)
short_now = Move("short_bow", "range", +4, 16, "piercing", "1d6", 2)
goblin = Character("goblin", 15, 7, 7, 6, 'nothing')


def turn_order(characters):


def fight(character1, character2):
