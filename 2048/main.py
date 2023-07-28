from tkinter import *
import random

root = Tk()
root.title('2048')
root.resizable(False, False)


class Game:
    def __init__(self):
        self.squares = []
        for i in range(16):
            square = Label(root, bg='red', width=6, height=3, font='system 40', text=random.choice(['','',2, 4, '', 1]))
            square.grid(row=i // 4, column=i % 4, pady=5, padx=5)
            self.squares.append(square)

    def merge_board(self, direction):
        immovable = 0
        if direction in 'LR':
            board = [[self.squares[0], self.squares[1], self.squares[2], self.squares[3],],
                     [self.squares[4], self.squares[5], self.squares[6], self.squares[7],],
                     [self.squares[8], self.squares[9], self.squares[10], self.squares[11],],
                     [self.squares[12], self.squares[13], self.squares[14], self.squares[15],]]
        else:
            board = [[self.squares[0], self.squares[4], self.squares[8], self.squares[12],],
                     [self.squares[1], self.squares[5], self.squares[9], self.squares[13],],
                     [self.squares[2], self.squares[6], self.squares[10], self.squares[14],],
                     [self.squares[3], self.squares[7], self.squares[11], self.squares[15],]]

        if direction in 'DR':
            way = 1
        else:
            way = -1

        for row in range(4):
            for column in range(4):
                square_text = board[row][column].cget('text')
                #check text isn't empty
                if square_text != '':
                    while immovable != 16:
                        far_blnk_sq = board[row][column]
                        for i in range(way*1, way*4): #(1, 2, 3)
                            if column+(way*i) not in range(-3, 4) or board[row][column + (way * i)].cget('text') != '':
                                break
                            next_square = board[row][column + (way * i)]
                            if next_square.cget('text') == '':
                                far_blnk_sq = next_square
                        board[row][column].config(text='')
                        far_blnk_sq.config(text=square_text)

    def get_key(self, key):
        if key.keysym in ['Up', 'Down', 'Left', 'Right']:
            self.merge_board(key.keysym[0])
        else:
            pass

game = Game()
root.bind('<Key>', game.get_key)
root.mainloop()