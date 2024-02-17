import pygame
from src.buttons.image_button import ImageButton
from src.constants import GREEN, WHITE


class TextButton(ImageButton):
    def __init__(self, app, text, font: pygame.font.Font, colour=WHITE, **kwargs):
        super().__init__(
            app,
            font.render(text, True, colour),
            font.render(text, True, GREEN),
            **kwargs
        )
