import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pygame.surface.Surface):
        super().__init__()

        self.image = image

        #rect
        self.rect = image.get_rect()
        self.rect.center = (x, y)

    def draw(self, disp: pygame.surface.Surface):
        disp.blit(self.image, (self.rect.x, self.rect.y))

class Player(Entity):
    GRAVITY = 0.15
    AIR_RESISTANCE = 0.02

    def __init__(self, x: int, y: int, image: pygame.surface.Surface):
        super().__init__(x, y, image)

        #vel
        self.x_vel, self.y_vel = 0, 0
        self.moving = False

    def update(self, s_width, s_height):
        if self.moving:
            #AIR RESISTANCE
            if self.x_vel != 0:
                multiplier = self.x_vel / abs(self.x_vel)  #1 or -1
                self.x_vel = (abs(self.x_vel) - self.AIR_RESISTANCE) * multiplier

            #GRAVITY
            if self.y_vel < 30:
                self.y_vel += self.GRAVITY

            self.rect.centerx += self.x_vel
            self.rect.centery += self.y_vel

            if self.rect.centerx > s_width or self.rect.centerx < 0:
                self.rect.centerx %= s_width

            if self.rect.centery > s_height:
                return True

class Gun(Entity):
    POWER = 20

    def __init__(self, x: int, y: int, image: pygame.surface.Surface):
        super().__init__(x, y, image)


        self.og_img = image
        self.angle = 0

    def update(self, player: Entity):
        x, y = pygame.mouse.get_pos()
        pos = pygame.math.Vector2(x, y) - self.rect.center
        self.angle = pos.angle_to((0, 0))
        self.image = pygame.transform.rotate(self.og_img, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.center = player.rect.center

class CollectableBullet(Entity):
    def __init__(self, x: int, y: int, image: pygame.surface.Surface):
        super().__init__(x, y, image)
        self.mask = pygame.mask.from_surface(self.image)

class ShootingBullet(Entity):
    SPEED = 20

    def __init__(self, x: int, y: int, ratio: tuple, multiplier: tuple, image: pygame.surface.Surface, direction: float, screen_dimensions: tuple):
        super().__init__(x, y, pygame.transform.rotate(image, direction))
        x_vel, y_vel = ratio
        m_x, m_y = multiplier
        base = self.SPEED/(x_vel + y_vel)
        self.x_vel, self.y_vel = base*x_vel*m_x, base*y_vel*m_y
        self.scr_width, self.scr_height = screen_dimensions

    def update(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
        if self.rect.x not in range(0, self.scr_width) or self.rect.y not in range(0, self.scr_height):
            self.kill()
