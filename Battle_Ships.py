import tkinter as tk
import random
import string

FIELD_SIZE = 10
CELL = 35
LETTERS = string.ascii_uppercase[:FIELD_SIZE]

SHIPS_INFO = [
    ("Aircraft Carrier", 5),
    ("Battleship", 4),
    ("Cruiser", 3),
    ("Submarine", 3),
    ("Destroyer", 2),
]


def create_empty_field():
    return [["." for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)]


def can_place_ship(field, row, col, length, direction):
    cells = []
    for i in range(length):
        r = row + (i if direction == "V" else 0)
        c = col + (i if direction == "H" else 0)

        if r >= FIELD_SIZE or c >= FIELD_SIZE:
            return None
        if field[r][c] != ".":
            return None

        cells.append((r, c))
    return cells


def place_ship(field, ships, name, row, col, length, direction):
    cells = can_place_ship(field, row, col, length, direction)
    if not cells:
        return False

    for r, c in cells:
        field[r][c] = "S"

    ships.append({
        "name": name,
        "cells": cells,
        "hits": set()
    })
    return True


def shoot(field, ships, row, col):
    if field[row][col] in ["O", "H", "X"]:
        return "repeat", None

    for ship in ships:
        if (row, col) in ship["cells"]:
            ship["hits"].add((row, col))
            field[row][col] = "H"

            if len(ship["hits"]) == len(ship["cells"]):
                for r, c in ship["cells"]:
                    field[r][c] = "X"
                ships.remove(ship)
                return "destroyed", ship["name"]

            return "hit", ship["name"]

    field[row][col] = "O"
    return "miss", None


