from tkinter import *
from tkinter import font
import random
import re

root = Tk()
root.title('15 Puzzle')
root.iconbitmap('C:/Users/user/Downloads/depositphotos_66714493-stock-photo-number-15.ico')
root.resizable(False, False)
widgets = []
widgets.append(root)
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] #mixed up
random.shuffle(numbers)
buttons = [] #in order
sample_buttons = []
labels = []
selectedButton = 0
inversions = 0
time = -1
moves = 0
finish = False
sample = numbers[:]

#options
chosen_font = 0
chosen_colour_scheme = 0
colour_schemes = [['white', 'grey'], ['white', 'black'], ['orange', '#5B84B1'], ['#949398', '#F4DF4E'], ['#FC766A', '#5B84B1'], ['#D6ED17', '#606060'], ['red', 'black']]

#frames
game_frame = Frame(root, bg=colour_schemes[chosen_colour_scheme][1])
start_frame = Frame(root, bg=colour_schemes[chosen_colour_scheme][1])
option_menu = Frame(root, bg=colour_schemes[chosen_colour_scheme][1])
help_frame = Frame(root, bg=colour_schemes[chosen_colour_scheme][1])
scores_frame = Frame(root, bg=colour_schemes[chosen_colour_scheme][1])
widgets.append(game_frame)
widgets.append(start_frame)
widgets.append(option_menu)
widgets.append(help_frame)
widgets.append(scores_frame)

#data
data = 'scores.txt'
with open(data) as file:
    lines = file.readlines()
names = []
scores = []
lines = sorted(lines, key=lambda x:int(re.search(r'\d+', x).group()))

#gets all names
for i in lines:
    names.append(i.split(',')[0])
    scores.append(int(i.split(',')[1]))

#check if solvable (and make solvable)
for q in range(15):
    if sample[sample.index(q + 1)] != sample[q]:
        sample[sample.index(q + 1)], sample[q] = sample[q], sample[sample.index(q + 1)]
        inversions += 1
if inversions % 2 == 1:
    numbers[0], numbers[1] = numbers[1], numbers[0]
numbers.append('')

#functions
def end_program():
    error_message1.pack_forget()
    error_message2.pack_forget()
    if ' ' in name_entry.get() or 2 >= len(name_entry.get())  or len(name_entry.get()) >= 20 or '.' in name_entry.get():
        error_message1.grid(columnspan=4)
        return None
    elif name_entry.get() in names:
        if time >= int(scores[names.index(name_entry.get())]):
            error_message2.grid(columnspan=4)
            return None
        else:
            popup()
            return None
    lines.append(f'{name_entry.get()},{time}\n')
    with open(data, 'w') as file:
        for line in lines:
            file.write(line)

    name_entry.destroy()
    enter.destroy()
    error_message1.destroy()
    error_message2.destroy()
    Label(game_frame, text='Thanks for playing', font=(font.families()[chosen_font], 20), bg=colour_schemes[chosen_colour_scheme][1], fg=colour_schemes[chosen_colour_scheme][0]).grid(columnspan=4)
    root.after(3000, lambda: exit())

def popup():
    global ask
    ask = Toplevel(root, bg=colour_schemes[chosen_colour_scheme][1])
    ask.title('Warning')
    ask.iconbitmap('C:/Users/user/Downloads/warning-512.ico')
    confirmb = Label(ask,
                     text="WOULD YOU LIKE TO REPLACE THE SCORE?\n"
                          "\n"
                          "That name is already taken,\n"
                          "and you got a better score than them.\n"
                          "If this is you, well done, you can\n"
                          "replace your score by clicking YES.\n"
                          "If not, you can either give this\n"
                          "person a better score, or claim the\n"
                          "score under a different name\n"
                          "for yourself by pressing NO.",
                     font=(font.families()[chosen_font], 20), bg=colour_schemes[chosen_colour_scheme][1],
                     fg=colour_schemes[chosen_colour_scheme][0])
    confirmb.grid(columnspan=2)
    yes = Button(ask, text='Yes', font=(font.families()[chosen_font], 20), bg=colour_schemes[chosen_colour_scheme][1],
                 fg=colour_schemes[chosen_colour_scheme][0], command=lambda: confirm(0))
    no = Button(ask, text='No', font=(font.families()[chosen_font], 20), bg=colour_schemes[chosen_colour_scheme][1],
                fg=colour_schemes[chosen_colour_scheme][0], command=lambda: confirm(1))
    yes.grid(row=1, column=0, sticky=E)
    no.grid(row=1, column=1, sticky=W)

