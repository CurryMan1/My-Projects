import tkinter as tk
from random import randint

class Game:
    def __init__(self, root):
        #game vars
        self.root = root
        self.game_frame = tk.Frame(root)
        self.board_width = 40
        self.squares = [[] for i in range(self.board_width)]
        self.snake = []
        self.sequence = []
        self.delay = 100
        self.changed = False
        self.dir_x, self.dir_y = 1, 0
        self.new_part = False

        #bind arrows
        root.bind('<Key>', self.change_direction)

        #setup ui
        self.create_grid()
        self.game_frame.pack()

    def create_grid(self):
        for i in range(self.board_width**2):
            square = tk.Label(self.game_frame, width=2, bg='black')
            square.grid(row=i//self.board_width, column=i%self.board_width)
            self.squares[i//self.board_width].append(square)

        #snake
        self.squares[int(self.board_width/2)][int(self.board_width/2)]['bg'] = 'green'
        self.snake.append(self.squares[int(self.board_width/2)][int(self.board_width/2)])
        self.move_snake()

        #fruit
        self.squares[randint(0, self.board_width-1)][randint(0, self.board_width-1)]['bg'] = 'red'

    def change_direction(self, event):
        print('yo')
        if event.keysym in ['Up', 'Down', 'Left', 'Right'] and not self.changed:
            key = event.keysym[0]
            self.changed = True
            if key in 'UD':
                if self.dir_y == 0 or len(self.snake) == 1:
                    if key == 'U':
                        self.dir_x, self.dir_y = 0, -1
                    else:
                        self.dir_x, self.dir_y = 0, 1
            else:
                if self.dir_x == 0 or len(self.snake) == 1:
                    if key == 'L':
                        self.dir_x, self.dir_y = -1, 0
                    else:
                        self.dir_x, self.dir_y = 1, 0

    def move_snake(self):
        self.changed = False
        self.new_part = False
        sequence = self.sequence[:]
        for i, part in enumerate(self.snake):
            y, x = self.get_pos(part)
            # we'll start again

        root.after(self.delay, self.move_snake)

    def get_pos(self, square):
        for i, row in enumerate(self.squares):
            if square in row:
                y = i
                for j, row_sqr in enumerate(row):
                    if square == row_sqr:
                        x = j
                        return y, x

root = tk.Tk()
root.title('Snake')
root.resizable(False, False)
g = Game(root)
root.mainloop()