from tkinter import *
import random

root = Tk()
root.title('Simon Says')
colours = ['green', 'red', 'yellow', 'blue']
buttons = []
real_list = []
user_input = []
score = 0

def signals():
    global inputt
    real_list.append(random.choice(buttons))
    inputt = False
    root.after(750, root.quit)
    root.mainloop()
    for button in real_list:
        root.after(250, root.quit)
        root.mainloop()
        button.config(bg='white')
        root.after(250, root.quit)
        root.mainloop()
        button.config(bg=colours[buttons.index(button)])
    inputt = True

def click(button):
    global score, user_input
    if inputt:
        user_input.append(buttons[button])
        if user_input == real_list:
            score += 1
            score_label.config(text=f'Score: {score}')
            user_input = []
            signals()
        elif user_input != real_list[:len(user_input)]:
            wrong = Label(root, text='Game OVER', font=('System', 40))
            wrong.grid(row=3, columnspan=2)
            for button in buttons:
                button.config(state='disabled')
            root.after(3000, lambda: exit())

for i in range(4):
    button = Button(root,width=40, height=20, command=lambda i=i:click(i), bg=colours[i])
    button.grid(row=(i // 2)+1, column=i % 2)
    buttons.append(button)

score_label = Label(root, text=f'Score: {score}', font=('System', 40))
score_label.grid(row=0,columnspan=1, sticky=W)

signals()
root.mainloop()