def confirm(q):
    if q == 0:
        lines[names.index(name_entry.get())] = f'{name_entry.get()},{time}\n'
        with open(data, 'w') as file:
            for line in lines:
                file.write(line)
        root.after(2000, exit())
    ask.destroy()

def scoress():
    start_frame.pack_forget()
    scores_frame.pack()

def scroll(direction):
    itera = 0
    if direction == 2:
        for i in names[int(labels[0].cget('text').split('.')[0])+9:int(labels[0].cget('text').split('.')[0])+19]:
            labels[itera].config(text=f'{names.index(i)+1}. {i} solved it in {scores[names.index(i)]}s')
            last_label = labels[itera]
            itera += 1
        if itera != 0:
            for i in labels[labels.index(last_label)+1:]:
                i.config(text='')
        up.config(state='normal')
        if labels[-1].cget('text') == '' or int(labels[-1].cget('text').split('.')[0])+1 > len(names):
            down.config(state='disabled')
    else:
        for i in names[int(labels[0].cget('text').split('.')[0]) -11:int(labels[0].cget('text').split('.')[0]) - 1]:
            labels[itera].config(text=f'{names.index(i) + 1}. {i} solved it in {scores[names.index(i)]}s')
            itera += 1
        down.config(state='normal')
        if labels[0].cget('text').split('.')[0] == '1':
            up.config(state='disabled')

def enter_name():
    name_entry.grid(columnspan=4)
    enter.grid(columnspan=4)

def start_game():
    start_frame.pack_forget()
    game_frame.pack()
    update()

def start_menu():
    scores_frame.pack_forget()
    help_frame.pack_forget()
    option_menu.pack_forget()
    start_frame.pack()

def options():
    start_frame.pack_forget()
    option_menu.pack()

def help_menu():
    start_frame.pack_forget()
    help_frame.pack()

def change_font(x):
    global chosen_font
    if chosen_font == len(font.families())-1 or chosen_font == -len(font.families()):
        chosen_font = 0
    else:
        chosen_font += x
    for widget in widgets:
        try:
            widget.config(font=(font.families()[chosen_font], int(widget.cget('font').split()[-1])))
        except:
            pass

def change_colours(x):
    global chosen_colour_scheme
    if x == 0:
        colour_schemes[chosen_colour_scheme][0], colour_schemes[chosen_colour_scheme][1] = colour_schemes[chosen_colour_scheme][1], colour_schemes[chosen_colour_scheme][0]
    elif chosen_colour_scheme == len(colour_schemes)-1 or chosen_colour_scheme == -len(colour_schemes):
        chosen_colour_scheme = 0
    else:
        chosen_colour_scheme += x
    for widget in widgets:
        try:
            if widget.cget('text') == '' or widget == name_entry:
                widget.config(bg=colour_schemes[chosen_colour_scheme][0], fg=colour_schemes[chosen_colour_scheme][1])
            else:
                try:
                    widget.config(fg=colour_schemes[chosen_colour_scheme][0], bg=colour_schemes[chosen_colour_scheme][1])
                except:
                    widget.config(bg=colour_schemes[chosen_colour_scheme][1])
        except:
            try:
                widget.config(fg=colour_schemes[chosen_colour_scheme][0], bg=colour_schemes[chosen_colour_scheme][1])
            except:
                widget.config(bg=colour_schemes[chosen_colour_scheme][1])

def update():
    global time
    if finish:
        #break loop
        return 'WELL DONE'
    time += 1
    timer.config(text=f'Time: {time}s')
    root.after(1000, update)

def click(x):
    global blankLoc, selectedButton, moves, finish
    selectedButton = buttons[x]
    if (x == buttons.index(blankLoc) - 4 or x == buttons.index(blankLoc) + 4 or x == buttons.index(blankLoc) - 1
            or x == buttons.index(blankLoc) + 1) and selectedButton.cget('text') != '':
        moves += 1
        mover.config(text=f'Moves: {moves}')
        blankLoc.config(text=selectedButton.cget('text'), bg=colour_schemes[chosen_colour_scheme][1], fg=colour_schemes[chosen_colour_scheme][0])
        blankLoc = selectedButton
        selectedButton.config(text='', bg=colour_schemes[chosen_colour_scheme][0], fg=colour_schemes[chosen_colour_scheme][0])
    for j in range(15):
        if int(buttons[j].cget('text')) == j+1:
            pass
        else:
            break
        if j == 14:
            finish = True
            win = Label(game_frame, text='YOU WIN', font=(font.families()[chosen_font], 40), bg=colour_schemes[chosen_colour_scheme][1], fg=colour_schemes[chosen_colour_scheme][0])
            win.grid(row=5, columnspan=4)
            for button in buttons:
                button.config(state='disabled')
            enter_name()

