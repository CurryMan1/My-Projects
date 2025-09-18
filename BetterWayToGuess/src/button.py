import pygame
from math import copysign
from src.constants import GREY, SHADOW_COLOUR, SELECTED_COLOUR


class Button:
    def __init__(
            self,
            app,
            text: str,
            font: pygame.font.Font,
            colour: tuple[int, int, int],
            pos: tuple[int, int],
            selected_colour=SELECTED_COLOUR,
            shadow_colour=SHADOW_COLOUR
    ):
        self.app = app

        self.pos = pos
        self.font = font
        self.colour = colour
        self.selected_colour = selected_colour
        self.shadow_colour = shadow_colour

        self.surf = font.render(text, True, colour)
        self.selected_surf = font.render(text, True, selected_colour)
        self.shadow = font.render(text, True, shadow_colour)
        self.disabled_surf = font.render(text, True, GREY)

        self.disabled = False

        self.rect = self.surf.get_rect(center=pos)
        self.hovered = False

    def is_clicked(self, mouse_input=None, mouse_pos=None) -> bool:
        if not self.disabled:
            if mouse_pos or mouse_input:
                self.hovered = self.is_hovered(mouse_pos)
                return self.hovered and mouse_input[0]
            else:
                self.hovered = self.is_hovered(self.app.mouse_pos)
                return self.hovered and self.app.mouse_input[0]

    def draw(self) -> None:
        shadow_movement = 5*(self.font.get_point_size()/90)
        self.app.screen.blit(self.shadow, self.rect.move(shadow_movement, shadow_movement))
        if self.disabled:
            self.app.screen.blit(self.disabled_surf, self.rect)
        else:
            if self.hovered:
                self.app.screen.blit(self.selected_surf, self.rect)
            else:
                self.app.screen.blit(self.surf, self.rect)

    def change_text(self, text):
        self.surf = self.font.render(text, True, self.colour)
        self.selected_surf = self.font.render(text, True, self.selected_colour)
        self.rect = self.surf.get_rect(center=self.pos)
        self.shadow = self.font.render(text, True, self.shadow_colour)

    def align(self, x, y, x_offset, y_offset):
        self.rect.centerx = x + copysign(abs(x_offset) + abs(self.rect.width / 2), x_offset)
        self.rect.centery = y + copysign(abs(y_offset) + abs(self.rect.height / 2), y_offset)

    def toggle_enable(self):
        self.disabled = not self.disabled

    def is_hovered(self, pos=None):
        return self.rect.collidepoint(pos)
