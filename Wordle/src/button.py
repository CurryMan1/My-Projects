import pygame
from src.constants import GREEN, WHITE


class Button:
    def __init__(self, app, text, font: pygame.font.Font, pos: tuple[int, int]):
        self.app = app
        self.surf = font.render(text, True, WHITE)
        self.selected_surf = font.render(text, True, GREEN)

        self.rect = self.surf.get_rect(center=pos)
        self.hovered = False

    def is_clicked(self) -> bool:
        self.hovered = self.rect.collidepoint(self.app.mouse_pos)
        return self.hovered and self.app.mouse_input[0]

    def draw(self) -> None:
        if self.hovered:
            self.app.screen.blit(self.selected_surf, self.rect)
        else:
            self.app.screen.blit(self.surf, self.rect)
