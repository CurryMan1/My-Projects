#other
from utils import *

#tkinter
from tkinter.scrolledtext import ScrolledText
import tkinter as tk


#reset function
def reset(new_fg, new_bg1, new_bg2):
    global q #global here is unavoidable

    options['fg'] = new_fg
    options['primary_bg'] = new_bg1
    options['secondary_bg'] = new_bg2

    JsonManager.write(options_file, options)

    q.destroy()
    q = Quizzer()
    q.mainloop()


#pop up window
class EntryPopUp(tk.Toplevel):
    def __init__(self, master, bg, closing_command, title, extra=''):
        super().__init__(master, bg=bg, padx=20, pady=20)
        self.title(title)
        self.resizable(False, False)

        #entry
        self.name_entry = tk.Entry(self, bg=options['secondary_bg'], fg=options['fg'], font=FONT, width=15)
        self.name_entry.grid(row=0, padx=20, pady=10)

        #confirm button
        tk.Button(self, text='Enter'+extra, font=FONT, bg=options['primary_bg'], fg=options['fg'], width=15,
                  command=closing_command).grid(padx=20, pady=10)


#frames
class StartFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #pop up window
        self.win = None

        #add set button
        tk.Button(self, text='+', command=self.pop_window,
                  font=FONT, bg=options['primary_bg'], fg=options['fg']).place(x=4, y=4, width=60, height=60)

        #title
        tk.Label(self, text='Quizzer', font=FONT, bg=options['secondary_bg'], fg=options['fg']).grid(padx=20, pady=10)

        #practise button
        tk.Button(self, text='Practise', font=FONT, width=15, bg=options['primary_bg'], fg=options['fg'],
                  command=lambda: q.change_frame(StartFrame, OptionMenuFrame, QuizFrame)).grid(row=1, padx=20, pady=10)

        #edit sets button
        tk.Button(self, text='Edit Sets', font=FONT, width=15, bg=options['primary_bg'], fg=options['fg'],
                  command=self.check_sets).grid(row=2, padx=20, pady=10)

        #preferences button
        tk.Button(self, text='Preferences', font=FONT, width=15, bg=options['primary_bg'], fg=options['fg'],
                  command=lambda: q.change_frame(StartFrame, PreferencesFrame)).grid(row=3, padx=20, pady=(10, 20))

        #pack
        self.pack()

    def pop_window(self):
        if self.win:
            self.win.destroy()
        self.win = EntryPopUp(self, options['secondary_bg'], self.add_set, 'Add Set', ' Set')

    def add_set(self):
        #get text
        set_name = self.win.name_entry.get()
        if set_name != '':
            #add key to json
            sets[set_name] = {
                'questions': {},
                'attempts': 0,
                'correct_guesses': 0
            }

            JsonManager.write(sets_file, sets)

            self.win.destroy()

    def check_sets(self):
        if len(sets.keys()) > 0:
            q.change_frame(StartFrame, OptionMenuFrame, EditingFrame)


class OptionMenuFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #question set
        self.question_set = True

        #back button
        tk.Button(self, text='🔙', command=lambda: q.back(OptionMenuFrame),
                  font=('helvetica', 30), bg=options['primary_bg'], fg=options['fg']).grid(column=0, sticky=tk.W)

        #stringvar
        self.choice = tk.StringVar()
        sets_ = list(sets.keys())
        if sets_:
            self.choice.set(sets_[0])

        #optionmenu
        self.option_menu = tk.OptionMenu(self, self.choice, 'random thing so i dont get an error')
        self.option_menu.config(font=FONT, bg=options['primary_bg'], fg=options['fg'])
        self.option_menu.grid(row=0, column=1, pady=(10, 0), sticky=tk.W)

        #choice button
        self.choice_btn = tk.Button(self, text='Select', font=FONT, width=15, bg=options['primary_bg'],
                                    fg=options['fg'], command=lambda: q.change_frame(OptionMenuFrame))
        self.choice_btn.grid(row=1, padx=20, pady=10, columnspan=2)

    def update_values(self, values, question_set=True):
        #set last (question) set
        self.question_set = question_set

        #clear option menu
        self.option_menu['menu'].delete(0, 'end')

        #add new label
        for value in values:
            self.option_menu['menu'].add_command(label=value, command=tk._setit(self.choice, value))
        self.choice.set(values[0])

    def get(self):
        return self.choice.get()


class EditingFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.click_count = 0  #for delete set button
        self.reset_event = None

        self.deleting = False

        #back button
        tk.Button(self, text='🔙', command=lambda: q.change_frame(EditingFrame, StartFrame),
                  font=('helvetica', 30), bg=options['primary_bg'], fg=options['fg']).grid(row=0, column=0)

        #title
        self.title = tk.Label(self, text='Manage Set', font=FONT, bg=options['secondary_bg'], fg=options['fg'])
        self.title.grid(row=0, column=1, padx=20, pady=10, sticky=tk.W)

        #edit question button
        tk.Button(self, text='Edit Question', font=FONT, bg=options['primary_bg'], width=15, fg=options['fg'],
                  command=lambda: self.select_question('edit')).grid(row=1, column=0, padx=20,
                                                                     pady=10, columnspan=2)

        #add question button
        tk.Button(self, text='Add Question', font=FONT, bg=options['primary_bg'], width=15, fg=options['fg'],
                  command=lambda: q.change_frame(EditingFrame, EntryFrame, EditingFrame)
                  ).grid(row=2, column=0, padx=20, pady=10, columnspan=2)

        #delete question button
        tk.Button(self, text='Delete Question', font=FONT, bg=options['primary_bg'], width=15, fg=options['fg'],
                  command=lambda: self.select_question('delete')).grid(row=3, column=0, padx=20, pady=10, columnspan=2)

        #delete set button
        self.delete_set_button = tk.Button(self, text='Delete Set', font=FONT, bg=options['primary_bg'], width=15,
                                           fg=options['fg'], command=self.delete_set)
        self.delete_set_button.grid(row=4, column=0, padx=20, pady=10, columnspan=2)

    def pack_forget(self):
        super().pack_forget()
        self.reset_set_button()

    def reset_set_button(self):
        self.click_count = 0
        self.delete_set_button.config(text='Delete Set', bg=options['primary_bg'])
        self.after_cancel(self.reset_event)
        self.reset_event = None

    def delete_set(self):
        self.click_count += 1
        if self.click_count == 2:
            last_set = q.last_set
            #delete set
            del sets[last_set]
            #go back to start frame
            q.change_frame(EditingFrame, StartFrame, file_to_update=sets_file)
        else:
            self.reset_event = self.after(3000, self.reset_set_button)
            self.delete_set_button.config(text='Are you sure?', bg='#8B0000')

    def select_question(self, type_):
        #get last sets' questions
        if q.last_set:
            last_sets_questions = list(sets[q.last_set]['questions'].keys())
            if len(last_sets_questions) > 0:
                #update values of OptionMenuFrame
                q.frames[OptionMenuFrame].update_values(last_sets_questions, False)

                if type_ == 'edit':
                    #go to OptionMenuFrame
                    q.change_frame(EditingFrame, OptionMenuFrame, EntryFrame)

                    #set editing in entry frame to true
                    q.frames[EntryFrame].editing = True
                elif type_ == 'delete':
                    #go to OptionMenuFrame
                    q.change_frame(EditingFrame, OptionMenuFrame, EditingFrame)

                    #set deleting
                    self.deleting = True

    def pack(self):
        self.title['text'] = f'Manage {q.last_set}'
        super().pack()


class EntryFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.editing = False
        self.last_question = None

        #back button
        tk.Button(self, text='🔙', command=lambda: q.back(EntryFrame),
                  font=('helvetica', 30), bg=options['primary_bg'], fg=options['fg']).grid(sticky=tk.W)

        #question entry
        self.question_entry = tk.Text(self, font=SMALL_FONT, bg=options['secondary_bg'], fg=options['fg'], width=25, height=3)
        self.question_entry.grid()

        #answer entry
        self.answer_entry = ScrolledText(self, font=SMALL_FONT, bg=options['secondary_bg'], fg=options['fg'], width=25, height=6)
        self.answer_entry.grid()

        #add question button
        tk.Button(self, text='Done', font=FONT, bg=options['primary_bg'], width=15, fg=options['fg'],
                  command=self.add_question).grid()

    def add_question(self):
        #get question and answer
        qa = self.get()
        #check if entries are blank and if the question already exists
        if (qa[0] not in ['', *sets[q.last_set]['questions']] or self.editing) and qa[1] != '':
            #clear
            self.clear_entries()

            if self.editing:
                #delete question
                del sets[q.last_set]['questions'][self.last_question]
                #set editing to false
                self.editing = False

            #add a question and answer to dict
            sets[q.last_set]['questions'][qa[0]] = {'answer': qa[1]}

            #switch frame (and update file)
            q.change_frame(EntryFrame, EditingFrame, file_to_update=sets_file)

    def clear_entries(self):
        self.question_entry.delete('1.0', 'end')
        self.answer_entry.delete('1.0', 'end')

    def set_entries(self, question=None, answer=None):
        if question:
            #clear text widget
            self.question_entry.delete('1.0', 'end')
            #write in text widget
            self.question_entry.insert('1.0', question)

        if answer:
            #clear text widget
            self.answer_entry.delete('1.0', 'end')
            #write in text widget
            self.answer_entry.insert('1.0', answer)

    def get(self) -> list[str, str]:
        #gets both entries' text value
        return [self.question_entry.get("1.0", 'end-1c'), self.answer_entry.get("1.0", 'end-1c')]


class PreferencesFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, padx=20, pady=20)

        #pop up win
        self.win = None
        self.editing_btn = None

        #back button
        tk.Button(self, text='🔙', command=lambda: q.back(PreferencesFrame),
                  font=('helvetica', 30), bg=options['primary_bg'], fg=options['fg']).place(x=-15, y=-15, width=60, height=60)

        #primary_bg label
        tk.Label(self, text='Primary BG', font=FONT, bg=options['secondary_bg'], fg=options['fg']).grid(row=0, column=0)

        #primary_bg button
        self.primary_bg_btn = tk.Button(self, text=options['primary_bg'], font=FONT,
                                        bg=options['primary_bg'], width=8, fg=white_or_black(options['primary_bg']),
                                        command=lambda: self.pop_window(self.primary_bg_btn))
        self.primary_bg_btn.grid(row=0, column=1)

        #secondary_bg label
        tk.Label(self, text='Secondary BG', font=FONT, bg=options['secondary_bg'], fg=options['fg']).grid(row=1, column=0)

        #secondary_bg button
        self.secondary_bg_btn = tk.Button(self, text=options['secondary_bg'], font=FONT, bg=options['secondary_bg'],
                                          width=8, fg=white_or_black(options['secondary_bg']),
                                          command=lambda: self.pop_window(self.secondary_bg_btn))
        self.secondary_bg_btn.grid(row=1, column=1)

        #fg label
        tk.Label(self, text='Foreground', font=FONT, bg=options['secondary_bg'], fg=options['fg']).grid(row=2, column=0)

        #fg btn
        self.fg_btn = tk.Button(self, text=options['fg'], font=FONT, bg=options['fg'], width=8,
                                fg=white_or_black(options['fg']), command=lambda: self.pop_window(self.fg_btn))
        self.fg_btn.grid(row=2, column=1)

        #update button
        tk.Button(self, text='Apply', font=FONT, bg=options['primary_bg'], fg=options['fg'],
                  command=self.update_all).grid(sticky='ew', columnspan=2)

    def update_all(self):
        reset(self.fg_btn['text'], self.primary_bg_btn['text'], self.secondary_bg_btn['text'])

    def pop_window(self, editing_btn):
        if self.win:
            self.win.destroy()

        self.editing_btn = editing_btn
        self.win = EntryPopUp(self, options['secondary_bg'], self.change_button_color, 'Edit Color', ' Hex')

    def change_button_color(self):
        #get hex
        hex_ = self.win.name_entry.get()

        #edit button
        text_col = white_or_black(hex_)
        self.editing_btn.config(text=hex_, fg=text_col, bg=hex_)

        #destroy window
        self.win.destroy()


class QuizFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Quizzer(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Quizzer')
        self.resizable(False, False)

        self.last_frame = None
        self.next_frame = None
        self.last_set = None

        #frames
        self.frames = {}

        start_frame = StartFrame(self, bg=options['secondary_bg'])
        self.frames[StartFrame] = start_frame

        choose_set_frame = OptionMenuFrame(self, bg=options['secondary_bg'])
        self.frames[OptionMenuFrame] = choose_set_frame

        editing_frame = EditingFrame(self, bg=options['secondary_bg'])
        self.frames[EditingFrame] = editing_frame

        entry_frame = EntryFrame(self, bg=options['secondary_bg'])
        self.frames[EntryFrame] = entry_frame

        options_frame = PreferencesFrame(self, bg=options['secondary_bg'])
        self.frames[PreferencesFrame] = options_frame

        quiz_frame = QuizFrame(self, bg=options['secondary_bg'])
        self.frames[QuizFrame] = quiz_frame

    def back(self, frame):
        self.change_frame(frame, self.last_frame)

    def change_frame(self, start, destination=None, final=None, file_to_update=None):
        #unpack start frame
        self.frames[start].pack_forget()
        self.last_frame = start

        if start == StartFrame:
            self.frames[OptionMenuFrame].update_values(list(sets.keys()))

        if destination:
            #pack destination frame
            self.frames[destination].pack()
        else:
            #this mean func must be called from OptionMenuFrame
            #set last question set
            if self.frames[OptionMenuFrame].question_set:
                self.last_set = self.frames[OptionMenuFrame].get()
            else:
                #this means that the OptionMenuFrame displayed questions
                #saves last question so we can delete the edited question
                self.frames[EntryFrame].last_question = self.frames[OptionMenuFrame].get()

            if self.next_frame == EditingFrame:
                if self.frames[EditingFrame].deleting:
                    del sets[q.last_set]['questions'][q.frames[EntryFrame].last_question]
                    self.frames[EditingFrame].pack()
                    self.frames[EditingFrame].deleting = False
                    file_to_update = sets_file

            self.frames[self.next_frame].pack()

        if not self.frames[OptionMenuFrame].question_set and self.next_frame == EntryFrame:
            try:
                if self.frames[EntryFrame].editing:
                    #this means user is editing a question
                    #set entries to question and answer
                    question = self.frames[OptionMenuFrame].get()
                    #gives answer (KeyError might happen here)
                    answer = sets[self.last_set]['questions'][question]['answer']

                    #update entries
                    self.frames[EntryFrame].set_entries(question, answer)

            except KeyError:
                pass #this means that a question was edited/deleted. it will be automatically fixed next time.

        if final:
            self.next_frame = final

        #handle files
        if file_to_update:
            if file_to_update == sets_file:
                JsonManager.write(sets_file, sets)
            else:
                JsonManager.write(options_file, options_file)


if __name__ == '__main__':
    q = Quizzer()
    q.mainloop()
