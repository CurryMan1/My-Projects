from tkinter import *
import re

calc = Tk()
calc.title('Calculator')
calc.iconbitmap('C:/Users/user/Downloads/171352_calculator_icon.ico')
calc.config(bg='black')

operators = ['/', '*', '-', '+']

def clear():
    top.config(text='')
    type_space.config(text='')

def c_e():
    try:
        if top.cget('text')[-1] != '=':
            type_space.config(text=type_space.cget('text')[:-1])
    except:
        pass

def function(given_operator):
    if top.cget('text') == '' or type_space.cget('text')[-1] not in operators:
        try:
            if top.cget('text')[-1] == '=':
                top.config(text=type_space.cget('text'))
            else:
                top.config(text=top.cget('text') + type_space.cget('text'))
        except:
            top.config(text=top.cget('text') + type_space.cget('text'))

        type_space.config(text=given_operator)

def negative():
    if type_space.cget('text')[0] == '-':
        type_space.config(text=type_space.cget('text')[1:])
    elif type_space.cget('text')[1] == '-':
        type_space.config(text=type_space.cget('text')[0] + type_space.cget('text')[2:])
    elif type_space.cget('text')[0] in operators:
        type_space.config(text=type_space.cget('text')[0] + '-' + type_space.cget('text')[1:])
    else:
        type_space.config(text = '-' + type_space.cget('text'))
def insert_num(thing):
    if len(type_space.cget('text')) % 8 == 0 and len(type_space.cget('text')) != 0:
        type_space.config(text=type_space.cget('text') + '\n')
    try:
        if top.cget('text')[-1] not in ['1','2','3','4','5','6','7','8','9','0']:
            top.config(text='')
            type_space.config(text='')
    except:
        pass
    type_space.config(text=type_space.cget('text')+thing)


def equals():
    top.config(text=top.cget('text') + type_space.cget('text'))
    for number in re.split(r'\D', top.cget('text')):
        if number == '':
            pass
        elif number[0] == '0' and number.count(number[0]) == len(number):
            top.config(text=top.cget('text').replace(number, '0'))
        else:
            top.config(text=top.cget('text').replace(number, number.lstrip('0')))

    top.config(text=top.cget('text') + '=')
    try:
        type_space.config(text=str(eval(top.cget('text')[:-1].replace('\n', ''))))
    except:
        top.config(text='Syntax')
        type_space.config(text='ERROR')

top = Label(calc, font='helvetica 27 bold', text='', bg='black', fg='white')
top.grid(row=0, columnspan=4, sticky=E)

type_space = Label(calc, font='helvetica 67 bold', text='', bg='black', fg='white', anchor=E)
type_space.grid(row=1, columnspan=4, sticky=E)

ac = Button(calc, command=clear, text='AC', font='helvetica 37 bold', bg='white', width=3)
ac.grid(row=2, column=0)

ce = Button(calc, command=c_e, text='CE', font='helvetica 37 bold', width=3)
ce.grid(row=2, column=1)

pos_neg = Button(calc, command=negative, text='±', font='helvetica 37 bold', width=3)
pos_neg.grid(row=2, column=2)

for i, operator in enumerate(operators):
    operator = Button(text=operator, font='helvetica 37 bold', bg='orange', command=lambda operator=operator: function(operator), width=3)
    operator.grid(column=3, row=i + 2)
equals = Button(text='=', font='helvetica 37 bold', bg='orange', width=3, command=equals)
equals.grid(column=3, row=6)

for i in range(9):
    number = Button(text=str(9-i), font='helvetica 37 bold', bg='black', fg='white', command=lambda i=i: insert_num(str(9-i)), width=3)
    number.grid(row=(i//3) + 3, column=2-(i%3))

zero = Button(text='   0      ', font='helvetica 37 bold', bg='black', fg='white', command=lambda: insert_num('0'), anchor=W)
zero.grid(row=6, column=0, columnspan=2)

dec = Button(text='.', font='helvetica 37 bold', bg='black', fg='white', command=lambda: insert_num('.'), width=3)
dec.grid(row=6, column=2)

calc.mainloop()