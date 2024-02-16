import pygame
from src.scene_enum import Scenes
from src.scenes.base import BaseScene
from src.button import Button
from src.constants import WIDTH, HEIGHT, BLACK


class Start(BaseScene):
    def __init__(self, app):
        super().__init__(app)

        self.title = Button(
            self.app,
            'Wordle',
            self.app.title_font,
            (WIDTH/2, 300)
        )

        self.start_btn = Button(
            self.app,
            'Start',
            self.app.normal_font,
            (WIDTH/2, HEIGHT/2)
        )

        self.settings_btn = Button(
            self.app,
            'Settings',
            self.app.normal_font,
            (WIDTH/2, 660)
        )

        self.quit_btn = Button(
            self.app,
            'Quit',
            self.app.normal_font,
            (WIDTH/2, 780)
        )

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.stop()

    def update(self, delta):
        if self.start_btn.is_clicked():
            ...

        if self.settings_btn.is_clicked():
            s = self.app.get_scene(Scenes.SETTINGS)
            s.set_last_frame(self.app.screen.copy())
            self.app.change_scene(Scenes.SETTINGS)

        if self.quit_btn.is_clicked():
            self.app.stop()

    def draw(self):
        self.app.screen.fill(BLACK)

        self.title.draw()

        self.start_btn.draw()
        self.settings_btn.draw()
        self.quit_btn.draw()
