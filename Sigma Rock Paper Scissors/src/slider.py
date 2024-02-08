import pygame
from src.constants import WIDTH, WHITE, BLACK, BLUE


class Slider:
    def __init__(self, app, pos):
        self.app = app

        self.shadow = pygame.surface.Surface((WIDTH/3, 100))
        self.shadow.fill(BLACK)

        self.rect = self.shadow.get_rect(center=pos)

        self.value = 1
        self.clicked = False

        self.active = False

    def update(self):
        if self.active:
            mouse_in_y = self.rect.top < self.app.mouse_pos[1] < self.rect.bottom
            mouse_in_x = self.rect.left < self.app.mouse_pos[0] < self.rect.right

            if self.clicked:
                percent = 1 - ((self.rect.right-self.app.mouse_pos[0])/self.rect.width)
                if mouse_in_x:
                    self.value = percent
                else:
                    self.value = min([0, 1], key=lambda x: abs(x - percent))

            if mouse_in_y and mouse_in_x:
                if self.app.mouse_input[0]:
                    self.clicked = True
            else:
                self.clicked = False

        elif not self.app.mouse_input[0]:
            self.active = True

    def draw(self):
        self.app.screen.blit(self.shadow, self.rect.move(5, 5))

        #progress
        surf = pygame.surface.Surface((self.value*self.rect.width, self.rect.height))
        surf.fill(BLUE)
        self.app.screen.blit(surf, self.rect)

        #text
        label = self.app.normal_font.render(str(self.get()), True, WHITE)
        self.app.screen.blit(label, label.get_rect(center=self.rect.center))

    def get(self):
        return round(self.value*100)
