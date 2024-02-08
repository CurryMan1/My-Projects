import pygame
from src.constants import WIDTH, HEIGHT
from src.slider import Slider
from src.states.base import BaseState


class Settings(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.slider = Slider(self.app, (WIDTH/2, HEIGHT/2))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                ...

    def draw(self):
        self.slider.draw()

    def update(self):
        self.slider.update()
