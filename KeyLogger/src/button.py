import pygame
from src.constants import BLACK, PURPLE, GREY


class Button:
    def __init__(self, app,
                 text: str,
                 font: pygame.font.Font,
                 colour: tuple[int, int, int],
                 pos: tuple[int, int],
                 selected_colour=GREY,
                 shadow_colour=BLACK):
        self.app = app
        self.surf = font.render(text, True, colour)
        self.selected_surf = font.render(text, True, selected_colour)
        self.shadow = font.render(text, True, shadow_colour)
        self.disabled_surf = font.render(text, True, GREY)
        
        self.disabled = False

        self.rect = self.surf.get_rect(center=pos)
        self.hovered = False

    def is_clicked(self) -> bool:
        if not self.disabled:
            self.hovered = self.rect.collidepoint(self.app.mouse_pos)
            return self.hovered and self.app.mouse_input[0]

    def draw(self) -> None:
        self.app.screen.blit(self.shadow, self.rect.move(5, 5))
        if self.disabled:
            self.app.screen.blit(self.disabled_surf, self.rect)
        else:
            if self.hovered:
                self.app.screen.blit(self.selected_surf, self.rect)
            else:
                self.app.screen.blit(self.surf, self.rect)

    def toggle_enable(self):
        self.disabled = not self.disabled
