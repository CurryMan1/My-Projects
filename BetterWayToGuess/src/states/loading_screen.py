import pygame
import threading
from src.state_enum import States
from src.states.base import BaseState
from src.button import Button
from src.constants import WIDTH, HEIGHT, LABEL_COLOUR


class LoadingScreen(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.labels = [
            Button(
                self.app,
                "Loading"+"."*i,
                self.app.title_font,
                LABEL_COLOUR,
                (WIDTH/2, HEIGHT/2)
            )
            for i in range(4)
        ]

        self.time_elapsed = 0
        self.delay = 200

        self.is_loading = False
        self.first = True
        self.results_thread = None

    def update(self, delta):
        #animation
        self.time_elapsed += int(delta*1000)
        self.time_elapsed %= self.delay*len(self.labels)

        if self.first:
            #create results thread
            self.results_thread = threading.Thread(target=self.app.results_generator.generate)
            self.results_thread.start()
            self.first = False
        elif self.results_thread:
            if not self.results_thread.is_alive():
                self.app.change_state(States.RESULTS_DISPLAYER)

    def draw(self):
        #animation
        self.labels[self.time_elapsed//self.delay].draw()

    def handle_event(self, event):
        ...
