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


class Healing(Action):
    def __init__(self, name, target, a_range, healing_dice: str, healing_flat: int, type='Heal'):
        Action.__init__(self, name, target, a_range)
        self.type = type
        self.healing_dice = healing_dice
        self.healing_flat = healing_flat

    def heal(self, target, aim=None, show_action=False, wisdom=0):

        healing = sum(dice.roll(self.healing_dice)) + self.healing_flat + wisdom
        target.chp += healing
        if target.chp > target.mhp:
            target.chp = target.mhp
        if not SIMULATION or show_action:
            print(f"You heal {healing} dmg to {target.name}.")

        if not SIMULATION or show_action:
            print(f"{target.name} has {target.chp} hp")


class Attack(Action):
    def __init__(self, name, target, a_range, dmg_dice: str, dmg_flat: int, accuracy: int, type='Attack'):
        Action.__init__(self, name, target, a_range)
        self.type = type
        self.dmg_dice = dmg_dice
        self.dmg_flat = dmg_flat
        self.accuracy = accuracy

    def attack(self, target, aim=None, show_action=False, dexterity=0):
        # roll d20 to hit
        rolled = dice.roll("1d20")[0]
        chance_to_hit = int(((21 - (target.defs - self.accuracy - dexterity)) / 20) * 100)
        if not SIMULATION or show_action:
            print(f"Probability to hit with {self.name} {chance_to_hit}%")
            print(f"defense {target.defs} vs rolled {rolled} + accuracy {self.accuracy}")

        if rolled + self.accuracy + dexterity >= target.defs:
            dmg = sum(dice.roll(self.dmg_dice)) + self.dmg_flat
            target.chp -= dmg
            if not SIMULATION or show_action:
                print(f"You deal {dmg} dmg to {target.name}.")
        else:
            if not SIMULATION or show_action:
                print("You missed")
        if not SIMULATION or show_action:
            print(f"{target.name} has {target.chp} hp")

# chain_blade = Attack('attack', 'you', [2, 3], "4d3", 1, 2)
# sword = Attack('attack', 'you',[1, 1], "2d6", 2, 4)
