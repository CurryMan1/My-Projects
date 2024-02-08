import tkinter as tk
from random import randint

class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Snake')
        self.resizable(False, False)

        #game vars
        self.game_frame = tk.Frame(self)
        self.board_width = 30
        self.squares = [[] for i in range(self.board_width)]
        self.dir_x, self.dir_y = 1, 0
        self.snake = [(self.board_width // 2, self.board_width // 2)]
        self.delay = 100
        self.score = 0

        #for keys
        self.changed = False

        #bind arrows
        self.bind('<Key>', self.change_direction)

        #setup ui
        self.create_grid()
        self.game_frame.pack()

    def create_grid(self):
        for i in range(self.board_width**2):
            square = tk.Label(self.game_frame, width=2, bg='black')
            square.grid(row=i//self.board_width, column=i%self.board_width)
            self.squares[i//self.board_width].append(square)

        #fruit
        self.new_fruit()

        #snake
        self.move_snake()

    def change_direction(self, event):
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

        new_head = ((self.snake[0][0] + self.dir_x)%self.board_width, (self.snake[0][1] + self.dir_y)%self.board_width)
        if new_head in self.snake:
            self.game_over()
            return

        if new_head == self.fruit_pos:
            self.new_fruit()
        else:
            tail = self.snake.pop()
            self.squares[tail[1]][tail[0]]['bg'] = 'black'

        self.snake.insert(0, new_head)

        self.draw_snake()

        self.after(self.delay, self.move_snake)

    def new_fruit(self):
        self.score += 1
        while True:
            self.fruit_pos = (randint(0, self.board_width-1), randint(0, self.board_width-1))
            if self.fruit_pos not in self.snake:
                x, y = self.fruit_pos
                self.squares[y][x]['bg'] = 'red'
                break

    def game_over(self):
        win = tk.Toplevel(root)
        tk.Label(win, text=f'You Lost!\nScore: {self.score}', font='helvetica 25 bold').pack()

    def draw_snake(self):
        for x, y in self.snake:
            self.squares[y][x]['bg'] = 'green'


if __name__ == '__main__':
    g = Game()
    g.mainloop()
