import tkinter as tk
import random

GRID_LEN = 4
GRID_PADDING = 10
BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"

# Colors for tiles
BACKGROUND_COLOR_DICT = {
    2:      "#eee4da",
    4:      "#ede0c8",
    8:      "#f2b179",
    16:     "#f59563",
    32:     "#f67c5f",
    64:     "#f65e3b",
    128:    "#edcf72",
    256:    "#edcc61",
    512:    "#edc850",
    1024:   "#edc53f",
    2048:   "#edc22e",
}
CELL_COLOR_DICT = {
    2:      "#776e65",
    4:      "#776e65",
    8:      "#f9f6f2",
    16:     "#f9f6f2",
    32:     "#f9f6f2",
    64:     "#f9f6f2",
    128:    "#f9f6f2",
    256:    "#f9f6f2",
    512:    "#f9f6f2",
    1024:   "#f9f6f2",
    2048:   "#f9f6f2",
}

FONT = ("Verdana", 24, "bold")

class Game2048(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title('2048 Game')
        self.master.resizable(False, False)
        self.score = 0

        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()

        self.master.bind("<Key>", self.key_down)
        self.mainloop()

    def init_grid(self):
        background = tk.Frame(self, bg=BACKGROUND_COLOR_GAME, width=400, height=400)
        background.grid(pady=(100, 0))
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = tk.Frame(
                    background,
                    bg=BACKGROUND_COLOR_CELL_EMPTY,
                    width=100,
                    height=100
                )
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                label = tk.Label(
                    master=cell,
                    text="",
                    bg=BACKGROUND_COLOR_CELL_EMPTY,
                    justify=tk.CENTER,
                    font=FONT,
                    width=4,
                    height=2
                )
                label.grid()
                grid_row.append(label)
            self.grid_cells.append(grid_row)

        # Score label
        self.score_label = tk.Label(self, text=f"Score: {self.score}", font=("Verdana", 18, "bold"))
        self.score_label.grid(pady=(10, 0))

    def init_matrix(self):
        self.matrix = [[0] * GRID_LEN for _ in range(GRID_LEN)]
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(GRID_LEN) for j in range(GRID_LEN) if self.matrix[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.matrix[i][j] = 4 if random.random() < 0.1 else 2

    def update_grid_cells(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                value = self.matrix[i][j]
                if value == 0:
                    self.grid_cells[i][j].configure(
                        text="",
                        bg=BACKGROUND_COLOR_CELL_EMPTY
                    )
                else:
                    self.grid_cells[i][j].configure(
                        text=str(value),
                        bg=BACKGROUND_COLOR_DICT.get(value, "#3c3a32"),
                        fg=CELL_COLOR_DICT.get(value, "#f9f6f2")
                    )
        self.score_label.configure(text=f"Score: {self.score}")
        self.update_idletasks()

    def key_down(self, event):
        key = event.keysym
        moved = False
        score_gained = 0

        if key in ("Up", "w", "W"):
            self.matrix, score_gained, moved = self.move_up(self.matrix)
        elif key in ("Down", "s", "S"):
            self.matrix, score_gained, moved = self.move_down(self.matrix)
        elif key in ("Left", "a", "A"):
            self.matrix, score_gained, moved = self.move_left(self.matrix)
        elif key in ("Right", "d", "D"):
            self.matrix, score_gained, moved = self.move_right(self.matrix)

        if moved:
            self.score += score_gained
            self.add_new_tile()
            self.update_grid_cells()
            state = self.get_current_state()
            if state == "WON":
                self.show_game_over("You win!")
            elif state == "LOST":
                self.show_game_over("Game over!")

    # Movement helpers
    def compress(self, mat):
        changed = False
        new_mat = [[0] * GRID_LEN for _ in range(GRID_LEN)]
        for i in range(GRID_LEN):
            pos = 0
            for j in range(GRID_LEN):
                if mat[i][j] != 0:
                    new_mat[i][pos] = mat[i][j]
                    if j != pos:
                        changed = True
                    pos += 1
        return new_mat, changed

    def merge(self, mat):
        changed = False
        score = 0
        for i in range(GRID_LEN):
            for j in range(GRID_LEN - 1):
                if mat[i][j] == mat[i][j + 1] and mat[i][j] != 0:
                    mat[i][j] *= 2
                    mat[i][j + 1] = 0
                    score += mat[i][j]
                    changed = True
        return mat, score, changed

    def reverse(self, mat):
        return [row[::-1] for row in mat]

    def transpose(self, mat):
        return [list(row) for row in zip(*mat)]

    def move_left(self, mat):
        mat, c1 = self.compress(mat)
        mat, score, c2 = self.merge(mat)
        mat, _ = self.compress(mat)
        return mat, score, c1 or c2

    def move_right(self, mat):
        mat = self.reverse(mat)
        mat, score, changed = self.move_left(mat)
        mat = self.reverse(mat)
        return mat, score, changed

    def move_up(self, mat):
        mat = self.transpose(mat)
        mat, score, changed = self.move_left(mat)
        mat = self.transpose(mat)
        return mat, score, changed

    def move_down(self, mat):
        mat = self.transpose(mat)
        mat, score, changed = self.move_right(mat)
        mat = self.transpose(mat)
        return mat, score, changed

    def get_current_state(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                if self.matrix[i][j] == 2048:
                    return "WON"
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                if self.matrix[i][j] == 0:
                    return "GAME NOT OVER"
        for i in range(GRID_LEN):
            for j in range(GRID_LEN - 1):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return "GAME NOT OVER"
        for j in range(GRID_LEN):
            for i in range(GRID_LEN - 1):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return "GAME NOT OVER"
        return "LOST"

    def show_game_over(self, message):
        top = tk.Toplevel(self)
        top.title("Game Over")
        tk.Label(top, text=message, font=("Verdana", 18, "bold")).pack(pady=10)
        tk.Button(top, text="Restart", command=lambda: [top.destroy(), self.restart_game()]).pack(pady=5)
        tk.Button(top, text="Exit", command=self.master.destroy).pack(pady=5)

    def restart_game(self):
        self.score = 0
        self.init_matrix()
        self.update_grid_cells()

if __name__ == "__main__":
    Game2048()

