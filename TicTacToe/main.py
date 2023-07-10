from tkinter import *

root = Tk()
root.title('Tic Tac Toe')
root.iconbitmap("C:/Users/user/Documents/Hardhik's Stuff/Random Stuff/TTT.ico")
root.resizable(False, False)
buttons = [[], [], []]
turn = 0

def check():
    #rows
    for j in range(3):
        if buttons[0][j].cget('bg') == 'red' and buttons[1][j].cget('bg') == 'red' and buttons[2][j].cget('bg') == 'red':
            return True
        elif buttons[0][j].cget('bg') == 'blue' and buttons[1][j].cget('bg') == 'blue' and buttons[2][j].cget('bg') == 'blue':
            return False
    #columns
    for j in range(3):
        if buttons[j][0].cget('bg') == 'red' and buttons[j][1].cget('bg') == 'red' and buttons[j][2].cget('bg') == 'red':
            return True
        elif buttons[j][0].cget('bg') == 'blue' and buttons[j][1].cget('bg') == 'blue' and buttons[j][2].cget('bg') == 'blue':
            return False
    #diagonals
    if buttons[0][0].cget('bg') == 'red' and buttons[1][1].cget('bg') == 'red' and buttons[2][2].cget('bg') == 'red':
        return True
    elif buttons[0][0].cget('bg') == 'blue' and buttons[1][1].cget('bg') == 'blue' and buttons[2][2].cget('bg') == 'blue':
        return False
    if buttons[0][2].cget('bg') == 'red' and buttons[1][1].cget('bg') == 'red' and buttons[2][0].cget('bg') == 'red':
        return True
    elif buttons[0][2].cget('bg') == 'blue' and buttons[1][1].cget('bg') == 'blue' and buttons[2][0].cget('bg') == 'blue':
        return False

def click(x):
    global turn
    if turn % 2 == 0:
        buttons[x // 3][x % 3].config(bg='red', state='disabled')
    else:
        buttons[x // 3][x % 3].config(bg='blue', state='disabled')
    turn += 1
    if turn == 9:
        label = Label(root, font=('System',90), text='DRAW',)
        label.grid(row=3, columnspan=3)
        root.after(5000, lambda: exit())
    if check():
        label = Label(root, font=('System',90), text='Red WINS', fg='red')
        label.grid(row=3, columnspan=3)
        root.after(5000, lambda: exit())
    elif check() == False:
        label = Label(root, font=('System',90), text='Blue WINS', fg='blue')
        label.grid(row=3, columnspan=3)
        root.after(5000, lambda: exit())

for i in range(9):
    button = Button(root, padx=100, pady=100, command=lambda i=i:click(i), bg='black')
    button.grid(row=i // 3, column=i % 3)
    buttons[i // 3].append(button)

root.mainloop()