import pickle
import actions
import random
from constants import RANDOM, SIMULATION


class Character:
    def __init__(self, name: str, agility: int, vitality: int, dexterity: int, strength: int, wisdom: int, intellect:int, moves: list):
        self.name = name
        self.agility = agility
        self.intellect = intellect
        self.defs = 10 + self.agility
        self.vitality = vitality
        self.wisdom = wisdom
        self.mhp = 10 + self.vitality * 5
        self.chp = self.mhp
        self.dexterity = dexterity
        self.strength = strength
        self.moves = moves
        self.position = None

    def select_action(self, target_type='enemy', distance=0, attack_index=None):
        selected = False
        move_names = ['wait']
        moves_dict = {}
        for element in self.moves:
            if element.action_in_range(distance) and target_type == element.target:
                move_names.append(element.name)
                moves_dict[element.name] = element
            # if not move_names:
            #     move_names.append('wait')
        while not selected:
            if attack_index is None:
                if not RANDOM:
                    selected_action = int(input(f"select you actions: {move_names} "))
                else:
                    if len(move_names) > 1:
                        selected_action = random.randint(1, len(move_names))
                    else:
                        selected_action = random.randint(0, len(move_names))
            else:
                selected_action = attack_index
            # if selected_action.lower() == "wait":
            if selected_action == 0:
                if not SIMULATION:
                    print(f"{self.name} waiting")
                return None, selected_action
            if selected_action in range(0, len(move_names)):
                move = moves_dict[move_names[selected_action]]
                if not SIMULATION:
                    print(f"{self.name} using {move.name}")
                return move, selected_action


def create_character():
    # while True:
    #     type_of_generation = input("Character generated: randomly or manually? ").lower()
    # if type_of_generation == "randomly" or "manually":
    #     break
    # todo replace, when add randomly
    type_of_generation = "manually"
    if type_of_generation == "manually":
        name = input("Character name? ")
        mhp = input("HP? ")
        atk = input("ATK? ")
        defs = input("DEF? ")
        moves = []

    # new_character = Character(name, mhp, atk, defs, moves)
    # return new_character


def save_character(character):
    save_place = open(f'characters/{character.name}', 'wb')
    pickle.dump(character, save_place)
    save_place.close()


def load_character(character_name):
    """
    return loaded character (class)
    :arg: character name"""
    file = open(f'characters/{character_name}', 'rb')
    character = pickle.load(file)
    file.close()
    return character


# chain_blade = actions.Attack('chain_blade', 'you', 1, "4d3", 1, 2)
# sword = actions.Attack('sword', 'you', 1, "2d6", 2, 4)
# pike = actions.Attack('pike', 'you', 1, "1d12", 4, 6)
#
# goblin = Character("goblin", 4, 2, 1, 1, 1, [sword, chain_blade])
# gnoll = Character("gnoll", 4, 4, 2, 3, [sword, pike])
# save_character(goblin)
# save_character(gnoll)
# gnoll.select_action()
