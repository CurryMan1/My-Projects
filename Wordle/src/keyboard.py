import pygame
from string import ascii_uppercase


class Keyboard:
    KEY_GAP = 5
    ROWS = 4
    COLUMNS = 8

    def __init__(self, game, pos, width, height):
        self.game = game

        self.surf = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(center=pos)

        self.key_width = (width/self.COLUMNS) - self.KEY_GAP
        self.key_height = (height/self.ROWS) - self.KEY_GAP

        self.last_clues = None

    def update(self, clues):
        if self.last_clues != clues:
            self.last_clues = clues

            for i, letter in enumerate(ascii_uppercase):
                row = i%8
                column = i//8

                r = pygame.Rect(
                    (column*self.key_width+self.KEY_GAP, row*self.key_height+self.KEY_GAP),
                    (self.key_width, self.key_height)
                )

                pygame.draw.rect(
                    self.surf,
                    clues[letter],
                    r,
                    0,
                    3
                )
                self.surf.blit(self.game.letters[letter], r)

    def draw(self):
        self.game.app.screen.blit(self.surf, self.rect)
