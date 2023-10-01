import pygame

class Player(pygame.sprite.Sprite):
    ANIMATION_DELAY = 3
    GRAVITY = 4

    def __init__(self, x: int, y: int, animations: dict):
        super().__init__()

        #animation
        self.animations = animations
        self.cur_animation = 'idle'
        self.direction = 'right'
        self.animation_count = 0

        #movement
        self.x_vel = 0
        self.y_vel = 0

        #display
        self.image = self.animations[f'{self.cur_animation}_{self.direction}'][self.animation_count % self.ANIMATION_DELAY]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.cur_animation = 'jump'
        if keys[pygame.K_LEFT]:
            self.direction = 'left'
        if keys[pygame.K_RIGHT]:
            self.direction = 'right'

        #change animation
        if self.animation_count < len(self.animations[f'{self.cur_animation}_{self.direction}']) * self.ANIMATION_DELAY-1:
            self.animation_count += 1
        else:
            self.animation_count = 0

        self.image = self.animations[f'{self.cur_animation}_{self.direction}'][self.animation_count // self.ANIMATION_DELAY]
        self.rect = self.image.get_rect()
