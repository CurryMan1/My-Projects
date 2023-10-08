import pygame

class Object(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, name: str):
        super().__init__()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.name = name
        self.width, self.height = width, height
        self.offset_x = 0

class Block(Object):
    def __init__(self, x: int, y: int, size: int, image: pygame.surface.Surface, name: str):
        self.image = image

        super().__init__(x, y, size, size, name)


    def update(self):
        self.rect.x += self.offset_x


class Trampoline(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x: int, y: int, width: int, height: int, animations: dict, power: int, name: str):
        self.animations = animations
        self.cur_animation = 'idle'
        self.animation_count = 0
        self.power = power

        self.image = self.animations[self.cur_animation][self.animation_count // self.ANIMATION_DELAY]

        super().__init__(x, y, width, height, name)

    def update(self):
        self.rect.x += self.offset_x

        if self.animation_count < len(self.animations[self.cur_animation]) * self.ANIMATION_DELAY-1:
            self.animation_count += 1
        else:
            self.animation_count = 0
            if self.cur_animation == 'jump':
                self.cur_animation = 'idle'

        #update image
        self.image = self.animations[self.cur_animation][self.animation_count // self.ANIMATION_DELAY]

