import pygame
from src.scenes.base import BaseScene


class Pause(BaseScene):
    def __init__(self, app):
        super().__init__(app)
        self.last_frame = None

    def handle_event(self, event):
        ...
