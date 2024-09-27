import pygame
from src.button import Button
from src.constants import WHITE


class Entry:
    def __init__(
        self,
        app,
        pos: tuple[int, int],
        character_limit: int,
        text_colour=WHITE,
        line_colour=WHITE
    ):
        self.app = app
        
        self.string = ''
        self.character_limit = character_limit

        self.line = Button(
            app,
            '_'*(character_limit+1),
            app.normal_font,
            WHITE,
            pos
        )

        self.text = Button(
            app,
            'Entry',
            app.normal_font,
            WHITE,
            pos
        )

    def draw(self):
        self.line.draw()
        self.text.draw()

    def update(self): #when text is updated
        ...
