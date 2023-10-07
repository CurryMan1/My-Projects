import pygame

class Object(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width, self.height = width, height
        self.offsetx = 0

class Block(Object):
    def __init__(self, x: int, y: int, size: int, image: pygame.surface.Surface):
        super().__init__(x, y, size, size)
        self.image = image

    def update(self):
        self.rect.y = self.rect.y