class GameUI:
    def __init__(self, root):
        self.root = root
        root.title("Battleship")
        root.configure(bg="#0f172a")

        self.player_msg = tk.Label(root, fg="#38bdf8", bg="#0f172a",
                                   font=("Arial", 11), wraplength=700, justify="left")
        self.player_msg.pack(pady=4)

        self.computer_msg = tk.Label(root, fg="#f87171", bg="#0f172a",
                                     font=("Arial", 11), wraplength=700, justify="left")
        self.computer_msg.pack(pady=4)

        boards = tk.Frame(root, bg="#0f172a")
        boards.pack()

        self.player_canvas = tk.Canvas(boards, width=420, height=420,
                                       bg="#0f172a", highlightthickness=0)
        self.player_canvas.grid(row=0, column=0, padx=20)

        self.enemy_canvas = tk.Canvas(boards, width=420, height=420,
                                      bg="#0f172a", highlightthickness=0)
        self.enemy_canvas.grid(row=0, column=1, padx=20)

        self.restart_btn = tk.Button(root, text="Restart Battle",
                                     command=self.reset_game)
        self.restart_btn.pack(pady=10)

        self.player_canvas.bind("<Button-1>", self.place_horizontal)
        self.player_canvas.bind("<Button-3>", self.place_vertical)
        self.enemy_canvas.bind("<Button-1>", self.player_shoot)

        self.reset_game()

    def reset_game(self):
        self.player_field = create_empty_field()
        self.enemy_field = create_empty_field()

        self.player_ships = []
        self.enemy_ships = []

        self.phase = "placement"
        self.ship_index = 0

        self.place_enemy_ships()
        self.update_player_message()
        self.update_computer_message("")
        self.draw_boards()

    def place_enemy_ships(self):
        for name, length in SHIPS_INFO:
            while True:
                r = random.randint(0, FIELD_SIZE - 1)
                c = random.randint(0, FIELD_SIZE - 1)
                direction = random.choice(["H", "V"])
                if place_ship(self.enemy_field, self.enemy_ships,
                              name, r, c, length, direction):
                    break

    def draw_board(self, canvas, field, hide=False):
        canvas.delete("all")

        for i in range(FIELD_SIZE):
            canvas.create_text((i + 1.5) * CELL, CELL / 2,
                               text=LETTERS[i], fill="gray")
            canvas.create_text(CELL / 2, (i + 1.5) * CELL,
                               text=str(i), fill="gray")

        for r in range(FIELD_SIZE):
            for c in range(FIELD_SIZE):
                x1 = (c + 1) * CELL
                y1 = (r + 1) * CELL
                x2 = x1 + CELL
                y2 = y1 + CELL

                cell = field[r][c]
                if hide and cell == "S":
                    cell = "."

                colors = {
                    ".": "#1e293b",
                    "S": "#1d4ed8",
                    "H": "#f59e0b",
                    "X": "#b91c1c",
                    "O": "#334155",
                }

                canvas.create_rectangle(x1, y1, x2, y2,
                                        fill=colors[cell],
                                        outline="#0ea5e9")

    def draw_boards(self):
        self.draw_board(self.player_canvas, self.player_field)
        self.draw_board(self.enemy_canvas, self.enemy_field, hide=True)

    def get_cell(self, event):
        col = event.x // CELL - 1
        row = event.y // CELL - 1
        if 0 <= row < FIELD_SIZE and 0 <= col < FIELD_SIZE:
            return row, col
        return None

    def update_player_message(self, text=None):
        if text:
            self.player_msg.config(text=f"Player: {text}")
        else:
            if self.phase == "placement":
                name, length = SHIPS_INFO[self.ship_index]
                self.player_msg.config(
                    text=f"Player: Deploy {name} ({length} cells). "
                         f"Left click = Horizontal, Right click = Vertical."
                )
            elif self.phase == "battle":
                self.player_msg.config(
                    text="Player: Your turn, Admiral. Try to look competent."
                )

    def update_computer_message(self, text):
        self.computer_msg.config(text=f"Computer: {text}")

    def place_ship_ui(self, event, direction):
        if self.phase != "placement":
            return

        cell = self.get_cell(event)
        if not cell:
            return

        r, c = cell
        name, length = SHIPS_INFO[self.ship_index]

        if place_ship(self.player_field, self.player_ships,
                      name, r, c, length, direction):
            self.ship_index += 1
            if self.ship_index == len(SHIPS_INFO):
                self.phase = "battle"
                self.update_player_message(
                    "All ships deployed. The sea awaits poor decisions."
                )
            else:
                self.update_player_message()
        else:
            self.update_player_message(
                "That placement makes no sense. Even the ocean disagrees."
            )

        self.draw_boards()

    def place_horizontal(self, event):
        self.place_ship_ui(event, "H")

    def place_vertical(self, event):
        self.place_ship_ui(event, "V")

    def player_shoot(self, event):
        if self.phase != "battle":
            return

        cell = self.get_cell(event)
        if not cell:
            return

        r, c = cell
        result, ship = shoot(self.enemy_field, self.enemy_ships, r, c)

        if result == "repeat":
            self.update_player_message(
                "You already fired there. Memory is optional, apparently."
            )
            return

        if result == "hit":
            self.update_player_message(
                f"Direct hit on {ship}!"
            )
        elif result == "destroyed":
            self.update_player_message(
                f"You destroyed the {ship}. Insurance refuses comment."
            )
        else:
            self.update_player_message(
                "You hit water. The ocean remains undefeated."
            )

        self.draw_boards()

        if not self.enemy_ships:
            self.update_player_message(
                "Victory! You may now pretend this was skill."
            )
            self.phase = "over"
            return

        self.root.after(600, self.computer_turn)

    def computer_turn(self):
        while True:
            r = random.randint(0, FIELD_SIZE - 1)
            c = random.randint(0, FIELD_SIZE - 1)
            result, ship = shoot(self.player_field, self.player_ships, r, c)
            if result != "repeat":
                break

        if result == "hit":
            msg = f"Computer hit your {ship}. Mild panic onboard."
        elif result == "destroyed":
            msg = f"Computer destroyed your {ship}. Write to the families."
        else:
            msg = "Computer shoots water. Inspirational incompetence."

        self.update_computer_message(msg)
        self.draw_boards()

        if not self.player_ships:
            self.update_player_message(
                "Defeat. The navy politely asks you to never command again."
            )
            self.phase = "over"
        else:
            self.update_player_message()


root = tk.Tk()
GameUI(root)
root.mainloop()
