import pygame
from src.states.base import BaseState
from src.entry import Entry
from src.button import Button
from src.constants import WIN_SIZE


class SignIn(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.username_entry = Entry(
            app,
            pygame.Vector2(WIN_SIZE)/2,
            10
        )

    def update(self, delta):
        ...

    def draw(self):
        self.username_entry.draw()
