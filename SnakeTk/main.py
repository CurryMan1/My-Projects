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
        sequence = self.sequence[:]
        print(len(self.snake)-1 == len(self.sequence))
        del sequence[len(self.snake)-1::]
        print(len(self.snake) - 1 == len(self.sequence), '\n')
        i = 0
        while i < len(self.snake):
            part = self.snake[i]
            y, x = self.get_pos(part)
            if i == 0:
                dir_y, dir_x = self.dir_y, self.dir_x
                new_sq = self.squares[(y + dir_y) % self.board_width][(x + dir_x) % self.board_width]
                self.sequence.insert(0, (self.dir_y, self.dir_x))
                if new_sq['bg'] == 'red':
                    #fruit
                    self.squares[randint(0, self.board_width - 1)][randint(0, self.board_width - 1)]['bg'] = 'red'

                    sequence.insert(0, (self.dir_y, self.dir_x))

                    #new part
                    end_y, end_x = self.get_pos(self.snake[-1])
                    end_dir_y, end_dir_x = sequence[-1]

                    new_part = self.squares[(end_y+(-1*end_dir_y)) % self.board_width][(end_x+(-1*end_dir_x)) % self.board_width]
                    new_part['bg'] = 'green'
                    self.snake.append(new_part)
            else:
                dir_y, dir_x = sequence[i-1]
                new_sq = self.squares[(y + dir_y) % self.board_width][(x + dir_x) % self.board_width]

            part['bg'] = 'black'
            new_sq['bg'] = 'green'

            self.snake[i] = new_sq
            i+=1

        del self.sequence[len(self.snake)-1::]

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