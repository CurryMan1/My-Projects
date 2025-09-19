import pygame
from src.states.base import BaseState


class ResultsDisplayer(BaseState):
    def __init__(self, app):
        super().__init__(app)

    def update(self, delta):
        ...

    def draw(self):
        ...

    def handle_event(self, event):
        ...
