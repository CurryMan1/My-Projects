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

        self.ending = False
        self.time = 0

    def restart(self):
        self.set_players(self.app.get_state(States.SETTINGS).player_slider.get())
        self.app.change_state(States.START)

    def set_players(self, players):
        self.characters = [
            Character(self.app,
                      (random.randint(EDGE_AVOID_RADIUS+20, WIDTH - EDGE_AVOID_RADIUS-20),
                       random.randint(EDGE_AVOID_RADIUS+20, HEIGHT - EDGE_AVOID_RADIUS-20)),
                      i//players) for i in range(players*3)
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

    def update(self):
        self.update_characters()

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
                    (WIDTH/2, HEIGHT/2)
                )
                return

            for teammate in nearest_teammates:
                char.move_away_from(teammate)

            for predator in nearest_predators[:3]:
                if char.distance_to(predator) < RUN_AWAY_RADIUS:
                    char.move_away_from(predator)

            if nearest_prey and nearest_prey.distance_to(char) < CHASE_RADIUS:
                char.move_to(nearest_prey)

        for char in self.characters:
            char.move()
