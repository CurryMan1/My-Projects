from tkinter import *

root = Tk()
root.title('To Do List')
root.resizable(False, False)

items_file = 'items.txt'

stored_item = ''

times_run = 0

def close_win(x):
    global times_run
    print(items[box.curselection()[0]])
    temp = 0
    temp2 = ''
    if x == 1:
        temp = items[box.curselection()[0]].replace('\n', '').replace('-', '') + '\n'
        temp2 = items[box.curselection()[0]].replace('\n', '').replace('-', '') + '\n'
        items.remove(temp)
        print(temp)
        box.delete(box.curselection()[0])
        with open(items_file, 'w') as file:
            for line in items:
                file.write(line)
    try:
        window.destroy()
    except:
        print('Error Log: You pressed delete item or add item')
    try:
        box.insert(len(items) + 1, enter.get())
        items.append(enter.get()+'\n')
        with open(items_file, 'w') as file:
            for line in items:
                if line == items[-1]:
                    file.write(line+'\n')
                else:
                    file.write(line)
        window1.destroy()
    except:
        print('Error Log: You pressed delete item')
    delete_item.configure(state='disabled')
    times_run += 1

def add_an_item():
    global window1, enter, times_run
    times_run = 0
    window1 = Toplevel(root)
    window1.title('Add Item')
    window1.attributes("-topmost", True)
    enter = Entry(window1, font='helvetica 30 bold', bg='#0FA9A1', width=23)
    enter.grid(row=0, column=0, padx=(20, 0), pady=20)
    enterr = Button(window1, text='✔', command=lambda: close_win(0), width=5, font='helvetica 30 bold', fg='dark green', bg='#0FA9A1')
    enterr.grid(row=0, column=1, padx=(0, 20), pady=20)

def reset():
    global stored_item
    stored_item = ''

def config_item(q):
    global stored_item, window
    delete_item.configure(state='normal')
    print(stored_item)
    print(box.curselection())
    if box.curselection() == stored_item:
        try:
            window.destroy()
        except:
            print("Error Log: Confirmation window doesn't exist (yet)")
        window = Toplevel(root)
        window.title('Confirm')
        window.attributes("-topmost", True)
        counter = 0
        prev_letter = ' '
        x = ''
        for letter in items[stored_item[0]].replace('\n', ''):
            counter += 1
            x += letter
            if counter > 50:
                x += '\n'
                counter = 0
        sure = Label(window, text=f'Delete\n\n"{x}"\n\nfrom to-do list?', font=('font2', 20))
        sure.grid(row=0, columnspan=2, pady=(15,0), padx=15)
        no = Button(window, text='❌', command=lambda: close_win(0), font=('font2', 30), fg='red',bg='#0FA9A1')
        no.grid(row=1, column=1, pady=(0, 15), padx=(3, 15))
        yes = Button(window, text='✔', command=lambda: close_win(1), font=('font2', 30), fg='dark green', bg='#0FA9A1')
        yes.grid(row=1, column=0, pady=(0,15), padx=(15,3))
    else:
        print('yo why arent i here yet??')
        stored_item = box.curselection()
        print(stored_item)
        print(box.curselection())
        root.after(500, reset)

box = Listbox(root, font='helvetica 30 bold', width=20, height=10)
box.grid(columnspan=2)
with open(items_file, 'r') as file:
    items = file.readlines()
    x = ''
    mycounter = 0
    for line in items:
        for letter in line.strip():
            mycounter += 1
            x += letter
            if mycounter > 80:
                if letter != ' ' and prev_letter != ' ':
                    x += '-'
                x += '\n'
                mycounter = 0
                prev_letter = letter
        box.insert(END, x)
        x = ''
        mycounter = 0

#MAKE OTHER WIDGETS:::::::::::::::::::::::::::::::::::::::::::::::::::::::
add_item = Button(root, text='Add Item', command=add_an_item, font=('font2', 40), bg='#0FA9A1')
add_item.grid(row=1, column=0, sticky=E)

delete_item = Button(root, text='Delete Item', command=lambda: close_win(1), font=('font2', 40), bg='#0FA9A1', state='disabled')
delete_item.grid(row=1, column=1, sticky=W)

box.bind('<Button-1>', config_item)
root.mainloop()