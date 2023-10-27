#modules
import pygame
import webbrowser
import random
from math import ceil
#files
from utils import *
from entities import *
from ui import *

pygame.init()
pygame.mouse.set_visible(False)

FPS = 60
WIDTH, HEIGHT = 1500, 900
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAY = pygame.surface.Surface((WIDTH, HEIGHT))
pygame.display.set_caption('Space Game idk')

MAX_ROCKS = 20

#functions
def calculate_kb(pos1, pos2, power):
    #get pos difference between mouse and player
    x, y = pos1[0] - pos2[0], pos1[1] - pos2[1]

    #calculate ratio
    total = abs(x) + abs(y)
    base = power/total

    return base*x, base*y

def get_new_rock(player, rocks):
    while True:
        size = random.randint(3, 12)
        rock = Rock(random.randint(-Rock.BOUND, WIDTH + Rock.BOUND),
             random.randint(-Rock.BOUND, HEIGHT + Rock.BOUND),
             random.randrange(360),
             size,
             size*10,
             load_imgs(f'rocks/rock{random.randint(1, 2)}', True, size))

        if not (pygame.sprite.spritecollideany(rock, rocks, pygame.sprite.collide_mask)
        or pygame.sprite.collide_rect(rock, player)):
            break

    return rock

class Game():
    def __init__(self):
        #player
        images = [load_img('spaceship/off.png', True, 3), load_img('spaceship/on.png', True, 3)]
        self.player = Spaceship(WIDTH/2, HEIGHT/2, images)

        #load sounds
        self.gunshot = load_sound('gunshot.mp3', 0.025)
        self.ship_explosion = load_sound('ship_explosion.mp3', 0.125)
        self.rock_explosion = load_sound('rock_explosion.mp3', 0.05)

        #group
        self.bullet_group = []
        self.rock_group = []
        self.coin_group = []

        #bg
        self.bgs = [load_img('starfield1.png', True, 15, 90 * r) for r in range(3)]
        self.bg_tiles = [[] for i in self.bgs]  #layers for parallax effect
        self.bg_w, self.bg_h = self.bgs[0].get_rect().size
        self.bg_dimensions = [ceil(WIDTH / self.bg_w) + 1, ceil(HEIGHT / self.bg_h) + 1]#0 is x, 1 is y

        for i in range(len(self.bgs)): #for each layer
            for x in range(self.bg_dimensions[0]):
                for y in range(self.bg_dimensions[1]):
                    self.bg_tiles[i].append([(x-1)*self.bg_w+(i*50), (y-1)*self.bg_h+(i*50), random.choice(self.bgs)]) #randomise stars

        #rock_group
        for i in range(MAX_ROCKS):
            rock = get_new_rock(self.player, self.rock_group)
            self.rock_group.append(rock)

        #particles [pos, velocity, timer, speed, colour]
        self.particles = []

        #other
        self.coin_img = load_img('coin.png', True)
        self.crosshair = load_img('crosshair.png', True, 3)
        self.coins = 0
        self.shop_shown = False

        self.main()

    def main(self):
        screen_shake = 0

        sliding_m = SlidingMenu(WIDTH / 2, HEIGHT, WIDTH - 50, 210, DARK_BLUE, WHITE, 10, [])
        shop_btn = Button(WIDTH - 120, 10, 110, 50, DARK_BLUE, WHITE, 7, 'SHOP', 30, WHITE)
        while True:
            CLOCK.tick(FPS)

            #mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_btns = pygame.mouse.get_pressed()
            keys = pygame.key.get_pressed()

            if (keys[pygame.K_SPACE] or mouse_btns[2]) or mouse_btns[0]:
                if not self.player.on_cooldown:
                    if keys[pygame.K_SPACE] or mouse_btns[2]:
                        self.player.x_vel, self.player.y_vel = \
                            calculate_kb(self.player.rect.center, mouse_pos, self.player.ENGINE_POWER)
                        self.player.og_img = self.player.images[1]

                #shoot bullet?
                if mouse_btns[0]:
                    if self.player.shooting_delay == self.player.last_shot:
                        bullet = Bullet(*self.player.rect.center,
                                        *calculate_kb(pygame.mouse.get_pos(), self.player.rect.center, self.player.BULLET_SPEED),
                                        self.player.angle, COFFEE_BLUE)
                        #play gunshot
                        self.gunshot.play()
                        self.bullet_group.append(bullet)
                        self.player.last_shot = 0

            player_x_vel, player_y_vel = self.player.x_vel, self.player.y_vel

            #UPDATE AND DRAW

            #bg
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

                    self.bg_tiles[i][j] = [x + player_x_vel/(i+2), y + player_y_vel/(i+2), bg]

                    DISPLAY.blit(bg, (x, y))

            #bullet_group
            for bullet in self.bullet_group:
                if bullet.update(WIDTH, HEIGHT, player_x_vel, player_y_vel):
                    self.bullet_group.remove(bullet)
                bullet.draw(DISPLAY)

            #rock_group
            for rock in self.rock_group:
                condition_of_rock = rock.update(WIDTH, HEIGHT, player_x_vel, player_y_vel)
                if condition_of_rock:
                    if condition_of_rock == 'dead':
                        self.add_particles(rock.rect.center, 100, 10, 60, 0.3, [RED, ORANGE, YELLOW])
                        self.rock_explosion.play()

                        self.add_coins(rock.rect.center, rock.size, rock.size)

                    self.rock_group.remove(rock)
                    self.rock_group.append(get_new_rock(self.player, self.rock_group))
                rock.draw(DISPLAY)

            #coin_group
            for coin in self.coin_group:
                condition_of_coin = coin.update(WIDTH, HEIGHT, player_x_vel, player_y_vel)
                if condition_of_coin:
                    self.coin_group.remove(coin)

                coin.draw(DISPLAY)

            #player
            self.player.update()
            self.player.draw(DISPLAY)

            #particles
            for particle in self.particles:
                particle[0][0] += particle[1][0] + player_x_vel
                particle[0][1] += particle[1][1] + player_y_vel
                particle[2] -= particle[3]

                pygame.draw.rect(DISPLAY, particle[4],
                                 pygame.rect.Rect(*particle[0], particle[2] * 3, particle[2] * 3))
                if particle[2] <= 0:
                    self.particles.remove(particle)

            #ui
            draw_text(str(self.coins), PIXEL_FONT, YELLOW, 15, 10, 50, DISPLAY)

            sliding_m.update(DISPLAY, HEIGHT)
            if shop_btn.is_clicked(DISPLAY):
                print('clicked')
                sliding_m.toggle()

            #crosshair
            DISPLAY.blit(self.crosshair, (mouse_pos[0]-self.crosshair.get_width()/2, mouse_pos[1]-self.crosshair.get_height()/2))

            #COLLISIONS

            #bullet_group-rock_group
            for bullet, rocks in pygame.sprite.groupcollide(self.bullet_group, self.rock_group, False, False, pygame.sprite.collide_mask).items():
                self.bullet_group.remove(bullet)
                self.add_particles(bullet.rect.center, 20, 3, 20, 0.1, [COFFEE_BLUE])
                for rock in rocks:
                    rock.hit(self.player.damage)

            #player-rock_group
            collided_rock = pygame.sprite.spritecollideany(self.player, self.rock_group, pygame.sprite.collide_mask)
            if collided_rock:
                screen_shake = 20
                self.player.on_cooldown = True
                self.player.x_vel, self.player.y_vel = calculate_kb(collided_rock.rect.center, self.player.rect.center, 10)

            #player-coin_group
            collided_coins = pygame.sprite.spritecollide(self.player, self.coin_group, False, pygame.sprite.collide_mask)
            for coin in collided_coins:
                self.coin_group.remove(coin)
                self.coins += 1

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

    def add_particles(self, pos, number, size, vel, speed, colours):
        for i in range(number):
            self.particles.append(
                [list(pos), [random.randrange(vel) / 10 - vel/20, random.randrange(vel) / 10 - vel/20],
                 random.randrange(size), speed, random.choice(colours)])

    def add_coins(self, pos, number, max_vel):
        for i in range(number):
            coin = Coin(pos[0], pos[1], self.coin_img, max_vel)
            self.coin_group.append(coin)

if __name__ == '__main__':
    g = Game()
