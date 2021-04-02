import dice
import battle_field
from constants import RANDOM, SIMULATION


class Action:
    def __init__(self, name: str, target: str, a_range: list):
        self.name = name
        # target "you" or "other"
        self.target = target
        # attack range
        self.a_range = a_range

    def action_in_range(self, distance: int):
        """
        :param distance: distance between target and user
        :param action: action
        :return: True/False - suitable range or not
        """
        action_a_range = self.a_range
        if action_a_range[0] <= distance <= action_a_range[1]:
            return True
        else:
            return False


class Attack(Action):
    def __init__(self, name, target, a_range, dmg_dice: str, dmg_flat: int, accuracy: int):
        Action.__init__(self, name, target, a_range)
        self.dmg_dice = dmg_dice
        self.dmg_flat = dmg_flat
        self.accuracy = accuracy

    def attack(self, target, aim=None):
        # roll d20 to hit
        rolled = dice.roll("1d20")[0]
        chance_to_hit = int(((21 - (target.defs - self.accuracy)) / 20) * 100)
        if not SIMULATION:
            print(f"Probability to hit {chance_to_hit}%")
            print(f"{target.defs} vs {rolled} + {self.accuracy}")

        if rolled + self.accuracy >= target.defs:
            dmg = sum(dice.roll(self.dmg_dice)) + self.dmg_flat
            target.chp -= dmg
            if not SIMULATION:
                print(f"You deal {dmg} dmg to {target.name}.")
        else:
            if not SIMULATION:
                print("You missed")
        if not SIMULATION:
            print(f"{target.name} has {target.chp} hp")

# chain_blade = Attack('attack', 'you', [2, 3], "4d3", 1, 2)
# sword = Attack('attack', 'you',[1, 1], "2d6", 2, 4)
