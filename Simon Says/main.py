from tkinter import *
import random

root = Tk()
root.title('Simon Says')
colors = ['green', 'red', 'yellow', 'blue']
tiles = []
user_input = []
real_list = []
score = 0

def signals():
    global inputting
    real_list.append(random.choice(tiles))
    inputting = False
    root.after(500, root.quit)
    root.mainloop()
    for tile in real_list:
        tile.config(bg='white')
        root.after(250, root.quit)
        root.mainloop()
        tile.config(bg=colors[tiles.index(tile)])
        root.after(250, root.quit)
        root.mainloop()
    inputting = True

def click(tile):
    global user_input, score
    if inputting:
        user_input.append(tiles[tile])
        if user_input == real_list:
            score += 1
            score_display.config(text=f'Score: {score}')
            user_input = []
            signals()
        elif user_input != real_list[:len(user_input)]:
            wrong = Label(root, text='Game OVER!', font=('System', 50))
            wrong.grid(columnspan=2)
            for tile in tiles:
                button.config(state='disabled')
            root.after(3000, exit)

for i in range(4):
    tile = Button(root, width=40, height=20, command=lambda i=i: click(i), bg=colors[i])
    tile.grid(row=(i // 2)+1, column=i%2)
    tiles.append(tile)

score_display = Label(text=f'Score: {score}', font=('System', 40))
score_display.grid(row=0, sticky=W)

signals()
root.mainloop()