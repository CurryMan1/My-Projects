import pygame
from src.constants import WIN_SIZE, BLACK


class BaseScene:
    def __init__(self, app):
        self.app = app

        #for settings

        # self.last_frame = None
        #
        # self.surface_tint = pygame.Surface(WIN_SIZE)
        # self.surface_tint.fill(BLACK)
        # self.surface_tint.set_alpha(128)

    def handle_event(self, event):
        ...

    def update(self):
        ...

    def draw(self):
        ...
