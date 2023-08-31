from tkinter import *
from PIL import Image, ImageTk
from pygame import mixer

mixer.init()
mixer.Channel(0).set_volume(0.5)
mixer.Channel(0).play(mixer.Sound('background music.mp3'), -1)

root = Tk()
root.title('Checkers')
root.iconbitmap('Red Man.ico')
root.resizable(False, False)

def sleep(t):
    root.after(t, root.quit)
    root.mainloop()

class Checkers:
    def __init__(self, root):
        self.chosen_scheme = 0
        self.colour_schemes = (('#995a13', '#d69f59'), ('black', 'grey'), ('green', 'white'))
        self.dark_colours = tuple(s[0] for s in self.colour_schemes)
        self.turn = 0
        self.squares = []
        self.dot_squares = []
        self.hl = []
        self.hopping = False

        self.blank = ImageTk.PhotoImage(Image.open("Blank.png").resize((100,100))) #pyimage1

        self.red_man = ImageTk.PhotoImage(Image.open("Red Man.png").resize((100,100))) #pyimage2
        self.blue_man = ImageTk.PhotoImage(Image.open("Blue Man.png").resize((100,100))) #pyimage3

        self.red_king = ImageTk.PhotoImage(Image.open("Red King.png").resize((100,100))) #pyimage4
        self.blue_king = ImageTk.PhotoImage(Image.open("Blue King.png").resize((100,100))) #pyimage5

        self.selected_red_man = ImageTk.PhotoImage(Image.open("Selected Red Man.png").resize((100,100))) #pyimage6
        self.selected_blue_man = ImageTk.PhotoImage(Image.open("Selected Blue Man.png").resize((100, 100))) #pyimage7

        self.selected_red_king = ImageTk.PhotoImage(Image.open("Selected Red King.png").resize((100,100))) #pyimage8
        self.selected_blue_king = ImageTk.PhotoImage(Image.open("Selected Blue King.png").resize((100,100))) #pyimage9

        self.red_dot = ImageTk.PhotoImage(Image.open("Red Dot.png").resize((100, 100))) #pyimage10
        self.blue_dot = ImageTk.PhotoImage(Image.open("Blue Dot.png").resize((100, 100))) #pyimage11

        self.red_pieces = [str(self.red_king), str(self.red_man)]
        self.blue_pieces = [str(self.blue_king),str(self.blue_man)]

        self.board_frame = Frame(root)

        self.create_board()
    def create_board(self):
        for i in range(64):
            square = Label(self.board_frame, bg=self.colour_schemes[self.chosen_scheme][(i%2) if (i//8) % 2 == 1 else (i%2)-1],
                           width=100,height=100,
                           #add image
                           image=self.blue_man if i in [1,3,5,7,8,10,12,14,17,19,21,23]\
                               else self.red_man if i in [40,42,44,46,49,51,53,55,56,58,60,62]\
                               else self.blank)
            square.grid(row=i//8, column=i%8)
            square.bind('<Button-1>', lambda event, i=i: self.click(event, i))
            self.squares.append(square)
    def click(self, event, i):
        if self.hopping:
            self.turn = 1-self.turn
            self.hopping = False

        #unhighlight
        if self.hl != []:
            self.hl[0]['image'] = self.hl[1]

        #sleep(250)

        square_img = self.squares[i]['image']

        #remove dots
        for square in self.dot_squares:
            square['image'] = self.blank

        #reset temps
        self.hl = []
        self.dot_squares = []

        #check square
        if square_img != str(self.blank): #make sure it's not blank

            #red man
            if square_img == str(self.red_man) and self.turn == 0:
                self.check_piece(square_img, i, self.red_dot, self.selected_red_man, self.blue_pieces,-1)

            #blue man
            elif square_img == str(self.blue_man) and self.turn == 1:
                self.check_piece(square_img, i, self.blue_dot, self.selected_blue_man, self.red_pieces)

            #red king
            elif square_img == str(self.red_king) and self.turn == 0:
                self.check_piece(square_img, i, self.red_dot, self.selected_red_king, self.blue_pieces, king=True)

            #blue king
            elif square_img == str(self.blue_king) and self.turn == 1:
                self.check_piece(square_img, i, self.blue_dot, self.selected_blue_king, self.red_pieces, king=True)

            #dots
            elif square_img in [str(self.red_dot), str(self.blue_dot)]:
                #promote?
                if self.last_selected['image'] == str(self.red_man) and i in [1, 3, 5, 7]:
                    self.last_selected['image'] = self.red_king
                elif self.last_selected['image'] == str(self.blue_man) and i in [56, 58, 60, 62]:
                    self.last_selected['image'] = self.blue_king

                #move
                self.squares[i]['image'] = self.last_selected['image']
                self.last_selected['image'] = self.blank

                #sound
                if abs(i - self.squares.index(self.last_selected)) < 10:
                    mixer.Channel(1).play(mixer.Sound('move-self.mp3'))
                else:
                    mixer.Channel(2).play(mixer.Sound('capture.mp3'))
                    #remove counter
                    self.squares[int((i + self.squares.index(self.last_selected))/2)]['image'] = self.blank

                    #check for double
                    if self.squares[i]['image'] == str(self.red_man):
                        self.check_double(self.squares[i]['image'], i, self.red_dot, self.selected_red_man, self.blue_pieces, -1)
                    elif self.squares[i]['image'] == str(self.blue_man):
                        self.check_double(self.squares[i]['image'], i, self.blue_dot, self.selected_blue_man, self.red_pieces, 1)
                    elif self.squares[i]['image'] == str(self.red_king):
                        self.check_double(self.squares[i]['image'], i, self.red_dot, self.selected_red_king, self.blue_pieces, king=True)
                    elif self.squares[i]['image'] == str(self.blue_king):
                        self.check_double(self.squares[i]['image'], i, self.blue_dot, self.selected_blue_king, self.red_pieces, king=True)

                #next turn
                if not self.hopping:
                    self.turn = 1 - self.turn
                else:
                    self.hopping = False

        self.last_selected = self.squares[i]

    def check_piece(self, square_img, i, dot, selected, pieces, ml=1, king=False):
        #highlight
        self.squares[i]['image'] = selected
        self.hl = [self.squares[i], square_img]
        #check left square
        if i + (ml * 9) in range(64):
            if self.squares[i+(ml*9)]['image'] == str(self.blank) and self.squares[i+(ml*9)]['bg'] in self.dark_colours:
                self.squares[i+(ml*9)]['image'] = dot
                self.dot_squares.append(self.squares[i+(ml*9)])
            elif i + (ml * 18) in range(64):
                if self.squares[i+(ml*9)]['image'] in pieces and self.squares[i+(ml*18)]['image'] == str(self.blank)\
                    and self.squares[i+(ml*18)]['bg'] in self.dark_colours:
                    self.squares[i+(ml*18)]['image'] = dot
                    self.dot_squares.append(self.squares[i+(ml*18)])
        #check right square
        if i + (ml * 7) in range(64):
            if self.squares[i+(ml*7)]['image'] == str(self.blank) and self.squares[i+(ml*7)]['bg'] in self.dark_colours:
                self.squares[i+(ml*7)]['image'] = dot
                self.dot_squares.append(self.squares[i+(ml*7)])
            elif i + (ml * 14) in range(64):
                if self.squares[i+(ml*7)]['image'] in pieces and self.squares[i+(ml*14)]['image'] == str(self.blank)\
                    and self.squares[i+(ml*14)]['bg'] in self.dark_colours:
                    self.squares[i+(ml*14)]['image'] = dot
                    self.dot_squares.append(self.squares[i+(ml*14)])

        #if king repeat
        if king:
            self.check_piece(square_img, i, dot, selected, pieces, ml * (-1))

    def check_double(self, square_img, i, dot, selected, pieces, ml=1, king=False):
        self.hopping=False
        #check left square
        if i + (ml * 18) in range(64):
            if self.squares[i+(ml*9)]['image'] in pieces and self.squares[i+(ml*18)]['image'] == str(self.blank)\
                    and self.squares[i+(ml*18)]['bg'] in self.dark_colours:
                self.squares[i+(ml*18)]['image'] = dot
                self.dot_squares.append(self.squares[i+(ml*18)])
                self.squares[i]['image'] = selected
                self.hopping = True
                self.hl = [self.squares[i], square_img]

        #check right square
        if i + (ml * 14) in range(64):
            if self.squares[i+(ml*7)]['image'] in pieces and self.squares[i+(ml*14)]['image'] == str(self.blank)\
                    and self.squares[i + (ml*14)]['bg'] in self.dark_colours:
                self.squares[i+(ml*14)]['image'] = dot
                self.dot_squares.append(self.squares[i + (ml * 14)])
                self.squares[i]['image'] = selected
                self.hopping = True
                self.hl = [self.squares[i], square_img]

        #if king repeat
        if king:
            self.check_piece(square_img, i, dot, selected, pieces, ml * (-1))



g = Checkers(root)
g.board_frame.grid()
root.mainloop()
