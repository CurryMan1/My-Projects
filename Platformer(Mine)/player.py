import pygame
from os import listdir

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, path):
        super().__init__()
        sheets = listdir(path)

        self.animations = {}
        for sheet in sheets:
            pass
