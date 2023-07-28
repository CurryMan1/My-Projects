from tkinter import *
from tkinter import ttk
from datetime import datetime
from PIL import Image, ImageTk

'''
This is a clock app.
There may be random errors throughout the program; ignore them.
They are just after_cancel(self, id) errors.
The errors happen because {id} isn't defined yet
'''

#TKINTER----------------------------------------------------------------------------------------------------------------
root = Tk()
root.title('Clock')
root.resizable(False, False)
root.config(bg='black')

Clock = Frame(root, bg='black')
Timer = Frame(root, bg='black', width=700, height=800)
Stopwatch = Frame(root, bg='black')

mini_apps = [Clock, Timer, Stopwatch]
buttons = []

#BUTTONS----------------------------------------------------------------------------------------------------------------
def change(btn_idx, des_frame):
    for i, miniapp in enumerate(mini_apps):
        buttons[i].config(bg='black', state='normal')
        miniapp.grid_remove()
    des_frame.grid(columnspan=3)
    buttons[btn_idx].config(bg='white', state='disabled')

for i, frame in enumerate(mini_apps):
    button = Button(root,
                    text=[w for w, j in locals().items() if j == frame][0],
                    font='Helvetica 40 bold', bg=['white', 'black'][-(i//-3)],
                    fg='#9C7A00',
                    command=lambda i=i, frame=frame: change(i, frame),
                    state=['disabled', 'normal'][-(i//-3)],
                    disabledforeground='#9C7A00')
    button.grid(row=0, column=i)
    buttons.append(button)

#CLOCK------------------------------------------------------------------------------------------------------------------
def update():
    digclock.config(text=datetime.now().strftime("%H:%M:%S"))
    root.after(1000, update)

digclock = Label(Clock, text=datetime.now().strftime("%H:%M:%S"), font='Helvetica 100 bold', bg='black', fg='#9C7A00')
digclock.grid(row=1)

#TIMER------------------------------------------------------------------------------------------------------------------
def validate_min_secs(P):
    return ((len(P) < 3 and P.isdigit() and (int(P) < 60)) or len(P) == 0)

def validate_hours(P):
    return ((len(P) < 3 and P.isdigit()) or len(P) == 0)

def update_timer(timer, values, visual_timer, wait=False):
    global repeat
    if values[2] == 0:
        values[2] = 59
        values[1] -= 1
        if values[1] == -1:
            values[1] = 59
            values[0] -= 1
            if values[0] == -1:
                return 'END TIMER'
    else:
        values[2] -= 1

    formatted_times = [f"{values[0]:02}", f"{values[1]:02}", f"{values[2]:02}"]
    timer.config(text=':'.join(formatted_times))
    if wait == False:
        visual_timer.step(-1)
    else:
        wait = False
    repeat = root.after(1000, lambda: update_timer(timer, values, visual_timer))

def pause_play(button, time_dis, sending_list, visual_timer):
    global repeat, x
    if button.cget('text') == '⏸️':
        try:
            root.after_cancel(repeat)
        except:
            pass
        try:
            root.after_cancel(x)
        except:
            pass #only used try except bc otherwise rest of code wouldn't run
        button.config(text='▶️')
    else:
        button.config(text='⏸️')
        x = root.after(1000, lambda: update_timer(time_dis, sending_list, visual_timer))

def restart_timer(pause, timer, values, progressbar):
    global repeat
    root.after_cancel(repeat)
    seconds = progressbar.cget('maximum')
    values = [seconds//3600, (seconds%3600)//60, (seconds%3600)%60+1]
    progressbar.config(value=seconds)
    pause.config(text='⏸️')
    update_timer(timer, values, progressbar, True)


def start_timer(timer):
    global var
    if timer.winfo_children()[2].get() and timer.winfo_children()[4].get() and timer.winfo_children()[6].get():
        times = [f"{int(timer.winfo_children()[2].get()):02}", f"{int(timer.winfo_children()[4].get()):02}", f"{int(timer.winfo_children()[6].get()):02}"]
        if sum([int(time) for time in times]) > 0:
            for widgets in timer.winfo_children()[2:]:
                widgets.destroy()

            time_dis = Label(timer, text=f"{times[0]}:{times[1]}:{times[2]}", font='Helvetica 50 bold', bg='black', fg='white')
            time_dis.grid(row=1, column=0, pady=(20,0), padx=(35,0))

            sending_list = [int(time) if i != 2 else int(time)+1 for i, time in enumerate(times)]

            mystyle = ttk.Style()
            mystyle.theme_use('clam')
            mystyle.configure("bar.Horizontal.TProgressbar", troughcolor='white', bordercolor='white', background='#9C7A00')

            visual_timer = ttk.Progressbar(timer, style="bar.Horizontal.TProgressbar",
                                           value=(sending_list[0]*60*60)+(sending_list[1]*60)+(sending_list[2])-1,
                                           maximum=(sending_list[0]*60*60)+(sending_list[1]*60)+(sending_list[2])-1,
                                           length=270)
            visual_timer.grid(row=2, columnspan=2, padx=(35,0))

            pause = Button(timer, text='⏸️', command=lambda: pause_play(pause, time_dis, sending_list, visual_timer), font='Helvetica 37 bold', bg='black', fg='white')
            pause.grid(row=3, sticky=W, padx=(37, 0))

            restart = Button(timer, text='↻', command=lambda: restart_timer(pause, time_dis, sending_list, visual_timer), font='Helvetica 37 bold', bg='black', fg='white', width=3)
            restart.grid(row=3, sticky=E)

            update_timer(time_dis, sending_list, visual_timer, True)

def delete_timer(timer, spot):
    global available_spots
    for widgets in timer.winfo_children():
        widgets.destroy()
    timer.destroy()
    new_timer_button.config(state='normal')
    available_spots.append(spot)
    available_spots.sort()
def new_timer():
    global available_spots
    new_timer_frame = Frame(Timer, width=350, height=350, bg='black', highlightbackground="#9C7A00", highlightthickness=5)

    title = Label(new_timer_frame, text=f'Timer {str(available_spots[0] + 1)}', font='Helvetica 35 bold', bg='black', fg='#9C7A00')
    title.grid(row=0, columnspan=5, sticky=W, padx=(40, 0), pady=(15, 0))

    del_timer = Button(new_timer_frame, font='Helvetica 30 bold', text='X', command=lambda: delete_timer(new_timer_frame, int(title.cget('text')[-1]) - 1), bg='black', fg='#9C7A00', width=3)
    del_timer.place(relx=1, rely=0, anchor=NE)

    hours = Entry(new_timer_frame, font='Helvetica 50 bold', width=2, validatecommand=(root.register(validate_hours), '%P'), validate='key')
    hours.grid(row=1, column=0, pady=(20,0), padx=(24,0))

    Label(new_timer_frame, font='Helvetica 50 bold', text=':', bg='black', fg='white').grid(row=1, column=1, pady=(20, 0))

    mins = Entry(new_timer_frame, font='Helvetica 50 bold', width=2, validatecommand=(root.register(validate_min_secs), '%P'), validate='key')
    mins.grid(row=1, column=2, pady=(20,0))

    Label(new_timer_frame, font='Helvetica 50 bold', text=':', bg='black', fg='white').grid(row=1, column=3, pady=(20, 0))

    secs = Entry(new_timer_frame, font='Helvetica 50 bold', width=2, validatecommand=(root.register(validate_min_secs), '%P'), validate='key')
    secs.grid(row=1, column=4, pady=(20,0))

    start_time = Button(new_timer_frame, font='Helvetica 35 bold', text='Start Timer', command=lambda: start_timer(new_timer_frame), bg='black', fg='#9C7A00')
    start_time.grid(row=2, columnspan=5, padx=(24, 0), pady=20)

    new_timer_frame.grid_propagate(0)
    new_timer_frame.place(x=350 * (available_spots[0] % 2), y=350 * (available_spots[0] // 2))

    available_spots.remove(available_spots[0])
    if len(available_spots) == 0:
        new_timer_button.config(state='disabled')

plus = Image.open('plus.jpg').resize((110, 110))
tkplus = ImageTk.PhotoImage(plus)
new_timer_button = Button(Timer, image=tkplus, height=100, width=100, command=new_timer, bg='black')
new_timer_button.place(relx=1, rely=1, anchor=SE)
available_spots = [0, 1, 2, 3]

#END--------------------------------------------------------------------------------------------------------------------
root.after(round((1000000-int(str(datetime.now()).split('.')[1]))/1000), update)
Clock.grid(columnspan=3)
root.mainloop()