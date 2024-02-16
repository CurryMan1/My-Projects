import pygame
from src.switch import Switch
from src.constants import WIN_SIZE
from src.scenes.base import BaseScene
from src.scene_enum import Scenes


class Settings(BaseScene):
    def __init__(self, app):
        super().__init__(app)

        self.last_frame = None

        self.surface_tint = pygame.Surface(WIN_SIZE)
        self.surface_tint.fill((0, 0, 0))
        self.surface_tint.set_alpha(128)

        #switch
        self.hard_switch = Switch(app, 1000, 200, (WIN_SIZE[0]/2, WIN_SIZE[1]/2))
        self.switch2 = Switch(app, 200, 40, (WIN_SIZE[0] / 2, WIN_SIZE[1] / 2+300))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.change_scene(Scenes.START)

    def update(self, delta):
        self.hard_switch.update(delta)
        self.switch2.update(delta)

    def draw(self):
        self.app.screen.blit(self.last_frame, (0, 0))
        self.app.screen.blit(self.surface_tint, (0, 0))

        self.hard_switch.draw()
        self.switch2.draw()

    def set_last_frame(self, frame):
        self.last_frame = frame
