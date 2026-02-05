import random

FIELD_SIZE = 5
SHIP_HEALTHS = [2, 2, 3, 4, 5]


def create_empty_field():
    return [["." for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)]


def print_field(field, hide_ships=False):
    print("  0 1 2 3 4")
    for i, row in enumerate(field):
        print(i, end=" ")
        for cell in row:
            if hide_ships and cell == "S":
                print(".", end=" ")
            else:
                print(cell, end=" ")
        print()


def place_ship(field, ships, row, col, health):
    if field[row][col] == ".":
        field[row][col] = "S"
        ships[(row, col)] = health
        return True
    return False


def player_place_ships(field, ships):
    print("Place your ships (row col)")
    for health in SHIP_HEALTHS:
        while True:
            print_field(field)
            r, c = map(int, input(f"Ship with {health} HP: ").split())
            if 0 <= r < FIELD_SIZE and 0 <= c < FIELD_SIZE:
                if place_ship(field, ships, r, c, health):
                    break
            print("Invalid position, try again.")


def computer_place_ships(field, ships):
    for health in SHIP_HEALTHS:
        while True:
            r = random.randint(0, FIELD_SIZE - 1)
            c = random.randint(0, FIELD_SIZE - 1)
            if place_ship(field, ships, r, c, health):
                break


def shoot(field, ships, row, col):
    # If there's a ship here, apply damage
    if (row, col) in ships:
        ships[(row, col)] -= 1

        if ships[(row, col)] == 0:
            del ships[(row, col)]
            field[row][col] = "X"
            return "destroyed"
        else:
            field[row][col] = "H"
            return "hit"

    # No ship here
    if field[row][col] in ["O", "X"]:
        return "repeat"

    field[row][col] = "O"
    return "miss"


# --- GAME SETUP ---
player_field = create_empty_field()
computer_field = create_empty_field()

player_ships = {}
computer_ships = {}

player_place_ships(player_field, player_ships)
computer_place_ships(computer_field, computer_ships)

# --- GAME LOOP ---
player_turn = True

while player_ships and computer_ships:
    if player_turn:
        print("\nYour turn")
        print_field(computer_field, hide_ships=True)
        r, c = map(int, input("Shoot (row col): ").split())
        result = shoot(computer_field, computer_ships, r, c)

        if result == "hit":
            print("Hit! The ship is damaged but still afloat.")
        elif result == "destroyed":
            print("Ship destroyed!")
        elif result == "miss":
            print("Missed!")
        elif result == "repeat":
            print("You already shot there!")
    else:
        r = random.randint(0, FIELD_SIZE - 1)
        c = random.randint(0, FIELD_SIZE - 1)
        print(f"\nComputer shoots {r} {c}")
        result = shoot(player_field, player_ships, r, c)

        if result == "hit":
            print("Your ship was hit!")
        elif result == "destroyed":
            print("One of your ships was destroyed!")
        elif result == "miss":
            print("Computer missed.")

    player_turn = not player_turn

# --- GAME OVER ---
if player_ships:
    print("\n You win!")
else:
    print("\n Computer wins!")