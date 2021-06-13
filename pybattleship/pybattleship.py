import random
from TextGrid import TextGrid

WATER = '▓'
SHIP = 'S'
ISLAND = '░'
MAP_COMPONENTS = [WATER, WATER, ISLAND]
HIT = '×'
ASCII_ALPHA_START = 65
WIN = 0
MIN_MAP = 3
MAX_MAP = 8


# Game of battleships against A.I.
def main():
    print("Welcome to pyBattleship.")
    print("Do you think you can beat python at a game of Battleships?")
    map_width = int(
        input("How wide do you want the map? Recommended Between " + str(MIN_MAP) + " and " + str(MAX_MAP) + " : "))
    while map_width < MIN_MAP or map_width > MAX_MAP:
        map_width = int(input("Hold on! That's not between " + str(MIN_MAP) + " and " + str(MAX_MAP) + " : "))
    map_height = int(
        input("How long do you want the map? Recommended Between " + str(MIN_MAP) + " and " + str(MAX_MAP) + " : "))
    while map_height < MIN_MAP or map_height > MAX_MAP:
        map_height = int(input("That's not between " + str(MIN_MAP) + " and " + str(MAX_MAP) + " : "))
    user_ships = int(input("How many ships would you like to start? This determines difficulty. "))
    map_width = map_width + 1
    map_height = map_height + 1
    ai_ships = user_ships
    battle_map_ai = generate_map(map_width, map_height)
    battle_map_user = generate_map(map_width, map_height)
    locate_ships(battle_map_user, user_ships, map_width, map_height)  # locates ships on user's map
    locate_ships(battle_map_ai, ai_ships, map_width, map_height)  # locates ships on AI's map
    hidden_map = mask_map_ai(battle_map_ai, map_width, map_height)  # makes a copy of the map that hides the AI's ships
    map_print(hidden_map, battle_map_user)
    while ai_ships != 0:
        if user_ships == 0:
            break
        ai_ships = user_turn(battle_map_ai, ai_ships)  # user takes turn to destroy an enemy ship
        hidden_map = mask_map_ai(battle_map_ai, map_width, map_height)
        user_ships = computer_turn(battle_map_user, user_ships, map_width,
                                   map_height)  # computer takes turn to destroy one of the user's ships
        map_print(hidden_map, battle_map_user)
    game_end(ai_ships)


def computer_turn(battle_map_user, user_ships, map_width, map_height):
    target_x = random.randint(1, map_width - 1)
    target_y = random.randint(1, map_height - 1)
    cell = battle_map_user.get_cell(target_x, target_y)
    while cell.value == HIT or cell.value == ISLAND:
        target_x = random.randint(1, map_width - 1)
        target_y = random.randint(1, map_height - 1)
        cell = battle_map_user.get_cell(target_x, target_y)
    if cell.value == "S":
        print("Your ship has been HIT!")
        cell.value = HIT
        user_ships -= 1
    else:
        print("Computer took a turn and it missed!")
        cell.value = HIT
    print("Player has " + str(user_ships) + " ships remaining!")
    return user_ships


def game_end(ai_ships):
    print("")
    print("GAME OVER!")
    if ai_ships == 0:
        print("Player wins!")
    else:
        print("Computer wins!")
    print("")


def mask_map_ai(battle_map_ai, map_width, map_height):  # check code doesnt quite work!!!!
    hidden_map = TextGrid.blank(map_width, map_height)
    for x in range(map_width):
        for y in range(map_height):
            cell = battle_map_ai.get_cell(x, y)
            hidden_map.set_cell(x, y, cell)
    for cell in hidden_map:
        if cell.value == SHIP:
            cell.value = WATER
    return hidden_map


def user_turn(battle_map_ai, ai_ships):
    target_x = input("Pick X coordinates (NUMBER) for next target: ")
    target_x = int(target_x)
    target_y = input("Pick Y coordinates (LETTER) for next target: ")
    # need to check for capital letter, if not convert to capital
    target_y = (ord(target_y) - ASCII_ALPHA_START) + 1
    cell = battle_map_ai.get_cell(target_x, target_y)
    if cell.value == "S":
        print("Ship HIT!")
        cell.value = HIT
        ai_ships -= 1
    else:
        print("Miss!")
        cell.value = HIT
    print("Computer has " + str(ai_ships) + " ships remaining!")
    print("")
    return ai_ships


# prints both the user's and the AI's map as well as a legend for clarity
def map_print(hidden_map, battle_map_user):
    print("")
    print("Computer's Map")
    print(hidden_map)
    print("")
    print("Player's Map")
    print(battle_map_user)
    print("")
    print("LEGEND: " + str(WATER) + " Water " + str(ISLAND) + " Island '" + str(SHIP) + "' Ship ")


# takes generated map and puts ships on it
def locate_ships(battle_map_user, user_ships, map_width, map_height):
    for i in range(user_ships):
        ship_x, ship_y = ship_get_x_y(map_width, map_height)
        cell = battle_map_user.get_cell(ship_x, ship_y)
        while cell.value == SHIP or cell.value == ISLAND:
            ship_x, ship_y = ship_get_x_y(map_width, map_height)
            cell = battle_map_user.get_cell(ship_x, ship_y)
        cell.value = SHIP
    return battle_map_user, user_ships


# generate x & y location on map
def ship_get_x_y(map_width, map_height):
    ship_x = random.randint(1, map_width - 1)
    ship_y = random.randint(1, map_height - 1)
    return ship_x, ship_y


# Check for ships
def sunk_ships(battle_map_user):
    for cell in battle_map_user:
        cell = battle_map_user.get_cell(x, y)


# Generate random map
def generate_map(map_width, map_height):
    map_y_coordinate = 1
    map_x_coordinate = ASCII_ALPHA_START
    grid = TextGrid.blank(map_width, map_height)
    for x in range(map_width):
        for y in range(map_height):
            cell = grid.get_cell(x, y)
            if x == 0 and y == 0:
                cell.value = "0"
            elif x == 0:
                cell.value = chr(map_x_coordinate)
                map_x_coordinate += 1
            elif y == 0:
                cell.value = str(map_y_coordinate)
                map_y_coordinate += 1
            else:
                random_value = get_map_value()
                cell.value = random_value
    return grid


def get_map_value():  # randomly selects a map component to add to the map
    idx = random.randint(0, len(MAP_COMPONENTS) - 1)
    return MAP_COMPONENTS[idx]


if __name__ == '__main__':
    main()
