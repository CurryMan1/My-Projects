from tkinter import *
from tkinter import ttk
import random
import time as ti
import math

#SETUP==================================================================================================================
yellow = '#D6ED17'
grey = '#606060'

#TKINTER================================================================================================================
root = Tk()
root.iconbitmap('C:/Users/user/Downloads/Iconsmind-Outline-Timer-2.ico')
root.title('Benchmark Tests')
root.resizable(False, False)

main_menu = Frame(root, bg=grey)
reaction = Frame(root, bg=grey)
clicks = Frame(root, bg=grey)
visual_memory = Frame(root, bg=grey)
number_memory = Frame(root, bg=grey)
chimp_test = Frame(root, bg=grey)
verbal_test = Frame(root, bg=grey)

frames = [reaction, clicks, visual_memory, number_memory, chimp_test, verbal_test]
def sleep(milliseconds):
    root.after(milliseconds, root.quit)
    root.mainloop()

#MAIN_MENU==============================================================================================================
class Main_Menu_Class:
    def __init__(self):
        main_menu.pack()

        main_title = Label(main_menu, text='Benchmark Tests', font='System 50', fg=yellow, bg=grey)
        main_title.grid(row=0, columnspan=2, padx=20, pady=(20, 0))

        subtitle = Label(main_menu, text='By Hardhik Vittanala', font='System 20', fg=yellow, bg=grey)
        subtitle.grid(row=1, columnspan=2, padx=20, pady=(0, 20))

        self.reaction = Reaction_Game_Class()
        self.clicks = Clicks_Class()
        self.visual = Visual_Memory_Class()
        self.number = Number_Memory_Class()
        self.chimp = Chimp_Test_Class()

        for i in range(6):
            menu_button = Button(main_menu, text=' '.join(self.frame_comms[i].__name__.split('_')[1:]).title(), command=self.frame_comms[i], font='System 30', fg=yellow, bg=grey, width=15, height=2)
            menu_button.grid(row=(i // 2) + 2, column=i % 2)
            #TITLES(FOR ALL FRAMES)
            title = Label(frames[i], text=' '.join(self.frame_comms[i].__name__.split('_')[1:]).title(),font='System 50', fg=yellow, bg=grey)
            title.grid(row=0, columnspan=2)
            #BACK BUTTONS(FOR ALL FRAMES)
            back_button = Button(frames[i], text='🔙', font='System 30', fg=yellow, bg=grey, command=self.go_main_menu)
            back_button.place(width=70, height=70)

    def go_main_menu(self):
        root.title('Benchmark Tests')
        for frame in frames:
            frame.pack_forget()
        main_menu.pack()
        #REACTION
        self.reaction.box.config(text='Click Anywhere\nTo Start', bg='#1f4480')
        try:
            root.after_cancel(self.reaction.wait)
        except:
            pass
        #CLICKS
        self.clicks.clicker.config(text='Choose a time', state='disabled', bg='#1f4480')
        for time_button in self.clicks.time_buttons:
            self.clicks.time_button.config(bg='#857b7a', state='normal')
        #VISUAL MEMORY
        self.visual.vis_grid_frame.grid_forget()
        self.visual.start.grid(row=1, column=0, columnspan=2)
        self.visual.level = 0
        #NUMBER MEMORY
        self.number.digits = 0
        self.number.rand_num = ''
        try:
            root.after_cancel(self.number.counter)
        except:
            pass
        self.number.num_game_timer.grid_forget()
        self.number.num_game_enter.grid_forget()
        self.number.guess_frame.grid_forget()
        self.number.num_entry.delete(0, END)
        self.number.num_start.grid(row=1, column=0, columnspan=2)
        #CHIMP TEST
        self.chimp.restart()


    def go_reaction():
        root.title('Reaction Time')
        main_menu.pack_forget()
        reaction.pack()

    def go_clicks():
        root.title('CPS Test')
        main_menu.pack_forget()
        clicks.pack()

    def go_visual_memory():
        root.title('Visual Memory')
        main_menu.pack_forget()
        visual_memory.pack()

    def go_number_memory():
        root.title('Number Memory')
        main_menu.pack_forget()
        number_memory.pack()

    def go_chimp_test():
        root.title('Chimp Test')
        main_menu.pack_forget()
        chimp_test.pack()

    def go_verbal_test():
        root.title('Verbal Test')
        main_menu.pack_forget()
        verbal_test.pack()

    frame_comms = [go_reaction, go_clicks, go_visual_memory, go_number_memory, go_chimp_test, go_verbal_test]


#REACTION===============================================================================================================
class Reaction_Game_Class:
    def __init__(self):
        self.box = Label(reaction, text='Click Anywhere\nTo Start', font='System 50', fg=yellow, bg='#1f4480', width=14,
                         height=7)
        self.box.grid(row=1)
        self.box.bind('<Button-1>', self.get_react_time)

    def turn_green(self):
        self.box.config(bg='#06991a', text='Click!')
        self.time_now = round(ti.time() * 1000)

    def get_react_time(self, *args):
        if self.box.cget('bg') == '#1f4480':
            self.box.config(text='Wait for\ngreen...', bg='#cf4848')
            rand_wait = random.randint(1000, 5000)
            self.wait = root.after(rand_wait, self.turn_green)
        elif self.box.cget('text') == 'Wait for\ngreen...':
            root.after_cancel(self.wait)
            self.box.config(text='Too Soon!', bg='#1f4480')
        else:
            self.box.config(text=str(round(ti.time() * 1000) - self.time_now) + ' ms\nClick To Continue', bg='#1f4480')

#CLICKS=================================================================================================================
class Clicks_Class:
    def __init__(self):
        self.time_buttons = []
        self.no_clicks = 0
        self.clicker = Button(clicks, text='Choose a time', font='System 40', fg=yellow, bg='#1f4480', width=14, height=7, disabledforeground=yellow, state='disabled')
        self.clicker.grid(row=1, column=0)

        self.times = [1, 2, 5, 10, 15, 30, 60, 100]

        self.times_frame = Frame(clicks)
        self.times_frame.grid(row=1, column=1, padx=10)

        for index, time in enumerate(self.times):
            self.time_button = Button(self.times_frame, disabledforeground=yellow, command=lambda time=time, index=index: self.change_time(time, index), bg='#857b7a', text=str(time) + ' Second Test', font='System 17', fg=yellow, width=14)
            self.time_button.grid(row=index)
            self.time_buttons.append(self.time_button)

    def get_cps(self, time):
        self.clicker.config(text=f'You got\n{format(self.no_clicks/time, ".2f")} cps', bg='#1f4480', state='disabled')
        self.no_clicks = 0

    def click_reaction(self, time):
        if self.clicker.cget('text') == 'Click!':
            self.no_clicks += 1
        elif self.clicker.cget('text') == 'Click To Start':
            self.no_clicks += 1
            self.clicker.config(text='Click!', bg='#cf4848')
            self.timer = root.after(time*1000, lambda: self.get_cps(time))

    def change_time(self, time, index):
        self.no_clicks = 0
        if self.clicker.cget('text') == 'Click!':
            root.after_cancel(self.timer)
        for time_button in self.time_buttons:
            time_button.config(bg='#857b7a')
        self.time_buttons[index].config(bg='#1f4480')
        self.clicker.config(text='Click To Start', command=lambda: self.click_reaction(time), state='normal', bg='#1f4480')

#VISUAL MEMORY==========================================================================================================
class Visual_Memory_Class:
    def __init__(self):
        self.cells = []
        self.random_group = []
        self.level = 0
        self.lives = 3
        self.guesses = 0
        self.vis_grid_frame = Frame(visual_memory)

        self.level_display = Label(visual_memory, text=f'  Level: {self.level}', font='System 30', fg=yellow, bg=grey)
        self.lives_display = Label(visual_memory, text=f'Lives: {self.lives}  ', font='System 30', fg=yellow, bg=grey)

        self.start = Button(visual_memory, text='Start', font='System 50', fg=yellow, bg='#857b7a', width=16, height=8, command=lambda: self.create_grid(3, 3))
        self.start.grid(row=1, column=0, columnspan=2)

    def click(self, cellno):
        if self.cells[cellno] in self.random_group:
            if self.cells[cellno].cget('bg') != 'white':
                self.cells[cellno].config(bg='white')
                self.guesses += 1
            if self.guesses == len(self.random_group):
                for cell in self.cells:
                    cell.config(bg='#1f4480')
                self.give_output()
        else:
            self.lives -= 1
            self.lives_display.config(text=f'Lives: {self.lives}  ')
            self.cells[cellno].config(bg='#cf4848', state='disabled')
            if self.lives == 0:
                for cell in self.cells:
                    cell.config(bg='#cf4848', state='disabled')
                self.level = 0
                self.lives = 3
                self.guesses = 0
                sleep(3000)
                self.vis_grid_frame.grid_forget()
                self.start.grid(row=1, column=0, columnspan=2)

    def create_grid(self, width:int, height:int):
        self.start.grid_forget()
        for cell in self.cells:
            cell.destroy()
        self.cells = []
        for i in range(width*height):
            cell = Button(self.vis_grid_frame, bg='#1f4480', command=lambda i=i: self.click(i), width=math.floor(90 / width), height=int(45 / width))
            cell.grid(row=(i//width)+1, column=i%width)
            self.cells.append(cell)

        self.level_display.grid(row=1, sticky=W)
        self.lives_display.grid(row=1, column=1, sticky=E)
        self.vis_grid_frame.grid(row=2, columnspan=2)
        if self.level == 0:
            self.lives_display.config(text=f'Lives: {self.lives}  ')
            self.give_output()

    def give_output(self):
        for cell in self.cells:
            cell.config(state='disabled')
        sleep(400)
        self.random_group = []
        self.guesses = 0
        self.level += 1
        self.level_display.config(text=f'  Level: {self.level}')
        if math.floor((len(self.cells)/2)-1) == self.level:
            self.create_grid(int(math.sqrt(len(self.cells))+1), int(math.sqrt(len(self.cells))+1))
        self.random_group = random.sample(self.cells, self.level + 2)
        for cell in self.random_group:
            cell.config(bg='white')
        sleep(1000)
        for cell in self.cells:
            cell.config(bg='#1f4480', state='normal')

#NUMBER MEMORY==========================================================================================================
class Number_Memory_Class:
    def __init__(self):
        self.num_game_timer = Frame(number_memory, bg=grey)
        self.num_game_enter = Frame(number_memory, bg=grey)
        self.guess_frame = Frame(number_memory, bg='#1f4480')
        self.digits = 0
        self.rand_num = ''

        self.num_start = Button(number_memory, text='Start', font='System 50', fg=yellow, bg='#857b7a', width=20, height=4, command=self.start_number)
        self.num_start.grid(row=1, column=0, columnspan=2)

        self.number_display = Label(self.num_game_timer, font='System 30', fg=yellow, bg=grey)
        self.number_display.grid(row=0)

        self.time_left = ttk.Progressbar(self.num_game_timer, orient=HORIZONTAL, maximum=2000, length=400)
        self.time_left.grid(row=1)

        self.memorise_num = Label(self.num_game_timer, text='Memorise the Number!', font='System 20', fg=yellow, bg=grey)
        self.memorise_num.grid()

        self.num_entry = Entry(self.num_game_enter, font='System 30', fg=yellow, bg='#857b7a')
        self.num_entry.grid(row=0, column=0)

        self.num_entry_button = Button(self.num_game_enter, font='System 25', fg=yellow, bg='#857b7a', text='Enter', command=self.check_num)
        self.num_entry_button.grid(row=0, column=1)

        self.rand_num_display = Label(self.guess_frame, text=f'Answer: {self.rand_num}', font='System 40', fg='#cf4848', bg='#1f4480')
        self.rand_num_display.grid(row=0, pady=(160, 0), padx=160)

        self.user_guess_display = Label(self.guess_frame, text=f'Your Guess: {self.num_entry.get()}\n\nClick To Continue', font='System 40', fg='#cf4848', bg='#1f4480')
        self.user_guess_display.grid(row=1, pady=(0, 160), padx=160)

        self.guess_frame.bind('<Button-1>', self.start_number)
        self.rand_num_display.bind('<Button-1>', self.start_number)
        self.user_guess_display.bind('<Button-1>', self.start_number)

    def check_num(self, x=0):
        if self.num_entry.get() == self.rand_num:
            self.digits += 1
            self.user_guess_display.config(text=f'Your Guess: {self.num_entry.get()}\n\nCorrect!\nClick To Continue', fg='light green')
            self.rand_num_display.config(text=f'Digits Memorised: {self.digits}\nAnswer: {self.rand_num}', fg='light green')
        else:
            self.digits = 0
            self.user_guess_display.config(text=f'Your Guess: {self.num_entry.get()}\n\nIncorrect!\nClick To Play Again', fg='#cf4848')
            self.rand_num_display.config(text=f'Digits Memorised: {self.digits}\nAnswer: {self.rand_num}', fg='#cf4848')

        self.num_game_enter.grid_forget()
        self.guess_frame.grid(row=1, columnspan=2)
        self.num_entry.delete(0, END)

    def start_number(self, x=0):
        self.time_left.config(value=((self.digits+1)*1000)+1000, maximum=((self.digits+1)*1000)+1000)
        self.num_start.grid_forget()
        self.guess_frame.grid_forget()
        self.num_game_timer.grid(row=1, columnspan=2, pady=(25, 50), padx=150)
        self.rand_num = ''
        for i in range(self.digits+1):
            self.rand_num += str(random.randint(1,9))
        self.number_display.config(text=self.rand_num)
        self.count_down()

    def count_down(self):
        self.time_left.step(-1)
        if self.time_left.cget('value') == 0:
            self.num_entry.delete(0, END)
            self.num_game_timer.grid_forget()
            self.num_game_enter.grid(row=1, columnspan=2, pady=(25, 50), padx=60)
        else:
            self.counter = root.after(1, self.count_down)

#CHIMP TEST==========================================================================================================
class Chimp_Test_Class:
    def __init__(self):
        self.level = 1
        self.guessno = 1
        self.lives = 3
        self.buttons = []
        self.border_buttons = []

        self.buttons_frame = Frame(chimp_test, bg='#1f4480')

        self.fail_frame = Frame(chimp_test, bg='#cf4848')
        self.fail_msg = Label(self.fail_frame, font='System 30', fg=yellow, bg='#cf4848')
        self.fail_msg.grid(pady=60, padx=60)
        self.fail_frame.bind('<Button-1>', self.restart)
        self.fail_msg.bind('<Button-1>', self.restart)

        self.start = Button(chimp_test, text='Start', font='System 50', fg=yellow, bg='#857b7a', width=16, height=8, command=self.create_grid)
        self.start.grid(row=1, columnspan=2)

        self.level_display = Label(chimp_test, text=f'  Level: {self.level}', font='System 30', fg=yellow, bg=grey)
        self.lives_display = Label(chimp_test, text=f'Lives: {self.lives}  ', font='System 30', fg=yellow, bg=grey)

    def restart(self, *args):
        self.fail_frame.grid_forget()
        self.guessno = 1
        self.level = 1
        self.lives = 3
        self.level_display.grid_forget()
        self.lives_display.grid_forget()
        self.level_display['text'] = f'  Level: {self.level}'
        self.lives_display['text'] = f'Lives: {self.lives}  '
        self.buttons_frame.grid_forget()
        self.start.grid(row=1, columnspan=2)
        for widgets in self.buttons_frame.winfo_children():
            widgets.destroy()
        self.buttons = []
        self.border_buttons = []

    def create_grid(self):
        for button in self.buttons:
            button.destroy()
        self.buttons = []
        if self.level == 1:
            self.start.grid_forget()
            self.level_display.grid(row=1, sticky=W)
            self.lives_display.grid(row=1, column=1, sticky=E)
            self.buttons_frame.grid(row=2, columnspan=2)

        #CREATE BORDER SO BUTTONS ALIGN
        for i in range(70):
            if i//10 == 0 or i//10 == 6 or i%10 == 0 or i%10 == 9:
                border_button = Button(self.buttons_frame, font='System 20', bg='#00AFA6', width=4, height=2, state='disabled', text='‎')
#                                                                                                                                Invisible Character^^^
                border_button.grid(row=i//10, column=i%10)
                self.border_buttons.append(border_button)

        #MAIN GRID
        for i, letter in enumerate(''.join(random.sample(('l'*(40-(self.level+3))) + ('b'*(self.level+3)), 40))):
            if letter == 'b':
                button = Button(self.buttons_frame, font='System 20', fg=yellow, bg='#857b7a', width=4, height=2)
                button.grid(row=(i//8)+1, column=(i%8)+1)
                self.buttons.append(button)

        random.shuffle(self.buttons)
        for i, button in enumerate(self.buttons):
            button.config(text=i+1, command=lambda i=i: self.click(i+1))

    def click(self, number):
        if number == 1:
            for button in self.buttons:
                button.config(text='', bg='white')
        elif number != self.guessno and self.guessno == 1:
            return
        if number == self.guessno:
            self.buttons[number-1].destroy()
            self.guessno += 1
            if self.level+3 == self.guessno-1:
                self.guessno = 1
                self.level += 1
                self.level_display.config(text=f'  Level: {self.level}')
                self.create_grid()
        else:
            self.lives -= 1
            self.fail_msg['text'] = f'You lost all your lives!\nYou got up to Level {self.level}.\n\nClick to continue'
            if self.lives == 0:
                self.lives_display.grid_forget()
                self.level_display.grid_forget()
                self.buttons_frame.grid_forget()
                self.fail_frame.grid(row=1, columnspan=2)
            else:
                self.lives_display.config(text=f'Lives: {self.lives}  ')
                for button in self.border_buttons:
                    button.config(bg='#cf4848')
                sleep(200)
                for button in self.border_buttons:
                    button.config(bg='#00AFA6')

#BOTTOM OF CODE=========================================================================================================
main_menu_thing = Main_Menu_Class()
root.mainloop()