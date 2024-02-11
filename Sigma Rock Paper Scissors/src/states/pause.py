import pygame
from src.states.base import BaseState
from src.ui.button import Button
from src.tools.state_enum import States
from src.tools.constants import WIDTH, WHITE


class Pause(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.title = Button(
            self.app,
            'PAUSED',
            self.app.title_font,
            WHITE,
            (WIDTH/2, 250)
        )

        self.resume_btn = Button(
            self.app,
            'RESUME',
            self.app.normal_font,
            WHITE,
            (WIDTH / 2, 450)
        )

        self.menu_btn = Button(
            self.app,
            'MENU',
            self.app.normal_font,
            WHITE,
            (WIDTH / 2, 650)
        )

    def set_last_frame(self, frame):
        self.last_frame = frame

    def draw(self):
        self.app.screen.blit(self.last_frame, (0, 0))
        self.app.screen.blit(self.surface_tint, (0, 0))

        self.title.draw()

        self.resume_btn.draw()
        self.menu_btn.draw()

    def update(self):
        if self.resume_btn.is_clicked():
            self.app.change_state(States.GAME)

        if self.menu_btn.is_clicked():
            self.app.change_state(States.START)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.change_state(States.GAME)
