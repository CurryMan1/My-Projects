import pygame


class BaseState:
    def __init__(self, app):
        self.app = app
        self.last_frame = None

    def handle_event(self, event):
        ...

    def update(self):
        ...

    def draw(self):
        ...
