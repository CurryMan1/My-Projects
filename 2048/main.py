from tkinter import *
import random

root = Tk()
root.title('2048')
root.resizable(False, False)
squares = [[],[],[],[]]


# no_unmovable = 0
# while no_unmovable < 16:
#     no_unmovable = 0
#     iteration = 0
#     for square in squares:
#         iteration += 1
#         if square.cget('text') != '' and squares.index(square)-4 >= 0:
#             if squares[squares.index(square)-4].cget('text') == '':
#                 squares[squares.index(square)-4].config(text=square.cget('text'))
#                 square.config(text='')
#             elif squares[squares.index(square)-4].cget('text') == square.cget('text'):
#                 squares[squares.index(square) - 4].config(text=str(int(squares[squares.index(square) - 4].cget('text')) + int(square.cget('text'))))
#                 square.config(text='')
#             else:
#                 no_unmovable += 1
#         else:
#             no_unmovable += 1
# if iteration != 1:
#     random_square = random.choice(squares)
#     while random_square.cget('text') != '':
#         random_square = random.choice(squares)
#     if random.random() <= 0.9:
#         random_square.config(text=2)
#     else:
#         random_square.config(text=4)

def up(x):
    for row in range(4):
        for column in range(4):
            if squares[row][column].cget('text') != '':
                try:
                    if squares[row][column].cget('text') == squares[row+1][column].cget('text'):
                        squares[row][column].config(text=str(int(squares[row][column].cget('text')) + int(squares[row+1][column].cget('text'))))
                        squares[row+1][column].config(text='')
                except:
                    pass

def down(x):
    print('down')

def left(x):
    print('left')

def right(x):
    print('right')


for i in range(16):
    square = Label(bg='red', width=6, height=3, font=('system', 40))
    square.grid(row=i//4, column=i%4, pady=5, padx=5)
    squares[i//4].append(square)

squares[0][0]['text'], squares[1][0]['text'] = 1, 1

# taken_square = random.choice(squares)
# second_square = random.choice(squares)
# while taken_square == second_square:
#     second_square = random.choice(squares)
# if random.random() <= 0.9:
#     taken_square.config(text=2)
# else:
#     taken_square.config(text=4)
#
# if random.random() <= 0.9:
#     second_square.config(text=2)
# else:
#     second_square.config(text=4)

root.bind('<Up>', up)
root.bind('<Down>', down)
root.bind('<Left>', left)
root.bind('<Right>', right)

root.mainloop()