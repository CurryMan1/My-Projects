import pygame
from src.state_enum import States
from src.constants import WIDTH, HEIGHT, LABEL_COLOUR
from src.states.base import BaseState
from src.button import Button
from src.slider import Slider


class Start(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.title = Button(
            app,
            'Guess Simulator',
            self.app.title_font,
            LABEL_COLOUR,
            (WIDTH / 2, 250)
        )

        self.start_btn = Button(
            app,
            "Start",
            self.app.subtitle_font,
            LABEL_COLOUR,
            (450, 575)
        )

        self.quit_btn = Button(
            app,
            "Quit",
            self.app.subtitle_font,
            LABEL_COLOUR,
            (450, 800)
        )

        self.questions_slider = Slider(
            app,
            (1420, 500),
            (450, 120),
            10000,
            100,
            5000,
            1,
            "Questions: ",
            self.app.normal_font
        )

        self.answers_slider = Slider(
            app,
            (1420, 760),
            (450, 120),
            500,
            50,
            250,
            1,
            "Answers: ",
            self.app.normal_font
        )

    def update(self, delta):
        if self.start_btn.is_clicked():
            questions = self.questions_slider.get()
            answers = self.answers_slider.get()

            self.app.change_state(States.LOADING_SCREEN)
            self.app.generate_results(questions, answers)

        if self.quit_btn.is_clicked():
            self.app.stop()

        self.questions_slider.update()
        self.answers_slider.update()

    def draw(self):
        self.title.draw()
        self.start_btn.draw()
        self.quit_btn.draw()
        self.questions_slider.draw()
        self.answers_slider.draw()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.questions_slider.increment(1)
            elif event.key == pygame.K_LEFT:
                self.questions_slider.increment(-1)
