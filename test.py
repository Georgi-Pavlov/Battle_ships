import tkinter as tk
import random

FIELD_SIZE = 5
SHIP_HEALTHS = [2, 2, 3, 4, 5]
CELL = 45


def create_empty_field():
    return [["." for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)]


def place_ship(field, ships, row, col, health):
    if field[row][col] == ".":
        field[row][col] = "S"
        ships[(row, col)] = health
        return True
    return False


def shoot(field, ships, row, col):
    if (row, col) in ships:
        ships[(row, col)] -= 1
        if ships[(row, col)] == 0:
            del ships[(row, col)]
            field[row][col] = "X"
            return "destroyed"
        else:
            field[row][col] = "H"
            return "hit"

    if field[row][col] in ["O", "X", "H"]:
        return "repeat"

    field[row][col] = "O"
    return "miss"


class GameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Battleships")
        root.configure(bg="#0f172a")

        self.frame = tk.Frame(root, bg="#0f172a")
        self.frame.pack(pady=10)

        # Message panels
        self.player_msg = tk.Label(root, text="", bg="#0f172a", fg="#38bdf8", font=("Arial", 11), wraplength=500, justify="left")
        self.player_msg.pack(pady=4)

        self.computer_msg = tk.Label(root, text="", bg="#0f172a", fg="#f87171", font=("Arial", 11), wraplength=500, justify="left")
        self.computer_msg.pack(pady=4)

        self.boards = tk.Frame(root, bg="#0f172a")
        self.boards.pack()

        self.player_canvas = tk.Canvas(self.boards, width=300, height=300, bg="#0f172a", highlightthickness=0)
        self.player_canvas.grid(row=0, column=0, padx=20)

        self.enemy_canvas = tk.Canvas(self.boards, width=300, height=300, bg="#0f172a", highlightthickness=0)
        self.enemy_canvas.grid(row=0, column=1, padx=20)

        self.restart_btn = tk.Button(root, text="Restart Battle", command=self.reset_game)
        self.restart_btn.pack(pady=10)

        self.player_canvas.bind("<Button-1>", self.handle_player_click)
        self.enemy_canvas.bind("<Button-1>", self.handle_enemy_click)

        self.reset_game()

    def reset_game(self):
        self.player_field = create_empty_field()
        self.computer_field = create_empty_field()
        self.player_ships = {}
        self.computer_ships = {}
        self.phase = "placement"
        self.current_ship_index = 0

        self.place_computer_ships()
        self.update_player_message()
        self.update_computer_message("")
        self.draw_boards()

    def place_computer_ships(self):
        for hp in SHIP_HEALTHS:
            while True:
                r = random.randint(0, FIELD_SIZE - 1)
                c = random.randint(0, FIELD_SIZE - 1)
                if place_ship(self.computer_field, self.computer_ships, r, c, hp):
                    break

    def draw_board(self, canvas, field, hide_ships=False):
        canvas.delete("all")

        for i in range(FIELD_SIZE):
            canvas.create_text((i + 1.5) * CELL, CELL / 2, text=str(i), fill="gray")
            canvas.create_text(CELL / 2, (i + 1.5) * CELL, text=str(i), fill="gray")

        for r in range(FIELD_SIZE):
            for c in range(FIELD_SIZE):
                x1 = (c + 1) * CELL
                y1 = (r + 1) * CELL
                x2 = x1 + CELL
                y2 = y1 + CELL

                cell = field[r][c]
                if hide_ships and cell == "S":
                    cell = "."

                color = {
                    ".": "#1e293b",
                    "S": "#1d4ed8",
                    "H": "#f59e0b",
                    "X": "#b91c1c",
                    "O": "#334155",
                }[cell]

                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#0ea5e9")

    def draw_boards(self):
        self.draw_board(self.player_canvas, self.player_field)
        self.draw_board(self.enemy_canvas, self.computer_field, hide_ships=True)

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
                hp = SHIP_HEALTHS[self.current_ship_index]
                self.player_msg.config(
                    text=f"Player: Admiral, deploy a ship with {hp} HP. Try not to embarrass the navy."
                )
            elif self.phase == "battle":
                self.player_msg.config(
                    text="Player: Your turn, Admiral. Try to look like you know naval warfare."
                )

    def update_computer_message(self, text):
        self.computer_msg.config(text=f"Computer: {text}")

    def handle_player_click(self, event):
        if self.phase != "placement":
            return

        cell = self.get_cell(event)
        if not cell:
            return

        r, c = cell
        hp = SHIP_HEALTHS[self.current_ship_index]

        if place_ship(self.player_field, self.player_ships, r, c, hp):
            self.current_ship_index += 1
            if self.current_ship_index == len(SHIP_HEALTHS):
                self.phase = "battle"
                self.update_player_message("All ships deployed. The sea awaits poor decisions.")
            else:
                self.update_player_message()
        else:
            self.update_player_message(
                "That position is either occupied or you can't read coordinates. Try again, strategist."
            )

        self.draw_boards()

    def handle_enemy_click(self, event):
        if self.phase != "battle":
            return

        cell = self.get_cell(event)
        if not cell:
            return

        r, c = cell
        result = shoot(self.computer_field, self.computer_ships, r, c)

        if result == "repeat":
            self.update_player_message(
                "You already fired there. Memory issues this early in the battle?"
            )
            return

        if result == "hit":
            self.update_player_message(
                "Direct hit! Somewhere, a sailor just reconsidered his career choices."
            )
        elif result == "destroyed":
            self.update_player_message("Ship obliterated. Insurance claim denied.")
        else:
            self.update_player_message(
                "You hit water. Impressive. The ocean remains undefeated."
            )

        self.draw_boards()

        if not self.computer_ships:
            self.update_player_message(
                "Victory! The enemy retreats. You may now pretend this was skill."
            )
            self.phase = "over"
            return

        self.root.after(600, self.computer_turn)

    def computer_turn(self):
        while True:
            r = random.randint(0, FIELD_SIZE - 1)
            c = random.randint(0, FIELD_SIZE - 1)
            result = shoot(self.player_field, self.player_ships, r, c)
            if result != "repeat":
                break

        if result == "hit":
            msg = "We've been hit! The crew is panicking and someone dropped the coffee."
        elif result == "destroyed":
            msg = "A ship has been lost. Write a heartfelt letter to the families."
        else:
            msg = "Enemy fires blindly and hits nothing. Miraculously relatable."

        self.draw_boards()

        if not self.player_ships:
            self.update_computer_message(msg)
            self.update_player_message(
                "Defeat. The navy politely asks you to never command again."
            )
            self.phase = "over"
        else:
            self.update_computer_message(msg)
            self.update_player_message()

root = tk.Tk()
GameUI(root)
root.mainloop()