import pygame
from src.states.base import BaseState
from src.button import Button
from src.bar_graph import BarGraph


class ResultsDisplayer(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.bar_graph = ...

    def update(self, delta):
        ...

    def draw(self):
        ...

    def handle_event(self, event):
        ...
