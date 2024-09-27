import pygame
from src.constants import WHITE, GREY, GREEN


class Switch:
    SPEED = 15

    def __init__(self, app, width, height, on_colour=GREEN, off_colour=GREY, **kwargs):
        self.app = app

        self.width = width
        self.height = height
        self.half_height = int(height/2)

        self.on_colour = pygame.Color(on_colour)
        self.off_colour = pygame.Color(off_colour)

        self.colour = off_colour

        #rect
        self.surf = pygame.surface.Surface((width, height))
        self.rect = self.surf.get_frect(**kwargs)

        #knob
        self.knob_start = self.rect.left + self.half_height
        self.knob_end = self.rect.right - self.half_height
        self.knob_travel_dist = self.knob_end - self.knob_start

        self.knob_radius = self.half_height * 0.75
        self.knob_pos = pygame.Vector2(self.knob_start, self.rect.centery)

        #other
        self.state = False
        self.changing = False
        self.lock_px = (width - height)/100

    def get_input(self):
        if self.rect.collidepoint(self.app.mouse_pos):
            if self.app.mouse_input[0] and not self.app.clicked:
                self.state = not self.state
                self.changing = True

    def update(self, delta):
        self.get_input()

        if self.changing:
            if self.state:
                end_pos = self.knob_end
            else:
                end_pos = self.knob_start

            x_diff = end_pos - self.knob_pos.x
            self.knob_pos.x += x_diff * self.SPEED * delta

            #check lock on
            if abs(x_diff) < self.lock_px or not (self.knob_start <= self.knob_pos.x <= self.knob_end):
                self.changing = False
                self.knob_pos.x = end_pos

            #colour
            self.colour = self.off_colour.lerp(
                self.on_colour,
                min((self.knob_pos.x - (self.rect.x+self.half_height))/self.knob_travel_dist, 1)
            )

    def draw(self):
        pygame.draw.rect(self.app.screen, self.colour, self.rect, border_radius=self.half_height)
        pygame.draw.circle(self.app.screen, WHITE, self.knob_pos, self.knob_radius)

    def get(self):
        return self.state

    def set(self, state=None, animate=True):
        if state is None:
            self.state = not self.state
        elif self.state != state:
            self.state = state
        else:
            return

        if animate:
            self.changing = True
        else:
            self.knob_pos.x = [self.knob_start, self.knob_end][self.state]
            self.colour = [self.off_colour, self.on_colour][self.state]
