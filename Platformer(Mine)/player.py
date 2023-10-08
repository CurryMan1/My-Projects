import pygame

class Player(pygame.sprite.Sprite):
    ANIMATION_DELAY = 3
    GRAVITY = 0.9
    SPEED = 5
    JUMP_POWER = -17

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
        self.clicked = False
        self.jump_count = 2

        #display
        self.image = self.animations[f'{self.cur_animation}_{self.direction}'][self.animation_count % self.ANIMATION_DELAY]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

    #HANDLE COLLISIONS AND VELOCITY IN GAME LOOP
    def update(self):
        #gravity
        self.y_vel += self.GRAVITY

        #change animation
        if self.animation_count < len(self.animations[f'{self.cur_animation}_{self.direction}']) * self.ANIMATION_DELAY-1:
            self.animation_count += 1
        else:
            self.animation_count = 0

        #update image
        self.image = self.animations[f'{self.cur_animation}_{self.direction}'][self.animation_count // self.ANIMATION_DELAY]
        #update pos
        self.move(self.x_vel, self.y_vel)
        #update mask
        self.mask = pygame.mask.from_surface(self.image)
