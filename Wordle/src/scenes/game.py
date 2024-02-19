import pygame
import random
from string import ascii_lowercase, ascii_uppercase
from src.utils import load_words
from src.buttons.text_button import TextButton
from src.constants import BLACK, WHITE, GREY, GREEN, YELLOW, WIDTH, HEIGHT
from src.scene_enum import Scenes
from src.scenes.base import BaseScene


class Game(BaseScene):
    SQUARE_SIZE = 100
    HALF_SIZE = SQUARE_SIZE/2
    TOTAL_SIZE = SQUARE_SIZE+6

    def __init__(self, app):
        super().__init__(app)


        self.grid = pygame.surface.Surface((self.TOTAL_SIZE*5, self.TOTAL_SIZE*6))
        self.grid_rect = self.grid.get_rect(center=(350, 640))

        self.title = TextButton(
            self.app,
            'Wordle',
            self.app.title_font,
            center=(WIDTH/2, 150)
        )

        self.letters = {
            letter: app.letter_font.render(letter, True, WHITE) for letter in ascii_uppercase
        }

        self.rows = [] # [word, [colours]]
        self.guess = []

        self.words = load_words('assets/other/five_letter_words.txt')
        self.word = random.choice(self.words)
        print(self.word)

        self.draw_error = False
        self.error_message = TextButton(
            app,
            'Not in word list',
            app.letter_font,
            GREEN,
            center=(WIDTH/2, 300)
        )
        self.error_timer = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.change_scene(Scenes.START)
            elif event.key == pygame.K_BACKSPACE:
                if self.guess:
                    self.guess.pop(-1)
            elif event.key == pygame.K_RETURN:
                if len(self.guess) == 5:
                    if ''.join(self.guess) in self.words:
                        colours = []
                        for letter in self.guess:
                            if letter in self.word:
                                if self.guess.index(letter) == self.word.index(letter):
                                    colours.append(GREEN)
                                else:
                                    colours.append(YELLOW)
                            else:
                                colours.append(GREY)

                        self.rows.append(
                            (
                                ''.join(self.guess),
                                colours
                            )
                        )
                        self.guess.clear()
                    else:
                        self.error_timer = 3

            elif event.unicode != '':
                if event.unicode in ascii_lowercase:
                    if len(self.guess) < 5:
                        self.guess.append(event.unicode.upper())

    def draw(self):
        self.app.screen.fill(BLACK)

        #keyboard (soon)
        # vals = list(self.letters.values())
        # for i, surf in enumerate(vals):
        #     self.app.screen.blit(surf, ((i%9)*200, (i//9)*200))

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
