#modules
import pygame
import webbrowser
import random
from math import ceil
from os import listdir
#files
from entities import *
from button import *

pygame.init()

FPS = 60
WIDTH, HEIGHT = 1500, 900
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAY = pygame.surface.Surface((WIDTH, HEIGHT))
pygame.display.set_caption('Space Game idk')

#functions
def calculate_kb(pos1, pos2, power):
    #get pos difference between mouse and player
    x, y = pos1[0] - pos2[0], pos1[1] - pos2[1]

    #calculate ratio
    total = abs(x) + abs(y)
    base = power/total

    return base*x, base*y

def load_img(path, transparent=False, scale=None, rotate=None):
    img = pygame.image.load('assets/img/'+path)

    if scale:
        img = pygame.transform.scale_by(img, scale)

    if rotate:
        img = pygame.transform.rotate(img, rotate)

    if transparent:
        img = img.convert_alpha()
    else:
        img = img.convert()

    return img

def load_imgs(path, transparent=False, scale=None, rotate=None):
    images = []
    for file in listdir(f'assets/img/{path}'):
        img = load_img(f'{path}/{file}', transparent, scale, rotate)
        images.append(img)

    return images

def load_sound(path, volume=None):
    sound = pygame.mixer.Sound('assets/sound/'+path)
    if volume:
        sound.set_volume(volume)

    return sound

class Game():
    def __init__(self):
        #player
        images = [load_img('spaceship/off.png', True, 3), load_img('spaceship/on.png', True, 3)]
        self.player = Spaceship(WIDTH/2, HEIGHT/2, images)

        #load sounds
        self.gunshot = load_sound('gunshot.mp3', 0.2)

        #bg
        self.bgs = [load_img('starfield1.png', True, 15, 90*r) for r in range(4)]
        self.bg_tiles = [[] for i in self.bgs]  #layers for parallax effect

        self.bullets = []
        self.rocks = []

        self.bg_w, self.bg_h = self.bgs[0].get_rect().size

        #0 is x, 1 is y
        self.bg_dimensions = [ceil(WIDTH/self.bg_w)+1, ceil(HEIGHT/self.bg_h)+1]

        for i in range(len(self.bgs)): #for each layer
            for x in range(self.bg_dimensions[0]):
                for y in range(self.bg_dimensions[1]):
                    self.bg_tiles[i].append([(x-1)*self.bg_w+(i*50), (y-1)*self.bg_h+(i*50), random.choice(self.bgs)]) #randomise stars

        self.main()

    def main(self):
        rock = Rock(50, 50, load_imgs('rocks/rock1', True, 10))
        self.rocks.append(rock)

        screen_shake = 0
        while True:
            CLOCK.tick(FPS)

            #mouse
            mouse_btns = pygame.mouse.get_pressed()
            keys = pygame.key.get_pressed()

            if (keys[pygame.K_SPACE] or mouse_btns[2]) or mouse_btns[0]:

                if not self.player.on_cooldown:
                    if keys[pygame.K_SPACE] or mouse_btns[2]:
                        self.player.x_vel, self.player.y_vel = \
                            calculate_kb(self.player.rect.center, pygame.mouse.get_pos(), self.player.ENGINE_POWER)
                        self.player.og_img = self.player.images[1]

                #shoot bullet?
                if mouse_btns[0]:
                    if self.player.SHOOTING_DELAY == self.player.last_shot:
                        bullet = Bullet(*self.player.rect.center,
                                        *calculate_kb(pygame.mouse.get_pos(), self.player.rect.center, self.player.SHOOTING_POWER),
                                        self.player.angle)
                        #play gunshot
                        self.gunshot.play()
                        self.bullets.append(bullet)
                        self.player.last_shot = 0

            player_x_vel, player_y_vel = self.player.x_vel, self.player.y_vel

            #update and draw everything

            #draw bg
            DISPLAY.fill((0, 0, 0))
            for i, layer in enumerate(self.bg_tiles):
                for j, coords_and_bg in enumerate(layer):
                    x, y, bg = coords_and_bg

                    diff_x = x - WIDTH
                    diff_y = y - HEIGHT

                    #works regardless of window size (if FOV is bigger than tile)
                    if 0 < diff_x:
                        x = WIDTH - (self.bg_dimensions[0] * self.bg_w) + diff_x
                    elif x < WIDTH - (self.bg_dimensions[0] * self.bg_w):
                        diff_x = x - (WIDTH - (self.bg_dimensions[0] * self.bg_w))
                        x = WIDTH + diff_x

                    if 0 < diff_y:
                        y = HEIGHT - (self.bg_dimensions[1] * self.bg_h) + diff_y
                    elif y < HEIGHT - (self.bg_dimensions[1] * self.bg_h):
                        diff_y = y - (HEIGHT - (self.bg_dimensions[1] * self.bg_h))
                        y = HEIGHT + diff_y

                    self.bg_tiles[i][j] = [x + player_x_vel/(i+1), y + player_y_vel/(i+1), bg]

                    DISPLAY.blit(bg, (x, y))

            #bullets
            for bullet in self.bullets:
                if bullet.update(WIDTH, HEIGHT, player_x_vel, player_y_vel):
                    self.bullets.remove(bullet)
                bullet.draw(DISPLAY)

            #rocks
            for rock in self.rocks:
                if rock.update(WIDTH, HEIGHT, player_x_vel, player_y_vel):
                    self.rocks.remove(rock)
                rock.draw(DISPLAY)


            #COLLISIONS
            #bullets-rocks
            for bullet, rocks in pygame.sprite.groupcollide(self.bullets, self.rocks, False, False, pygame.sprite.collide_mask).items():
                self.bullets.remove(bullet)
                for rock in rocks:
                    rock.hit(self.player.damage)

            #player-rocks
            collided_rock = pygame.sprite.spritecollideany(self.player, self.rocks, pygame.sprite.collide_mask)
            if collided_rock:
                screen_shake = 20
                self.player.on_cooldown = True
                self.player.x_vel, self.player.y_vel = calculate_kb(collided_rock.rect.center, self.player.rect.center, 10)

            #draw player
            self.player.update()
            self.player.draw(DISPLAY)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

            screen_offset = [0, 0]
            if screen_shake > 0:
                screen_offset = [random.randint(-6, 6), random.randint(-6, 6)]
                screen_shake -= 1

            SCREEN.blit(DISPLAY, screen_offset)

            pygame.display.update()

if __name__ == '__main__':
    g = Game()

