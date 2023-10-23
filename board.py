import sys
import tkinter as tk
from random import randrange
import time
GRID_SIZE = 9
BLOCK_SIZE = 40
WINDOW_SIZE = GRID_SIZE * BLOCK_SIZE
NUM_MINES = 9


class MinesweeperBoard(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.buttons = [[0] * GRID_SIZE for i in range(GRID_SIZE)]
        self.title("Minesweeper game")
        self.started = False
        self.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}")
        self.mine_coords = [[0] * GRID_SIZE for i in range(GRID_SIZE)]

        self.bomb = tk.PhotoImage(file=r"assets\bomb.png")
        self.bomb.zoom(20, 20)

        for x_coord in range(GRID_SIZE):
            for y_coord in range(GRID_SIZE):
                button = tk.Button(self, text="", compound="c", width=2, height=1)
                button.config(command=lambda button=button: self.clicked(button))

                self.buttons[x_coord][y_coord] = button
                self.buttons[x_coord][y_coord].grid(row=x_coord, column=y_coord)

    def disable_button(self, x_coord, y_coord):
        self.buttons[x_coord][y_coord].config(state=tk.DISABLED, relief=tk.SUNKEN)

    def add_num_to_button(self, x_coord, y_coord, number):
        self.disable_button(x_coord, y_coord)
        self.buttons[x_coord][y_coord].config(text=str(number))

    def count_mines(self, row, column):
        num_mines = 0
        if row > 0:
            if self.mine_coords[row - 1][column]:
                num_mines += 1
        if row < GRID_SIZE - 1:
            if self.mine_coords[row + 1][column]:
                num_mines += 1
        if column > 0:
            if self.mine_coords[row][column - 1]:
                num_mines += 1
        if column < GRID_SIZE - 1:
            if self.mine_coords[row][column + 1]:
                num_mines += 1

        if column > 0 and row > 0:
            if self.mine_coords[row - 1][column - 1]:
                num_mines += 1
        if column < GRID_SIZE - 1 and row > 0:
            if self.mine_coords[row - 1][column + 1]:
                num_mines += 1
        if row < GRID_SIZE - 1 and column > 0:
            if self.mine_coords[row + 1][column - 1]:
                num_mines += 1
        if column < GRID_SIZE - 1 and row < GRID_SIZE - 1:
            if self.mine_coords[row + 1][column + 1]:
                num_mines += 1
        return num_mines

    def floodfill(self, row, column):
        if self.buttons[row][column]["state"] != "disabled":
            mine_count = self.count_mines(row, column)
            if mine_count == 0:
                self.disable_button(row, column)
                if row > 0:
                    self.floodfill(row - 1, column)
                if row < GRID_SIZE - 1:
                    self.floodfill(row + 1, column)
                if column > 0:
                    self.floodfill(row, column - 1)
                if column < GRID_SIZE - 1:
                    self.floodfill(row, column + 1)

                if column > 0 and row > 0:
                    self.floodfill(row - 1, column - 1)
                if column < GRID_SIZE - 1 and row > 0:
                    self.floodfill(row - 1, column + 1)
                if row < GRID_SIZE - 1 and column > 0:
                    self.floodfill(row + 1, column - 1)
                if column < GRID_SIZE - 1 and row < GRID_SIZE - 1:
                    self.floodfill(row + 1, column + 1)
            else:
                self.add_num_to_button(row, column, mine_count)

    def explode(self):
        for x in range(NUM_MINES):
            for y in range(NUM_MINES):
                if self.mine_coords[x][y]:
                    self.buttons[x][y].config(image=self.bomb)

    def clicked(self, button):
        x_coord = button.grid_info()["row"]
        y_coord = button.grid_info()["column"]
        if not self.started:
            self.populate_mines()
            self.started = True

        self.floodfill(x_coord, y_coord)

    def populate_mines(self):
        for mine in range(NUM_MINES + 1):
            x_rand = randrange(GRID_SIZE)
            y_rand = randrange(GRID_SIZE)

            while self.mine_coords[x_rand][y_rand]:
                x_rand = randrange(GRID_SIZE)
                y_rand = randrange(GRID_SIZE)
            self.buttons[x_rand][y_rand].config(command=self.explode)

            self.mine_coords[x_rand][y_rand] = 1


if __name__ == "__main__":
    app = MinesweeperBoard()
    app.mainloop()
