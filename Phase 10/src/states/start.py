import pygame
from src.state_enum import States
from src.states.base import BaseState
from src.button import Button
from src.constants import WHITE, RED, YELLOW, GREEN, BLUE, WIDTH, HEIGHT


class Start(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.sign_in_btn = Button(
            app,
            'Sign In',
            self.app.normal_font,
            WHITE,
            (WIDTH-120, 90),
            GREEN
        )

        self.title = Button(
            app,
            'Phase 10',
            self.app.title_font,
            WHITE,
            (WIDTH/2, 375)
        )

        self.credit_title = Button(
            app,
            'Made by Hardhik Vittanala 11B',
            self.app.subtitle_font,
            WHITE,
            (WIDTH/2, 500)
        )
        
        self.start_btn = Button(
            app,
            'Start',
            self.app.normal_font,
            WHITE,
            (WIDTH/2, 700),
            RED
        )

        self.quit_btn = Button(
            app,
            'Quit',
            self.app.normal_font,
            WHITE,
            (WIDTH/2, 820),
            BLUE
        )

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.stop()

    def update(self, delta):
        if self.start_btn.is_clicked():
            self.app.change_state(States.GAME)
        
        if self.quit_btn.is_clicked():
            self.app.stop()

        if self.sign_in_btn.is_clicked():
            self.app.change_state(States.SIGN_IN)

    def draw(self):
        self.sign_in_btn.draw()
        
        self.title.draw()
        self.credit_title.draw()
        
        self.start_btn.draw()
        self.quit_btn.draw()
        
