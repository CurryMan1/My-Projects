#tkinter
from tkinter import ttk
import tkinter as tk
#other
from utils import *


#frames
class StartFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #title
        tk.Label(self, text='Quizzer', font=FONT, bg=secondary_bg, fg=fg).grid(padx=20, pady=10)

        #practise button
        tk.Button(self, text='Practise', font=FONT, width=15, bg=primary_bg, fg=fg,
                  command=lambda: q.change_frame(StartFrame, OptionMenuFrame, QuizFrame)).grid(row=1, padx=20, pady=10)

        #edit questions button
        tk.Button(self, text='Questions', font=FONT, width=15, bg=primary_bg, fg=fg,
                  command=lambda: q.change_frame(StartFrame, EditingFrame)).grid(row=2, padx=20, pady=10)

        #options button
        tk.Button(self, text='Options', font=FONT, width=15, bg=primary_bg, fg=fg,
                  command=lambda: q.change_frame(StartFrame, OptionsFrame)).grid(row=3, padx=20, pady=10)

        #pack
        self.pack()

class OptionMenuFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #title
        tk.Label(self, text='Select:', font=FONT, bg=secondary_bg, fg=fg).grid(padx=20, pady=10)

        #stringvar
        self.choice = tk.StringVar()
        self.choice.set(list(questions.keys())[0])

        #optionmenu
        self.option_menu = tk.OptionMenu(self, self.choice, *questions.keys())
        self.option_menu.config(font=FONT, bg=primary_bg, fg=fg)
        self.option_menu.grid(row=1, pady=(10, 0))

        #choice button
        self.choice_btn = tk.Button(self, text='Select', font=FONT, width=15, bg=primary_bg,
                                    fg=fg, command=lambda: q.change_frame(OptionMenuFrame))
        self.choice_btn.grid(row=2, padx=20, pady=10)

    def update(self, values):
        #clear option menu
        self.option_menu['menu'].delete(0, 'end')

        #add new label
        for value in values:
            self.option_menu['menu'].add_command(label=value)

    def get(self):
        return self.choice.get()

class EditingFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #title
        tk.Label(self, text='Manage Set', font=FONT, bg=secondary_bg, fg=fg).grid(padx=20, pady=10)

        #edit question button
        tk.Button(self, text='Edit Question', font=FONT, bg=primary_bg, width=15, fg=fg,
                  command=lambda: q.change_frame(EditingFrame, OptionMenuFrame, EditingFrame)
                  ).grid(row=1, column=0, padx=20, pady=10)

        #add question button


        #delete question button


class EntryFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.question_entry = ''


class OptionsFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class QuizFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Quizzer(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Quizzer')
        self.resizable(False, False)

        self.next_frame = None

        #frames
        self.frames = {}

        start_frame = StartFrame(self, bg=secondary_bg)
        self.frames[StartFrame] = start_frame

        choose_set_frame = OptionMenuFrame(self, bg=secondary_bg)
        self.frames[OptionMenuFrame] = choose_set_frame

        editing_frame = EditingFrame(self, bg=secondary_bg)
        self.frames[EditingFrame] = editing_frame

        options_frame = OptionsFrame(self, bg=secondary_bg)
        self.frames[OptionsFrame] = options_frame

        quiz_frame = QuizFrame(self, bg=secondary_bg)
        self.frames[QuizFrame] = quiz_frame

    def change_frame(self, start, destination=None, final=None):
        #unpack start frame
        self.frames[start].pack_forget()
        if destination:
            #pack dest frame
            self.frames[destination].pack()
        else:
            #this mean func must be called from OptionMenuFrame
            self.frames[self.next_frame].pack()

        if final:
            self.next_frame = final


if __name__ == '__main__':
    q = Quizzer()
    q.mainloop()
