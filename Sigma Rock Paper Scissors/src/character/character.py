import pygame
import random
from math import hypot
from src.tools.constants import WIDTH, HEIGHT, EDGE_AVOID_RADIUS


class Character:
    SPEED = 150

    def __init__(self, app, pos, group):
        self.app = app

        self.group = group
        self.image = self.app.characters[group]
        self.rect = self.image.get_frect(center=pos)

        self.moving_vector = pygame.Vector2(0, 0)
        self.repelling_vector = pygame.Vector2(0, 0)

    def move(self):
        if self.moving_vector:
            v = self.moving_vector.normalize() * self.SPEED * self.app.delta
        else:
            v = pygame.Vector2(0, 0) * self.SPEED * self.app.delta

        if (
                EDGE_AVOID_RADIUS <= self.rect.x + v.x <= WIDTH - EDGE_AVOID_RADIUS and
                EDGE_AVOID_RADIUS <= self.rect.y + v.y <= HEIGHT - EDGE_AVOID_RADIUS
        ):
            self.rect.x += v.x
            self.rect.y += v.y

        self.moving_vector = pygame.Vector2(0, 0)

    def add_move(self, vec):
        self.moving_vector += vec

    def move_to(self, character):
        x, y = self.get_xy(character)
        direction = pygame.Vector2(x, y)

        self.add_move(direction)
        if self.rect.colliderect(character.rect):
            character.convert(self.group)

    def move_away_from(self, character):
        x, y = character.get_xy(self)
        if x and y:
            direction = pygame.Vector2(x, y).normalize()
        else:
            direction = pygame.Vector2(
                random.randint(1, 10) * random.choice((-1, 1)),
                random.randint(-10, 10) * random.choice((-1, 1))
            ).normalize()

        self.add_move(direction * self.SPEED * self.app.delta)

    # def move_from_edge(self): #if character is stuck
    #     x, y = 0.1, 0.1
    #
    #     if self.rect.x < EDGE_AVOID_RADIUS:
    #         x = 1
    #     elif self.rect.x < WIDTH - EDGE_AVOID_RADIUS:
    #         x = -1
    #
    #     if self.rect.y < EDGE_AVOID_RADIUS:
    #         y = 1
    #     elif self.rect.y < HEIGHT - EDGE_AVOID_RADIUS:
    #         y = -1
    #
    #     v = pygame.Vector2(x, y).normalize() * 500
    #     self.rect.x += v.x
    #     self.rect.y += v.y

    def distance_to(self, character):
        x, y = self.get_xy(character)
        return hypot(x, y)

    def get_xy(self, character):
        x = character.rect.x - self.rect.x
        y = character.rect.y - self.rect.y
        return x, y

    def convert(self, group):
        self.group = group
        self.image = self.app.characters[group]

    def draw(self):
        self.app.screen.blit(self.image, self.rect)
