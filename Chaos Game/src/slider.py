import pygame
from src.button import Button
from src.constants import WHITE


class Slider:
    def __init__(self, app, pos, width, height, min_value, max_value, label=None, edit_result=None):
        self.app = app

        self.edit_func = edit_result

        self.width = width
        self.height = height

        self.background = pygame.surface.Surface((width, height))
        self.background.fill(self.app.ACCENT_COLOUR)

        self.rect = self.background.get_rect(center=pos)

        self.max_value = max_value-min_value
        self.min_value = min_value
        self.increment_val = 1/max_value

        self.value = 1
        self.clicked = False

        self.mouse_in_x = False
        self.mouse_in_y = False

        self.label = None
        self.label_text = label
        if label:
            self.label = Button(
                app,
                self.label_text+': '+str(self.get()),
                self.app.small_font,
                WHITE,
                pos-pygame.Vector2(0, 50)
            )

    def increment(self, amount):
        if self.mouse_in_x and self.mouse_in_y:
            value = self.value + self.increment_val*amount
            if 0 < value < 1:
                self.set_value(value)

    def update(self):
        self.mouse_in_x = self.rect.left < self.app.mouse_pos[0] < self.rect.right
        self.mouse_in_y = self.rect.top < self.app.mouse_pos[1] < self.rect.bottom

        if self.mouse_in_y:
            if self.clicked:
                self.value = pygame.math.clamp((self.app.mouse_pos[0] - self.rect.left)/self.width, 0, 1)
                self.label.change_text(self.label_text+': '+str(self.get()))

        if (
            self.mouse_in_y and
            self.mouse_in_x and
            self.app.mouse_input[0]
        ):
            self.clicked = True
        else:
            self.clicked = False

    def draw(self):
        self.app.screen.blit(self.background, self.rect)

        pygame.draw.circle(
            self.app.screen, WHITE, (self.rect.left, self.rect.centery), self.height/2
        )
        pygame.draw.circle(
            self.app.screen, self.app.ACCENT_COLOUR, (self.rect.right, self.rect.centery), self.height/2
        )

        progress_x = self.value*self.width
        surf = pygame.surface.Surface(
            (progress_x, self.rect.height)
        )
        surf.fill(WHITE)
        self.app.screen.blit(surf, self.rect)

        pygame.draw.circle(
            self.app.screen, WHITE, (self.rect.x+progress_x, self.rect.centery), self.height/2*1.15
        )

        #label
        if self.label:
            self.label.draw()

    def get(self):
        val = round((self.value * self.max_value)+self.min_value)
        if self.edit_func:
            return self.edit_func(val)
        else:
            return val

    def set_value(self, val):
        self.value = val
        self.label.change_text(self.label_text+': '+str(self.get()))

    def set_display(self, dis):
        self.set_value(dis/self.max_value)
