from customtkinter import *
from PIL import ImageGrab

root = CTk()
root.title('Paint')
root.state('zoomed')
root.iconbitmap('C:/Users/user/Downloads/paint-brush.ico')
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

canvas = CTkCanvas(root, highlightthickness=5, highlightbackground="black")
canvas.grid(padx=3, sticky='nsew')

buttons_frame = CTkFrame(root, fg_color='light blue')
buttons = []

selected_colour = 'Black'
colours = ['Black', 'Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple', 'Pink', 'Grey', 'White', '#964B00']
current_x, current_y = 0, 0


def locate_xy(event):
    global current_x, current_y
    current_x, current_y = event.x, event.y


def addLine(event):
    global current_x, current_y
    canvas.create_line(current_x, current_y, event.x, event.y, fill=selected_colour, width=thickness.get())
    current_x, current_y = event.x, event.y


def change(colour):
    global selected_colour
    selected_colour = colour


def idk():
    x = root.winfo_rootx() + canvas.winfo_x()
    y = root.winfo_rooty() + canvas.winfo_y()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()
    ImageGrab.grab().crop((x, y, x1, y1)).save(f"C:/Users/user/PycharmProjects/Paint App/{qq}.jpg")


def do_it():
    global qq
    if entryy.get() == '' or entryy.get().isspace():
        CTkLabel(namefile, text='Invalid File Name', fg_color='red').grid()
        return None
    qq = entryy.get()
    namefile.destroy()
    root.after(700, idk)


def save(event):
    global namefile, entryy
    if options.get() == 'Save':
        namefile = CTkToplevel(root)
        namefile.iconbitmap('C:/Users/user/Downloads/paint-brush.ico')
        namefile.title('Save File')
        entryy = CTkEntry(namefile)
        entryy.grid(padx=30, pady=(30, 0))
        enterrr = CTkButton(namefile, text='Enter File Name', command=do_it)
        enterrr.grid(padx=30, pady=(0, 30))
    else:
        canvas.delete('all')
    options.set('Options')


lis = ['Save', 'Clear']

options = CTkOptionMenu(buttons_frame, values=lis, command=save)
options.grid(column=0, row=0)
options.set('Options')

for colour in colours:
    button = CTkButton(buttons_frame, width=50, text='', fg_color=colour,
                       text_color=colours[-colours.index(colour) + 1], command=lambda colour=colour: change(colour))
    button.grid(row=0, column=colours.index(colour) + 1)
    buttons.append(button)

CTkLabel(buttons_frame, text_color='black', text='Pen Thickness', fg_color='light blue').grid(columnspan=12)
thickness = CTkSlider(buttons_frame, from_=0, to=250, fg_color='grey', width=500, orientation=HORIZONTAL)
thickness.grid(columnspan=12)

canvas.bind('<Button-1>', locate_xy)
canvas.bind('<B1-Motion>', addLine)

buttons_frame.grid(row=1, column=0)
root.mainloop()