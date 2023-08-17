from math import floor
from tkinter import *
from PIL import Image, ImageTk
import pygame

pygame.mixer.init()
pygame.mixer.Channel(1).play(pygame.mixer.Sound('background music.mp3'), -1)

class Checkers:
    def __init__(self, root):
        self.root = root

        self.chosen_scheme = 0
        self.colour_schemes = (('#995a13', '#d69f59'), ('black', 'grey'), ('green','white'))
        self.dark_colours = tuple(s[0] for s in self.colour_schemes)
        self.turn = 0
        self.squares = []
        self.dot_squares = []
        self.hl = []

        self.blank = ImageTk.PhotoImage(Image.open("Blank.png").resize((100,100)))

        self.red_man = ImageTk.PhotoImage(Image.open("Red Man.png").resize((100,100)))
        self.blue_man = ImageTk.PhotoImage(Image.open("Blue Man.png").resize((100,100)))

        self.selected_red_man = ImageTk.PhotoImage(Image.open("Selected Red Man.png").resize((100,100)))
        self.selected_blue_man = ImageTk.PhotoImage(Image.open("Selected Blue Man.png").resize((100, 100)))

        self.red_dot = ImageTk.PhotoImage(Image.open("Red Dot.png").resize((100, 100)))
        self.blue_dot = ImageTk.PhotoImage(Image.open("Blue Dot.png").resize((100, 100)))

        self.board_frame = Frame(root)

        self.create_board()
    def create_board(self):
        for i in range(64):
            square = Label(self.board_frame,bg=self.colour_schemes[self.chosen_scheme][(i%2) if floor(i/8) % 2 == 1 else (i%2)-1],
                           width=100,height=100,
                           #add image
                           image=self.blue_man if i in [1,3,5,7,8,10,12,14,17,19,21,23]\
                               else self.red_man if i in [40,42,44,46,49,51,53,55,56,58,60,62]\
                               else self.blank)
            square.grid(row=i//8, column=i%8)
            square.bind('<Button-1>', lambda event, i=i: self.click(event, i))
            self.squares.append(square)
    def click(self, event, i):
        #unhighlight counter
        if self.hl != []:
            self.hl[0]['image'] = self.hl[1]
        square_img = self.squares[i]['image']

        #remove dots
        for square in self.dot_squares:
            square['image'] = self.blank

        #reset temps
        self.hl = []
        self.dot_squares = []
        #check square isn't blank
        if square_img != str(self.blank):

            #red
            if square_img == str(self.red_man) and self.turn == 0:
                #highlight
                self.squares[i]['image'] = self.selected_red_man
                self.hl = [self.squares[i],self.red_man]
                #check left square
                if self.squares[i-9]['image'] == str(self.blank) and self.squares[i - 9]['bg'] in self.dark_colours:
                    self.squares[i-9]['image'] = self.red_dot
                    self.dot_squares.append(self.squares[i-9])
                elif self.squares[i-9]['image'] == str(self.blue_man) and self.squares[i-18]['image'] == str(self.blank)\
                        and self.squares[i-18]['bg'] in self.dark_colours:
                    self.squares[i-18]['image'] = self.red_dot
                    self.dot_squares.append(self.squares[i-18])
                #check right square
                if self.squares[i-7]['image'] == str(self.blank) and self.squares[i - 7]['bg'] in self.dark_colours:
                    self.squares[i-7]['image'] = self.red_dot
                    self.dot_squares.append(self.squares[i-7])
                elif self.squares[i-7]['image'] == str(self.blue_man) and self.squares[i-14]['image'] == str(self.blank)\
                        and self.squares[i-14]['bg'] in self.dark_colours:
                    self.squares[i-14]['image'] = self.red_dot
                    self.dot_squares.append(self.squares[i-14])
            #blue
            elif square_img == str(self.blue_man) and self.turn == 1:
                #highlight
                self.squares[i]['image'] = self.selected_blue_man
                self.hl = [self.squares[i],self.blue_man]

                #check left square
                if self.squares[i+9]['image'] == str(self.blank) and self.squares[i + 9]['bg'] in self.dark_colours:
                    self.squares[i+9].config(image=self.blue_dot)
                    self.dot_squares.append(self.squares[i+9])
                elif self.squares[i+9]['image'] == str(self.red_man) and self.squares[i+18]['image'] == str(self.blank)\
                        and self.squares[i+18]['bg'] in self.dark_colours:
                    self.squares[i+18]['image'] = self.blue_dot
                    self.dot_squares.append(self.squares[i+18])
                #check right square
                if self.squares[i+7]['image'] == str(self.blank) and self.squares[i + 7]['bg'] in self.dark_colours:
                    self.squares[i+7].config(image=self.blue_dot)
                    self.dot_squares.append(self.squares[i+7])
                elif self.squares[i+7]['image'] == str(self.red_man) and self.squares[i+14]['image'] == str(self.blank)\
                        and self.squares[i+14]['bg'] in self.dark_colours:
                    self.squares[i+14]['image'] = self.blue_dot
                    self.dot_squares.append(self.squares[i+14])

            #dots
            elif square_img in [str(self.red_dot), str(self.blue_dot)]:

                #move
                if square_img == str(self.red_dot):
                    self.last_selected['image'] = self.blank
                    self.squares[i]['image'] = self.red_man
                else:
                    self.last_selected['image'] = self.blank
                    self.squares[i]['image'] = self.blue_man

                #sound
                if abs(i - self.squares.index(self.last_selected)) < 10:
                    pygame.mixer.music.load('move-self.mp3')
                else:
                    pygame.mixer.music.load('capture.mp3')
                    self.squares[int((i + self.squares.index(self.last_selected)) / 2)]['image'] = self.blank
                pygame.mixer.music.play()

                #next turn
                self.turn = 1 - self.turn

        self.last_selected = self.squares[i]

root = Tk()
root.title('Checkers')
root.resizable(False, False)

g = Checkers(root)
g.board_frame.grid()
root.mainloop()