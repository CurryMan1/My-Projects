import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pygame.surface.Surface):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, disp: pygame.surface.Surface):
        disp.blit(self.image, (self.rect.x, self.rect.y))

    def get_bound(self, WIDTH, HEIGHT, bound):
        if self.rect.centerx not in range(-bound, WIDTH + bound
        ) or self.rect.centery not in range(-bound, HEIGHT + bound):
            return True

class Spaceship(Entity):
    ENGINE_POWER = 15
    SHOOTING_POWER = 25
    SHOOTING_DELAY = 20
    AIR_RESISTANCE = 0.95 #for timesing

    def __init__(self, x: int, y: int, images: list):
        super().__init__(x, y, images[0])
        self.mask = pygame.mask.from_surface(self.image)
        self.og_img = self.image
        self.images = images
        self.last_shot = self.SHOOTING_DELAY
        self.angle = 0
        self.x_vel, self.y_vel = 0, 0

        self.on_cooldown = False
        self.damage = 10

    def update(self):
        x, y = pygame.mouse.get_pos()
        pos = pygame.math.Vector2(x, y) - self.rect.center
        self.angle = pos.angle_to((0, 0))
        self.image = pygame.transform.rotate(self.og_img, self.angle-90)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

        self.x_vel *= self.AIR_RESISTANCE
        self.y_vel *= self.AIR_RESISTANCE

        if self.last_shot < self.SHOOTING_DELAY:
            self.last_shot += 1

        if self.og_img == self.images[1]:
            self.og_img = self.images[0]

        if self.on_cooldown:
            if abs(self.x_vel) < 1 and abs(self.y_vel) < 1:
                self.on_cooldown = False

class Bullet(Entity):
    BOUND = 100

    def __init__(self, x: int, y: int, x_vel: float, y_vel: float, angle: float):
        image = pygame.surface.Surface((20, 5), pygame.SRCALPHA)
        image.fill((192, 255, 238))
        image = pygame.transform.rotate(image, angle)
        super().__init__(x, y, image)
        self.mask = pygame.mask.from_surface(self.image)
        self.x_vel, self.y_vel = x_vel, y_vel

    def update(self, width, height, player_x_vel, player_y_vel):
        self.rect.centerx += self.x_vel + player_x_vel
        self.rect.centery += self.y_vel + player_y_vel

        if self.get_bound(width, height, self.BOUND):
            return True

class Rock(Entity):
    BOUND = 300

    def __init__(self, x: int, y: int, images: list):
        super().__init__(x, y, images[0])
        self.images = images
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 100

    def update(self, width, height, player_x_vel, player_y_vel):
        self.rect.centerx += player_x_vel
        self.rect.centery += player_y_vel

        if self.get_bound(width, height, self.BOUND):
            return True

    def hit(self, damage):
        self.health -= damage