#setup

#game_frame
timer = Label(game_frame, font=(font.families()[chosen_font], 30), text=f'Time: {time}s', fg=colour_schemes[chosen_colour_scheme][0], bg=colour_schemes[chosen_colour_scheme][1])
timer.grid(row=0, column=0, columnspan=2, sticky=W)
mover = Label(game_frame, font=(font.families()[chosen_font], 30), text=f'Moves: {moves}', fg=colour_schemes[chosen_colour_scheme][0], bg=colour_schemes[chosen_colour_scheme][1])
mover.grid(row=0, column=2, columnspan=2, sticky=E)
widgets.append(timer)
widgets.append(mover)

for i in range(16):
    button = Button(game_frame, font=(font.families()[chosen_font], 50), width=3, height=1, command=lambda i=i:click(i), bg='grey', fg='white', text=str(numbers[i]))
    button.grid(row=(i // 4)+1, column=i % 4)
    buttons.append(button)
    widgets.append(button)
    if i == 15:
        sample_button = Button(option_menu, font=(font.families()[chosen_font], 50), width=3, height=1, bg='white')
    else:
        sample_button = Button(option_menu, font=(font.families()[chosen_font], 50), width=3, height=1, bg=colour_schemes[chosen_colour_scheme][1], fg=colour_schemes[chosen_colour_scheme][0], text=str(i + 1))
    sample_button.grid(row=(i // 4) + 1, column=i % 4)
    sample_buttons.append(button)
    widgets.append(sample_button)

blankLoc = buttons[-1]
blankLoc.config(bg=colour_schemes[chosen_colour_scheme][0])
widgets.append(blankLoc)

name_entry = Entry(game_frame, width=10, font=(font.families()[chosen_font],20), fg=buttons[0].cget('bg'))
enter = Button(game_frame, text='Enter Name', font=(font.families()[chosen_font],20), command=end_program, bg=colour_schemes[chosen_colour_scheme][1], fg=colour_schemes[chosen_colour_scheme][0])
error_message1 = Label(game_frame, text='Enter a valid name\n(2-18 Characters, No Spaces, No "."s)', font=(font.families()[chosen_font],20), bg=colour_schemes[chosen_colour_scheme][1], fg=colour_schemes[chosen_colour_scheme][0])
error_message2 = Label(game_frame, text="Name is already taken\n(and your score isn't lower than their's)", font=(font.families()[chosen_font],20), bg=colour_schemes[chosen_colour_scheme][1], fg=colour_schemes[chosen_colour_scheme][0])
widgets.append(name_entry)
widgets.append(enter)
widgets.append(error_message1)
widgets.append(error_message2)

#start_frame
help = Button(start_frame, text='?', font=(font.families()[chosen_font], 30), fg=colour_schemes[chosen_colour_scheme][0], bg=colour_schemes[chosen_colour_scheme][1], command=help_menu)
help.place(height=40, width=40)
widgets.append(help)
title = Label(start_frame, text='15 Puzzle', font=(font.families()[chosen_font], 50), fg=colour_schemes[chosen_colour_scheme][0], bg=colour_schemes[chosen_colour_scheme][1])
title.grid(pady=20)
widgets.append(title)
start_button = Button(start_frame, text='Start Game', width=10, command=start_game, font=(font.families()[chosen_font], 50), fg=colour_schemes[chosen_colour_scheme][0], bg=colour_schemes[chosen_colour_scheme][1])
start_button.grid(padx=20)
widgets.append(start_button)
options = Button(start_frame, text='Options', width=10, command=options, font=(font.families()[chosen_font], 50), fg=colour_schemes[chosen_colour_scheme][0], bg=colour_schemes[chosen_colour_scheme][1])
options.grid(padx=20)
widgets.append(options)
highscores = Button(start_frame, text='Highscores', width=10, command=scoress, font=(font.families()[chosen_font], 50), fg=colour_schemes[chosen_colour_scheme][0], bg=colour_schemes[chosen_colour_scheme][1])
highscores.grid(padx=20, pady=(0, 20))
widgets.append(highscores)
start_frame.pack()

#option_menu
back = Button(option_menu, text='←', command=start_menu, font=(font.families()[chosen_font], 25), fg=colour_schemes[chosen_colour_scheme][0], bg=colour_schemes[chosen_colour_scheme][1])
back.grid(row=0, column=0, pady=(0, 30), sticky=NW)
widgets.append(back)

font_label = Label(option_menu, text='Change Font', font=(font.families()[chosen_font], 20), fg=colour_schemes[chosen_colour_scheme][0], bg=colour_schemes[chosen_colour_scheme][1])
font_label.grid(row=5, column=0, columnspan=2)
widgets.append(font_label)

next_font = Button(option_menu, text='→', font=(font.families()[chosen_font], 35), command=lambda: change_font(1), fg=colour_schemes[chosen_colour_scheme][0], bg=colour_schemes[chosen_colour_scheme][1])
next_font.grid(row=6, column=1, sticky=W)
widgets.append(next_font)

previous_font = Button(option_menu, text='←', font=(font.families()[chosen_font], 35), command=lambda: change_font(-1), fg=colour_schemes[chosen_colour_scheme][0], bg=colour_schemes[chosen_colour_scheme][1])
previous_font.grid(row=6, column=0, sticky=E)
widgets.append(previous_font)

colour_label = Label(option_menu, text='Change\nColour Scheme', font=(font.families()[chosen_font], 20), fg=colour_schemes[chosen_colour_scheme][0], bg=colour_schemes[chosen_colour_scheme][1])
colour_label.grid(row=5, column=2, columnspan=2)
widgets.append(colour_label)

next_colour = Button(option_menu, text='←', font=(font.families()[chosen_font], 35), command=lambda: change_colours(-1), fg=colour_schemes[chosen_colour_scheme][0], bg=colour_schemes[chosen_colour_scheme][1])
next_colour.grid(row=6, column=2, sticky=E)
widgets.append(next_colour)

previous_colour = Button(option_menu, text='→', font=(font.families()[chosen_font], 35), command=lambda: change_colours(1), fg=colour_schemes[chosen_colour_scheme][0], bg=colour_schemes[chosen_colour_scheme][1])
previous_colour.grid(row=6, column=3, sticky=W)
widgets.append(previous_colour)

invert_colours = Button(option_menu, text='Invert Colours', font=(font.families()[chosen_font], 35), command=lambda: change_colours(0), fg=colour_schemes[chosen_colour_scheme][0], bg=colour_schemes[chosen_colour_scheme][1])
invert_colours.grid(row=7, columnspan=4)
widgets.append(invert_colours)

#help_frame
instructions = Label(help_frame, text='The aim of the game is to order\nall the tiles from 1-15 by clicking them.\nGo to the options menu to\nfind how this should look like.', font=(font.families()[chosen_font], 35), fg=colour_schemes[chosen_colour_scheme][0], bg=colour_schemes[chosen_colour_scheme][1])
instructions.grid()
widgets.append(instructions)
back2 = Button(help_frame, text='←', command=start_menu, font=(font.families()[chosen_font], 25), fg=colour_schemes[chosen_colour_scheme][0], bg=colour_schemes[chosen_colour_scheme][1])
back2.place(width=50, height=50)
widgets.append(back)

#scores_frame
up = Button(scores_frame, state='disabled', text='↑', command=lambda:scroll(1), width=30, font=(font.families()[chosen_font], 25), fg=colour_schemes[chosen_colour_scheme][0], bg=colour_schemes[chosen_colour_scheme][1])
up.grid(row=0, column=0, pady=(0, 30), columnspan=3)
widgets.append(up)

back3 = Button(scores_frame, text='←', command=start_menu, font=(font.families()[chosen_font], 25), fg=colour_schemes[chosen_colour_scheme][0], bg=colour_schemes[chosen_colour_scheme][1])
back3.grid(row=0, column=0, pady=(0, 30), sticky=NW)
widgets.append(back3)

for i in range(10):
    label = Label(scores_frame, text=f'{i+1}. {names[i]} solved it in {scores[i]}s', font=(font.families()[chosen_font], 30), fg=colour_schemes[chosen_colour_scheme][0], bg=colour_schemes[chosen_colour_scheme][1])
    label.grid(pady=2)
    widgets.append(label)
    labels.append(label)

down = Button(scores_frame, text='↓', command=lambda:scroll(2), width=30, font=(font.families()[chosen_font], 25), fg=colour_schemes[chosen_colour_scheme][0], bg=colour_schemes[chosen_colour_scheme][1])
down.grid(pady=(30,0))
widgets.append(down)

root.mainloop()