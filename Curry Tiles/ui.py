from utils import *


def get_box(width, height, border_width, fg, bg, text=None, text_col=None):
    box = pygame.surface.Surface((width, height))
    box.fill(bg)
    front = pygame.surface.Surface((width - border_width * 2, height - border_width*2))
    front.fill(fg)

    box.blit(front, (border_width, border_width))

    #text
    if text:
        draw_text(text, text_col, width/2, height/2, 20, box)

    return box


class Button:
    def __init__(self, x: int, y: int, *args, **kwargs):
        self.image = get_box(*args, *kwargs)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False

    def draw(self, surf: pygame.surface.Surface, mouse_click, mouse_pos) -> bool:
        clicked = False

        #makes button only give true ONCE (until released)
        if self.rect.collidepoint((mouse_pos)):
            if mouse_click:
                clicked = True

        surf.blit(self.image, (self.rect.x, self.rect.y))

        return clicked
