import pygame
from src.constants import WIDTH, SHADOW_COLOUR, LABEL_COLOUR, ACCENT_COLOUR
from src.utils import round_to_multiple


class Slider:
    def __init__(self, app, pos, size: tuple[int, int], max_value, min_value, value, increment, text=None, font=None):
        self.app = app

        self.shadow = pygame.surface.Surface(size)
        self.shadow.fill(SHADOW_COLOUR)

        self.rect = self.shadow.get_rect(center=pos)

        self.text = text
        self.font = font

        self.max_value = max_value
        self.min_value = min_value

        self.increment_percentage = increment / max_value
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

            self.value = round_to_multiple(exact_val, self.increment_percentage)

        if (
            self.mouse_in_y and
            self.mouse_in_x and
            self.app.mouse_input[0]
        ):
            self.clicked = True
        else:
            self.clicked = False

    def draw(self):
        shadow_movement = 5 * (self.rect.height*1.2 / 90)
        self.app.screen.blit(self.shadow, self.rect.move(shadow_movement, shadow_movement))

        #progress
        surf = pygame.surface.Surface((self.value*self.rect.width, self.rect.height))
        surf.fill(LABEL_COLOUR)
        self.app.screen.blit(surf, self.rect)

        #text
        if self.text:
            label = self.font.render(self.text + str(round(self.get())), True, ACCENT_COLOUR)
            #centers the text
            self.app.screen.blit(
                label, label.get_rect(center=self.rect.move(shadow_movement/2, shadow_movement/2).center)
            )

    def increment(self, amount):
        if self.mouse_in_x and self.mouse_in_y:
            value = self.value + self.increment_percentage * amount
            if self.increment_percentage < value < 1:
                self.value = value

    def get(self):
        return round(self.value*self.max_value)
