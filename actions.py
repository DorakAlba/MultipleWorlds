import dice


class Action:
    def __init__(self, name: str, target: str, a_range: int):
        self.name = name
        # target "you" or "other"
        self.target = target
        # attack range
        self.a_range = a_range


# class Move (Action):
#     def __init__(self, name, line, column):




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
        print(f"Probability to hit {chance_to_hit}%")
        print(f"{target.defs} vs {rolled} + {self.accuracy}")

        if rolled + self.accuracy >= target.defs:
            dmg = sum(dice.roll(self.dmg_dice)) + self.dmg_flat
            target.chp -= dmg
            print(f"You deal {dmg} dmg to {target.name}.")
        else:
            print("You missed")

        print(f"{target.name} has {target.chp} hp")




# chain_blade = Attack('attack', 'you', 1, "4d3", 1, 2)
# sword = Attack('attack', 'you', 1, "2d6", 2, 4)

