import pickle
import actions


class Character:
    def __init__(self, name: str, mhp: int, atk: int, defs: int, moves: list):
        self.name = name
        self.mhp = mhp
        self.chp = mhp
        self.atk = atk
        self.defs = defs
        self.moves = moves
        self.position = None

    def select_action(self):
        selected = False
        # move_names = []
        move_names = ['wait']
        moves_dict = {}
        for element in self.moves:
            move_names.append(element.name)
            moves_dict[element.name] = element
        while not selected:
            selected_action = int(input(f"select you actions: {move_names} "))

            # if selected_action.lower() == "wait":
            if selected_action == 0:
                print(f"{self.name} waiting")
                return None
            if selected_action in range(0, len(move_names)):

                move = moves_dict[move_names[selected_action]]
                print(f"{self.name} using {move.name}")
                return move
                selected = True

            # if selected_action in move_names:
            #     move = moves_dict[selected_action]
            #     return move
            #     selected = True


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

    new_character = Character(name, mhp, atk, defs, moves)
    return new_character


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


chain_blade = actions.Attack('chain_blade', 'you', 1, "4d3", 1, 2)
sword = actions.Attack('sword', 'you', 1, "2d6", 2, 4)
pike = actions.Attack('pike', 'you', 1, "1d12", 4, 6)

goblin = Character("goblin", 20, 4, 15, [sword, chain_blade])
gnoll = Character("gnoll", 30, 4, 14, [sword, pike])
# save_character(goblin)
# save_character(gnoll)
# gnoll.select_action()
