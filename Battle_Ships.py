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
    print("\nAdmiral, the sea awaits your genius. Deploy the fleet (row col). Try not to embarrass the navy.")
    for health in SHIP_HEALTHS:
        while True:
            print_field(field)
            r, c = map(int, input(f"Ship with {health} HP: ").split())
            if 0 <= r < FIELD_SIZE and 0 <= c < FIELD_SIZE:
                if place_ship(field, ships, r, c, health):
                    break
            print("That position is either occupied or you can't read coordinates. Try again, strategist.")


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
    if field[row][col] in ["O", "X", "H"]:
        return "repeat"
    else:
        while True:
            r = random.randint(0, FIELD_SIZE - 1)
            c = random.randint(0, FIELD_SIZE - 1)
            result = shoot(player_field, player_ships, r, c)
            if result != "repeat":
                break

    field[row][col] = "O"
    return "miss"


# --- GAME SETUP ---
while True:
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
            print("\nYour turn, Admiral. Try to look like you know naval warfare.")
            print_field(computer_field, hide_ships=True)
            r, c = map(int, input("Give firing coordinates (row col), and may Neptune forgive you: ").split())
            result = shoot(computer_field, computer_ships, r, c)

            if result == "hit":
                print("Direct hit! Somewhere, a sailor just reconsidered his career choices.")
            elif result == "destroyed":
                print("Ship obliterated.")
            elif result == "miss":
                print("You hit water. Impressive. The ocean remains undefeated.")
            elif result == "repeat":
                print("You already fired there. Memory issues this early in the battle?")
        else:
            r = random.randint(0, FIELD_SIZE - 1)
            c = random.randint(0, FIELD_SIZE - 1)
            print(f"\nEnemy fleet fires at {r} {c}. They look suspiciously more competent.")
            result = shoot(player_field, player_ships, r, c)

            if result == "hit":
                print("We've been hit! The crew is panicking and someone dropped the coffee.")
            elif result == "destroyed":
                print("A ship has been lost. Write a heartfelt letter to the families.")
            elif result == "miss":
                print("Computer missed.")

        player_turn = not player_turn

    # --- GAME OVER ---
    if player_ships:
        print("\nVictory! The enemy retreats. You may now pretend this was skill.")
    else:
        print("\nDefeat. The navy politely asks you to never command again.")

    while True:
        choice = input("Play again? [y / n]: ").lower()

        if choice == "y":
            print("Resetting the battlefield. History will repeat itself.\n")
            break
        elif choice == "n":
            print("Game over. The ocean is closed for today.")
            exit()
        else:
            print("There were exactly two choices. Command may not be your calling.")
