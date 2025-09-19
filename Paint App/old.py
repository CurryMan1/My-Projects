from tkinter import *
from PIL import ImageGrab

root = Tk()
root.title('Hardhik Paint')
#root.iconbitmap('C:/Users/user/Downloads/paint-brush.ico')
root.state('zoomed')
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

canvas = Canvas(root, highlightthickness=5, highlightbackground="black")
canvas.grid(padx=3, sticky='nsew')

buttons_frame = Frame(root, bg='grey')
buttons = []

selected_colour = 'Black'
colours = ['Black', 'Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple', 'Pink', 'Grey', 'White', '#964B00']
pen_down = False

def tksleep(self, time:float) -> None:
    self.after(int(time*1000), self.quit)
    self.mainloop()
Misc.tksleep = tksleep

def make_pen_down(event):
    global pen_down
    pen_down = True
    pen_thickness = thickness.get()

    if pen_down:
        canvas.create_oval(event.x - pen_thickness,
                           event.y - pen_thickness,
                           event.x + pen_thickness,
                           event.y + pen_thickness,
                           fill=selected_colour,
                           outline=selected_colour)

def add_line(event):
    global pen_down

    pen_thickness = thickness.get()

    if pen_down:
        canvas.create_oval(event.x-pen_thickness,
                           event.y-pen_thickness,
                           event.x+pen_thickness,
                           event.y+pen_thickness,
                           fill=selected_colour,
                           outline=selected_colour)

def make_pen_up(event):
    global pen_down
    pen_down = False

def change(colour):
    global selected_colour
    selected_colour = colour

def do_it():
    if entryy.get() == '' or entryy.get().isspace():
        Label(namefile, text='Invalid File Name', fg='red').grid()
        return None
    qq = entryy.get()
    namefile.destroy()
    root.tksleep(0.7)
    x = root.winfo_rootx() + canvas.winfo_x()
    y = root.winfo_rooty() + canvas.winfo_y()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()
    ImageGrab.grab().crop((x, y, x1, y1)).save(f"C:/Users/user/PycharmProjects/Paint App/{qq}.jpg")

def save(event):
    global namefile, entryy
    if clicked.get() == 'Save':
        namefile = Toplevel(root)
        #namefile.iconbitmap('C:/Users/user/Downloads/paint-brush.ico')
        namefile.title('Save File')
        entryy = Entry(namefile)
        entryy.grid(padx=30, pady=(30,0))
        enterrr = Button(namefile, text='Enter File Name', command=do_it)
        enterrr.grid(padx=30, pady=(0,30))
    else:
        canvas.delete('all')
    clicked.set('Options')

lis = ['Save', 'Clear']

clicked = StringVar()
clicked.set('Options')

options = OptionMenu(buttons_frame, clicked, *lis, command=save)
options.grid(column=0, row=0)

for colour in colours:
    button = Button(buttons_frame, width=10, text='', bg=colour, fg=colours[-colours.index(colour)+1], command=lambda colour=colour:change(colour))
    button.grid(row=0, column=colours.index(colour)+1)
    buttons.append(button)

Label(buttons_frame, text='Pen Thickness', bg='grey').grid(columnspan=12)
thickness = Scale(buttons_frame, from_=1, to=250, bg='grey', orient=HORIZONTAL, length=950)
thickness.grid(columnspan=12)

canvas.bind('<Button-1>', make_pen_down)
canvas.bind('<B1-Motion>', add_line)
canvas.bind('<ButtonRelease-1>', make_pen_up)

buttons_frame.grid(row=1, column=0)
root.mainloop()