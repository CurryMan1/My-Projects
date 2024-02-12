import pygame
import random
from src.character.character import Character
from src.tools.state_enum import States
from src.tools.constants import WIDTH, HEIGHT, EDGE_AVOID_RADIUS, RUN_AWAY_RADIUS, CHASE_RADIUS, WHITE
from src.ui.button import Button
from src.states.base import BaseState


class Game(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.characters = []

        self.end_title = None
        self.restart_button = Button(
            app, 'RESTART',
            self.app.normal_font,
            WHITE,
            (WIDTH/2, HEIGHT/2+90)
        )

        self.ending = False
        self.time = 0

        self.pl_g = random.Random()

    def restart(self):
        settings = self.app.get_state(States.SETTINGS)

        self.set_characters(*settings.get())
        self.app.change_state(States.START)

    def set_characters(self, characters, seed=0):
        self.pl_g.seed(seed)
        self.characters = [
            Character(self.app,
                      (self.pl_g.randint(EDGE_AVOID_RADIUS+20, WIDTH - EDGE_AVOID_RADIUS-20),
                       self.pl_g.randint(EDGE_AVOID_RADIUS+20, HEIGHT - EDGE_AVOID_RADIUS-20)),
                      i // characters) for i in range(characters*3)
        ]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_state = self.app.get_state(States.PAUSE)
                pause_state.set_last_frame(self.app.screen.copy())
                self.app.change_state(States.PAUSE)

    def draw(self):
        for char in self.characters:
            char.draw()

        if self.ending:
            self.end_title.draw()
            self.restart_button.draw()

    def update(self):
        self.update_characters()
        if self.restart_button.is_clicked():
            self.restart()

    def update_characters(self):
        if self.ending:
            if self.time >= 1:
                self.ending = False
                self.restart()
            return

        for char in self.characters:
            prey = [c for c in self.characters if (char.group+1) % 3 == c.group]
            predators = [c for c in self.characters if (char.group+2) % 3 == c.group]

            nearest_prey = min(prey, key=char.distance_to, default=None)
            nearest_predators = sorted(predators, key=char.distance_to)
            nearest_teammates = [c for c in self.characters if char.group == c.group and char.rect.colliderect(c.rect)]

            #check for game end
            if not(nearest_prey or nearest_predators):
                self.ending = True
                self.time = 0
                self.last_frame = self.app.screen.copy()
                self.end_title = Button(
                    self.app, ['FINNS', 'FRAGRANCES', 'GEORGES'][char.group] + ' WIN',
                    self.app.title_font,
                    WHITE,
                    (WIDTH/2, HEIGHT/2-60)
                )
                return

            for teammate in nearest_teammates:
                char.move_away_from(teammate)

            for predator in nearest_predators[:3]:
                if predator.distance_to(char) < RUN_AWAY_RADIUS:
                    char.move_away_from(predator)

            if nearest_prey and nearest_prey.distance_to(char) < CHASE_RADIUS:
                char.move_to(nearest_prey)

        for char in self.characters:
            char.move()
