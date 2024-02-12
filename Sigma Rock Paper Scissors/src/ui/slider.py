import pygame
from src.tools.constants import WIDTH, WHITE, BLACK, BLUE
from src.tools.utils import round_to_multiple


class Slider:
    def __init__(self, app, pos, text, max_value, min_value, value):
        self.app = app

        self.shadow = pygame.surface.Surface((WIDTH/3, 100))
        self.shadow.fill(BLACK)

        self.rect = self.shadow.get_rect(center=pos)

        self.text = text

        self.max_value = max_value
        self.min_value = min_value

        self.increment_percent = 1/(100/max_value)
        self.min_percentage = min_value/max_value

        self.value = value/max_value
        self.clicked = False

        self.mouse_in_x = False
        self.mouse_in_y = False

    def update(self):
        self.mouse_in_x = self.rect.left < self.app.mouse_pos[0] < self.rect.right
        self.mouse_in_y = self.rect.top < self.app.mouse_pos[1] < self.rect.bottom

        if self.clicked:
            percent = 1 - ((self.rect.right-self.app.mouse_pos[0])/self.rect.width)
            if self.mouse_in_x:
                exact_val = max(self.min_percentage, percent)
            else:
                exact_val = min([self.min_percentage, 1], key=lambda x: abs(x - percent))

            self.value = round_to_multiple(exact_val, self.min_percentage)

        if (
            self.mouse_in_y and
            self.mouse_in_x and
            self.app.mouse_input[0]
        ):
            self.clicked = True
        else:
            self.clicked = False

    def draw(self):
        self.app.screen.blit(self.shadow, self.rect.move(5, 5))

        #progress
        surf = pygame.surface.Surface((self.value*self.rect.width, self.rect.height))
        surf.fill(BLUE)
        self.app.screen.blit(surf, self.rect)

        #text
        label = self.app.normal_font.render(self.text + str(round(self.get())), True, WHITE)
        self.app.screen.blit(label, label.get_rect(center=self.rect.center))

    def increment(self, amount):
        if self.mouse_in_x and self.mouse_in_y:
            value = self.value + self.min_percentage*amount
            if self.min_percentage < value < 1:
                self.value = value

    def get(self):
        return round(self.value*100*self.increment_percent)
