import pygame
from src.states.base import BaseState
from src.ui.button import Button
from src.tools.state_enum import States
from src.tools.constants import WIDTH, HEIGHT, WHITE


class Pause(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.title = Button(
            self.app,
            'PAUSED',
            self.app.title_font,
            WHITE,
            (WIDTH/2, 300)
        )

        self.resume_btn = Button(
            self.app,
            'RESUME',
            self.app.normal_font,
            WHITE,
            (WIDTH / 2, HEIGHT/2)
        )

        self.restart_btn = Button(
            self.app,
            'RESTART',
            self.app.normal_font,
            WHITE,
            (WIDTH / 2, 660)
        )

        self.menu_btn = Button(
            self.app,
            'MENU',
            self.app.normal_font,
            WHITE,
            (WIDTH / 2, 780)
        )

    def set_last_frame(self, frame):
        self.last_frame = frame

    def draw(self):
        self.app.screen.blit(self.last_frame, (0, 0))
        self.app.screen.blit(self.surface_tint, (0, 0))

        self.title.draw()

        self.resume_btn.draw()
        self.restart_btn.draw()
        self.menu_btn.draw()

    def update(self):
        if self.resume_btn.is_clicked():
            self.app.change_state(States.GAME)

        if self.restart_btn.is_clicked():
            self.app.get_state(States.GAME).restart()
            self.app.change_state(States.GAME)

        if self.menu_btn.is_clicked():
            self.app.change_state(States.START)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.change_state(States.GAME)
