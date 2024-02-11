import pygame
import random
from src.character.character import Character
from src.tools.state_enum import States
from src.tools.constants import WIDTH, HEIGHT, EDGE_AVOID_RADIUS, RUN_AWAY_RADIUS
from src.states.base import BaseState


class Game(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.characters = [
            Character(app,
                      (random.randint(EDGE_AVOID_RADIUS, WIDTH - EDGE_AVOID_RADIUS),
                       random.randint(EDGE_AVOID_RADIUS, HEIGHT - EDGE_AVOID_RADIUS)),
                      i//20) for i in range(60)
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

    def update(self):
        self.update_characters()

    def update_characters(self):
        for char in self.characters:
            prey = [c for c in self.characters if (char.group+1) % 3 == c.group]
            predators = [c for c in self.characters if (char.group+2) % 3 == c.group]

            nearest_prey = min(prey, key=char.distance_to, default=None)
            nearest_predators = sorted(predators, key=char.distance_to)[:3]
            nearest_teammates = [c for c in self.characters if char.group == c.group and char.rect.colliderect(c.rect)]

            for teammate in nearest_teammates:
                char.move_away_from(teammate)

            for predator in nearest_predators:
                if char.distance_to(predator) < RUN_AWAY_RADIUS:
                    char.move_away_from(predator)

            if nearest_prey:
                char.move_to(nearest_prey)
                pygame.draw.rect(self.app.screen, (0, 0, 0), nearest_prey.rect, 1)

        for char in self.characters:
            char.move()
