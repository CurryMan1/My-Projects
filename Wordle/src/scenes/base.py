import pygame
from src.constants import WIN_SIZE, BLACK


class BaseScene:
    def __init__(self, app):
        self.app = app

    def handle_event(self, event):
        ...

    def update(self, delta):
        ...

    def draw(self):
        ...
