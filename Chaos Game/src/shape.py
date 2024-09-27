import random
import pygame
from src.constants import BLUE, WHITE


class Shape:
    def __init__(self, app, size, pos):
        self.app = app
        self.points = []
        self.edges = []

        self.size = size
        self.pos = pos
        self.top_point = pygame.Vector2(0, -self.size)
        self.points.append(self.top_point)

        self.angle = 120

    def update(self, sides):
        if 360/sides == self.angle:
            return
        self.angle = 360/sides
        self.points = self.points[:1]

        for i in range(sides):
            next_point = self.top_point.rotate(self.angle*(i+1))
            self.points.append(next_point)

    def draw(self):
        last_point = None
        for p in self.points:
            next_point = self.pos + p
            if last_point:
                pygame.draw.line(self.app.screen, WHITE, last_point, next_point, 8)
            last_point = next_point

        for p in self.points:
            next_point = self.pos + p
            pygame.draw.circle(self.app.screen, BLUE, next_point, 12)

    def get_random(self):
        x = random.choice(self.points) + self.pos
        return x

    def get_edges(self):
        if len(self.points) == len(self.edges):
            return self.edges

        self.edges.clear()

        for i in range(len(self.points)-1):
            point1 = self.points[i]+self.pos
            point2 = self.points[i+1]+self.pos

            edge = sorted([point1, point2], key=lambda point: point[1])
            self.edges.append(edge)

        return self.edges
