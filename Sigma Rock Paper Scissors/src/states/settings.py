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

        self.subtitle = Button(
            self.app,
            'Use arrow keys while hovering to increment',
            self.app.small_font,
            WHITE,
            (WIDTH / 2, 330)
        )

        self.player_slider = Slider(self.app, (WIDTH/2, 500), 'Team Size: ', 250, 1, 100)
        self.seed_slider = Slider(self.app, (WIDTH/2, 650), 'Seed: ', 10000, 1, 5000)

    def get(self):
        return self.player_slider.get(), self.seed_slider.get()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.change_state(States.START)
            elif event.key == pygame.K_RIGHT:
                self.player_slider.increment(1)
                self.seed_slider.increment(1)
            elif event.key == pygame.K_LEFT:
                self.player_slider.increment(-1)
                self.seed_slider.increment(-1)

    def draw(self):
        self.back_btn.draw()

        self.title.draw()
        self.subtitle.draw()

        self.player_slider.draw()
        self.seed_slider.draw()

    def update(self):
        if self.back_btn.is_clicked():
            self.app.change_state(States.START)

        self.player_slider.update()
        self.seed_slider.update()
