import pygame
from utils import *

def get_box(width, height, border_width, fg, bg):
    box = pygame.surface.Surface((width, height))
    box.fill(bg)
    front = pygame.surface.Surface((width - border_width * 2, height - border_width*2))
    front.fill(fg)

    box.blit(front, (border_width, border_width))
    return box

class SlidingMenu:
    def __init__(self, x: int, y: int, width: int, height: int, fg, bg, border_width: int, buttons: list):
        self.image = get_box(width, height, border_width, fg, bg)

        self.rect = self.image.get_rect(midtop=(x, y))
        self.buttons = buttons
        self.moving = False
        self.y_vel = 20

    def update(self, screen, height):
        y = self.rect.y
        if self.moving:
            self.rect.y += self.y_vel

            if self.rect.y not in range(height-self.rect.height, height):
                self.moving = False
                if self.y_vel > 0:
                    self.rect.y = height
                else:
                    self.rect.y = height-self.rect.height-20

        for button in self.buttons:
            button.rect.y += self.y_vel

        screen.blit(self.image, self.rect.topleft)

    def toggle(self):
        self.y_vel *= -1
        self.moving = True

class Button:
    def __init__(self, x: int, y: int, width: int=None, height: int=None, fg=None, bg=None, border_width=None,
                 text: str=None, text_size=None, text_colour=None, image: pygame.surface.Surface=None):

        self.text = text
        self.text_size = text_size
        self.text_colour = text_colour
        if image:
            self.image = image
        else:
            self.image = get_box(width, height, border_width, fg, bg)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.can_click = False

    def is_clicked(self, screen: pygame.surface.Surface):  #draws button too
        clicked = False

        #makes button only give true ONCE (until released)
        if self.rect.collidepoint((pygame.mouse.get_pos())):
            if pygame.mouse.get_pressed()[0] == 0:
                self.can_click = True
                self.clicked = True
            else:
                if self.can_click and self.clicked:
                    clicked = True
                self.clicked = False
        else:
            self.can_click = False

        screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.text:
            draw_text(self.text, PIXEL_FONT, self.text_colour, self.rect.centerx, self.rect.centery, self.text_size, screen, True)

        return clicked

class UpgradeButton(Button):
    def __init__(self, text):
        super().__init__()