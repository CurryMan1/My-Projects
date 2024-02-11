import pygame
from src.states.base import BaseState
from src.ui.button import Button
from src.ui.slider import Slider
from src.tools.constants import WIDTH, HEIGHT, WHITE
from src.tools.state_enum import States


class Settings(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.back_btn = Button(
            self.app,
            'BACK',
            self.app.normal_font,
            WHITE,
            (144, 96)
        )

        self.title = Button(
            self.app,
            'SETTINGS',
            self.app.title_font,
            WHITE,
            (WIDTH / 2, 180)
        )

        self.slider = Slider(self.app, (WIDTH/2, HEIGHT/2), 'Team Size: ', 20, 1)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.change_state(States.START)

    def draw(self):
        self.back_btn.draw()
        self.title.draw()
        self.slider.draw()

        self.app.screen.blit(self.app.characters[2], (400, 400))

    def update(self):
        if self.back_btn.is_clicked():
            self.app.change_state(States.START)

        self.slider.update()
