import tkinter as tk

FIELD_SIZE = 5
CELL_SIZE = 50

def create_empty_field():
    return [["." for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)]


class BattleshipsUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Battleships Command Console")
        self.field = create_empty_field()

        self.canvas = tk.Canvas(root,
                                width=(FIELD_SIZE + 1) * CELL_SIZE,
                                height=(FIELD_SIZE + 1) * CELL_SIZE,
                                bg="#0f172a",
                                highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=4, padx=20, pady=20)

        self.draw_grid()

        tk.Label(root, text="X:", fg="white", bg="#0f172a").grid(row=1, column=0)
        self.x_entry = tk.Entry(root, width=5)
        self.x_entry.grid(row=1, column=1)

        tk.Label(root, text="Y:", fg="white", bg="#0f172a").grid(row=1, column=2)
        self.y_entry = tk.Entry(root, width=5)
        self.y_entry.grid(row=1, column=3)

        tk.Button(root, text="Place Ship", command=self.place_ship).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(root, text="Fire", command=self.fire).grid(row=2, column=2, columnspan=2)

        self.message = tk.Label(root, text="Welcome Admiral.", fg="white", bg="#0f172a")
        self.message.grid(row=3, column=0, columnspan=4, pady=10)

        root.configure(bg="#0f172a")

    def draw_grid(self):
        self.canvas.delete("all")

        # Axes
        for i in range(FIELD_SIZE):
            # Top X axis
            self.canvas.create_text((i + 1.5) * CELL_SIZE, CELL_SIZE / 2,
                                    text=str(i), fill="lightgray", font=("Arial", 12))

            # Left Y axis
            self.canvas.create_text(CELL_SIZE / 2, (i + 1.5) * CELL_SIZE,
                                    text=str(i), fill="lightgray", font=("Arial", 12))

        # Cells
        for r in range(FIELD_SIZE):
            for c in range(FIELD_SIZE):
                x1 = (c + 1) * CELL_SIZE
                y1 = (r + 1) * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                cell = self.field[r][c]

                color = {
                    ".": "#1e293b",
                    "S": "#1d4ed8",
                    "X": "#b91c1c",
                    "O": "#334155"
                }[cell]

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#0ea5e9")

    def get_coords(self):
        try:
            r = int(self.x_entry.get())
            c = int(self.y_entry.get())
            if 0 <= r < FIELD_SIZE and 0 <= c < FIELD_SIZE:
                return r, c
        except ValueError:
            pass
        return None

    def place_ship(self):
        coords = self.get_coords()
        if not coords:
            self.message.config(text="Invalid coordinates.")
            return

        r, c = coords
        if self.field[r][c] == ".":
            self.field[r][c] = "S"
            self.message.config(text=f"Ship placed at ({r},{c})")
        else:
            self.message.config(text="Cell already occupied.")

        self.draw_grid()

    def fire(self):
        coords = self.get_coords()
        if not coords:
            self.message.config(text="Invalid coordinates.")
            return

        r, c = coords
        if self.field[r][c] == "S":
            self.field[r][c] = "X"
            self.message.config(text="Hit!")
        elif self.field[r][c] == ".":
            self.field[r][c] = "O"
            self.message.config(text="Miss.")
        else:
            self.message.config(text="Already targeted.")

        self.draw_grid()


if __name__ == "__main__":
    root = tk.Tk()
    app = BattleshipsUI(root)
    root.mainloop()
