import pygame
import random
from string import ascii_uppercase
from src.utils import load_words
from src.keyboard import Keyboard
from src.buttons.text_button import TextButton
from src.constants import BLACK, WHITE, GREY, GREEN, YELLOW, WIDTH, HEIGHT
from src.scene_enum import Scenes
from src.scenes.base import BaseScene


class Game(BaseScene):
    SQUARE_SIZE = 100
    HALF_SIZE = int(SQUARE_SIZE/2)
    TOTAL_SIZE = SQUARE_SIZE+6

    GAME_COLOURS = [GREY, YELLOW, GREEN]

    def __init__(self, app):
        super().__init__(app)

        self.grid = pygame.surface.Surface((self.TOTAL_SIZE*5, self.TOTAL_SIZE*6))
        self.grid_rect = self.grid.get_rect(center=(350, 640))

        self.keyboard = Keyboard(self, (600, HEIGHT/2), 700, 300)

        self.title = TextButton(
            self.app,
            'Wordle',
            self.app.title_font,
            center=(WIDTH/2, 150)
        )

        self.letters = {
            letter: app.letter_font.render(letter, True, WHITE) for letter in ascii_uppercase
        }

        self.clues = {
            letter: GREY for letter in ascii_uppercase
        }

        self.rows = [] #(word, [colours])
        self.guess = []

        self.words = load_words('assets/other/five_letter_words.txt')
        self.word = random.choice(self.words)
        print(self.word)

        self.hard_mode = False
        self.keyboard_input = True

        self.draw_error = False
        self.error_message = None
        self.error_timer = 0 #in seconds

        self.word_list_error = TextButton(
            app,
            'Not in word list',
            app.letter_font,
            GREEN,
            center=(WIDTH/2, HEIGHT/2)
        )

        self.hard_mode_error = TextButton(
            app,
            'Must use all clues in hard mode',
            app.letter_font,
            GREEN,
            center=(WIDTH/2, HEIGHT/2)
        )

        self.guessed = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.change_scene(Scenes.START)
            elif event.key == pygame.K_BACKSPACE:
                if self.guess:
                    self.guess.pop(-1)
            elif event.key == pygame.K_RETURN:
                if len(self.guess) == 5:
                    guess = ''.join(self.guess)

                    if guess == self.word:
                        self.rows.append(
                            (
                                ''.join(self.guess),
                                [GREEN]*5
                            )
                        )
                        self.guess.clear()
                        self.guessed = True
                        return

                    if guess in self.words:
                        colours = []

                        useful_clues = {
                            lt: self.clues[lt] for lt in self.clues.keys() if self.clues[lt] != GREY
                        }

                        if self.hard_mode:
                            err = False
                            for i, letter in enumerate(list(useful_clues.keys())):
                                if letter not in guess:
                                    err = True
                                    break
                                if not(useful_clues[letter] == GREEN and self.word[i] == self.guess[i]):
                                    err = True
                                    break

                            if err:
                                #hard mode error
                                self.error_message = self.hard_mode_error
                                self.error_timer = 3
                                return

                        for i, letter in enumerate(self.guess):
                            if letter in self.word:
                                if self.guess[i] == self.word[i]:
                                    colours.append(GREEN)
                                    biggest_colour = GREEN
                                else:
                                    colours.append(YELLOW)
                                    biggest_colour = YELLOW
                            else:
                                biggest_colour = GREY
                                colours.append(GREY)

                            old_clue = self.GAME_COLOURS.index(self.clues[letter])
                            new_clue = self.GAME_COLOURS.index(biggest_colour)

                            if new_clue > old_clue:
                                self.clues[letter] = biggest_colour

                        self.rows.append(
                            (
                                guess,
                                colours
                            )
                        )

                        self.guess.clear()
                    else:
                        #not in word list
                        self.error_message = self.word_list_error
                        self.error_timer = 3

            elif event.unicode != '':
                if self.guessed:
                    return

                cap_letter = event.unicode.upper()
                if cap_letter in ascii_uppercase:
                    if len(self.guess) < 5:
                        self.guess.append(cap_letter)

    def draw(self):
        self.app.screen.fill(BLACK)

        self.keyboard.draw()

        self.draw_grid()
        if self.draw_error:
            self.error_message.draw()

    def update(self, delta):
        if self.error_timer > 0:
            self.error_message.surf.set_alpha((self.error_timer/2)*300)

            self.draw_error = True
            self.error_timer = max(self.error_timer-delta, 0)
        else:
            self.draw_error = False

        self.keyboard.update(self.clues)

    def draw_grid(self):
        self.grid.fill(BLACK)

        self.title.draw()

        for column in range(5):
            for row in range(6):
                box_rect = pygame.rect.Rect(
                    (column * self.TOTAL_SIZE + 3, row * self.TOTAL_SIZE + 3), (self.SQUARE_SIZE, self.SQUARE_SIZE)
                )

                if len(self.rows) - 1 >= row:
                    #draw letter
                    letter = self.letters[self.rows[row][0][column]]
                    colour = self.rows[row][1][column]

                    rect = letter.get_rect(
                        center=(column * self.TOTAL_SIZE + self.HALF_SIZE + 3,
                                row * self.TOTAL_SIZE + self.HALF_SIZE + 3)
                    )
                    pygame.draw.rect(self.grid, colour, box_rect, border_radius=2)
                    self.grid.blit(letter, rect)

                else:
                    pygame.draw.rect(
                        self.grid, GREY, box_rect, 3, 2
                    )

        #draw guess
        for i, letter in enumerate(self.guess):
            surf = self.letters[letter]
            rect = surf.get_rect(
                center=(i * self.TOTAL_SIZE + self.HALF_SIZE + 3,
                        len(self.rows) * self.TOTAL_SIZE + self.HALF_SIZE + 3)
            )
            self.grid.blit(surf, rect)

        #blit grid
        self.app.screen.blit(self.grid, self.grid_rect)

    def set_mode(self, hard_mode, keyboard_input):
        self.hard_mode = hard_mode
        self.keyboard_input = keyboard_input
