def display_distance(acting_character, targets: list):
    display_text = ""
    for character in targets.values():
        distance = calculate_range(acting_character.position, character.position)
        display_text += (f"{character.name} distance: {distance} ")
    print(display_text)


def calculate_range(position: list, target: list):
    line_distance = abs(position[0] - target[0])
    column_distance = abs(position[1] - target[1])
    distance = 0
    iteration = 0
    while line_distance > 0 and column_distance > 0:
        line_distance -= 1
        column_distance -= 1
        if iteration % 2 == 0:
            distance += 1
        else:
            distance += 2
        iteration += 1
    distance += (column_distance + line_distance)
    return distance

def find_next_actor(current_actor, player_count):
    if current_actor == player_count-1:
        return 0
    else:
        return current_actor+1