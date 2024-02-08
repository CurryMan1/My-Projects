import pygame
from src.constants import WIDTH, HEIGHT, WHITE
from src.utils import load_img
from src.button import Button
from src.states.base import BaseState


class Start(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.background = load_img('background.jpeg')

        self.title = Button(
            self.app,
            'SIGMA RPS',
            self.app.title_font,
            WHITE,
            (WIDTH/2, 250)
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
            (WIDTH/2, 550)
        )

        self.quit_btn = Button(
            self.app,
            'QUIT',
            self.app.normal_font,
            WHITE,
            (WIDTH/2, 650)
        )

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.stop()

    def update(self):
        if self.quit_btn.is_clicked():
            self.app.stop()

        if self.settings_btn.is_clicked():
            ...

        if self.start_btn.is_clicked():
            ...

    def draw(self):
        self.app.screen.blit(self.background, (0, 0))

        self.title.draw()
        self.start_btn.draw()
        self.settings_btn.draw()
        self.quit_btn.draw()
