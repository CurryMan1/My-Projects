import pygame
from src.tools.constants import WIDTH, HEIGHT, WHITE
from src.tools.state_enum import States
from src.ui.button import Button
from src.states.base import BaseState


class Start(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.title = Button(
            self.app,
            'SIGMA RPS',
            self.app.title_font,
            WHITE,
            (WIDTH/2, 300)
        )

        self.start_btn = Button(
            self.app,
            'START',
            self.app.normal_font,
            WHITE,
            (WIDTH/2, HEIGHT/2)
        )

        self.settings_btn = Button(
            self.app,
            'SETTINGS',
            self.app.normal_font,
            WHITE,
            (WIDTH/2, 660)
        )

        self.quit_btn = Button(
            self.app,
            'QUIT',
            self.app.normal_font,
            WHITE,
            (WIDTH/2, 780)
        )

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.stop()

    def update(self):
        if self.quit_btn.is_clicked():
            self.app.stop()

        if self.settings_btn.is_clicked():
            self.app.change_state(States.SETTINGS)

        if self.start_btn.is_clicked():
            self.app.change_state(States.GAME)

    def draw(self):
        self.title.draw()
        self.start_btn.draw()
        self.settings_btn.draw()
        self.quit_btn.draw()
