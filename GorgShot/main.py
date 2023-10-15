#modules
import pygame
import webbrowser
from random import randint
#files
from entities import *
from button import *

'''
This is a ripoff heavily inspired by Barji's BuckShot from the Youtube Video - "2 Python Developers Vs $1000".
By no means is this an original idea, I am copying it for fun.
'''

#initialise
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.load('assets/sound/background_song.mp3')
pygame.mixer.music.play(-1)

#display
WIDTH, HEIGHT = 1200, 900
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAY = pygame.surface.Surface((WIDTH, HEIGHT))
pygame.display.set_caption('GorgShot')
pygame.display.set_icon(pygame.image.load('assets/img/gorg.png'))

FPS = 60
CLOCK = pygame.time.Clock()
FONT = "assets/other/Futura Extra Black font.ttf"
DARK_GREY = (150, 150, 150)
LIGHT_GREY = (190, 190, 190)
GREEN = (100, 200, 150)

def draw_text(text, font, fg, x, y, size, surf, opacity=None):
    font = pygame.font.Font(font, size)
    img = font.render(text, True, fg)
    if opacity:
        img.set_alpha(opacity)
    surf.blit(img, (x-img.get_width()//2, y-img.get_height()//2))

class Game:
    def __init__(self):
        #img
        self.gorg = pygame.transform.scale_by(pygame.image.load('assets/img/gorg.png').convert_alpha(), 0.4)
        self.gun_img = pygame.transform.scale_by(pygame.image.load('assets/img/gun.png').convert_alpha(), 0.2)
        self.bullet_img = pygame.transform.scale_by(pygame.image.load('assets/img/bullet.png').convert_alpha(), 0.1)

        self.volume_on_img = pygame.transform.scale_by(pygame.image.load('assets/img/volume_on.png').convert_alpha(), 0.5)
        self.volume_off_img = pygame.transform.scale_by(pygame.image.load('assets/img/volume_off.png').convert_alpha(), 0.5)

        self.github_logo_img = pygame.transform.scale_by(pygame.image.load('assets/img/github.png').convert_alpha(), 0.5)

        #game vars
        self.ammo = 0 #one extra
        self.score = 0
        self.last_score = None
        self.clicked = False

        #sprites
        self.player = Player(WIDTH // 2, HEIGHT // 2 - 90, self.gorg)
        self.gun = Gun(WIDTH//2, HEIGHT//2, self.gun_img)

        self.collectable_bullets = pygame.sprite.Group()
        self.shot_bullets = pygame.sprite.Group()

        self.randomise_bullets()

        #splash text list
        self.splash_texts = []

        #sound
        self.gunshot = pygame.mixer.Sound('assets/sound/gunshot.mp3')
        self.gun_empty = pygame.mixer.Sound('assets/sound/gun_empty.wav')
        self.grunt = pygame.mixer.Sound('assets/sound/grunt.mp3')
        self.gunshot.set_volume(0.5)
        self.gun_empty.set_volume(0.5)

        #buttons
        self.volume_btn = Button(10, 10, self.volume_on_img)
        self.github_btn = Button(WIDTH-self.github_logo_img.get_width()-10, 10, self.github_logo_img)

        #start
        self.start()

    def randomise_bullets(self):
        for i in range(3):
            bullet_ = CollectableBullet(randint(60, WIDTH-60), randint(60, HEIGHT-60), self.bullet_img)
            self.collectable_bullets.add(bullet_)

    def start(self):
        while 1:
            CLOCK.tick(FPS)

            #fill screen
            DISPLAY.fill(DARK_GREY)

            #buttons
            if self.volume_btn.is_clicked(DISPLAY):
                if self.volume_btn.image == self.volume_on_img:
                    self.volume_btn.image = self.volume_off_img
                    self.volume_btn.rect = self.volume_btn.image.get_rect(topleft=(10, 10))
                    self.gunshot.set_volume(0)
                    self.gun_empty.set_volume(0)
                    self.grunt.set_volume(0)
                    pygame.mixer.music.pause()
                else:
                    self.volume_btn.image = self.volume_on_img
                    self.volume_btn.rect = self.volume_btn.image.get_rect(topleft=(10, 10))
                    self.gunshot.set_volume(0.5)
                    self.gun_empty.set_volume(0.5)
                    self.grunt.set_volume(1)
                    pygame.mixer.music.unpause()

            if self.github_btn.is_clicked(DISPLAY):
                webbrowser.open('https://github.com/CurryMan1/My-Projects')

            #draw titles
            if self.last_score != None:
                draw_text(str(self.last_score), FONT, LIGHT_GREY, WIDTH // 2, HEIGHT // 2-200, 100, DISPLAY)
            draw_text('GorgShot', FONT, LIGHT_GREY, WIDTH // 2, HEIGHT // 2, 150, DISPLAY)
            draw_text('Press Any Key To Start', FONT, LIGHT_GREY, WIDTH // 2, HEIGHT // 2+130, 50, DISPLAY)

            self.player.update(WIDTH, HEIGHT)
            self.player.draw(DISPLAY)

            self.gun.update(self.player)
            self.gun.draw(DISPLAY)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                elif event.type == pygame.KEYDOWN:
                    self.main()

            SCREEN.blit(DISPLAY, (0, 0))

            pygame.display.update()

    def main(self):
        self.player.moving = True
        self.ammo = 3
        while 1:
            CLOCK.tick(FPS)

            #fill screen
            DISPLAY.fill(DARK_GREY)

            #draw no of ammo
            draw_text(str(self.ammo), FONT, LIGHT_GREY, WIDTH // 2, HEIGHT // 2, 350, DISPLAY)

            self.collectable_bullets.draw(DISPLAY)

            for i, sp_text in enumerate(self.splash_texts):
                text, opacity, x, y = sp_text
                if opacity <= 0:
                    del self.splash_texts[i]
                    continue
                else:
                    self.splash_texts[i] = (text, opacity-5, x, y)

                draw_text(text, FONT, GREEN, x, y, 50, DISPLAY, opacity)


            is_dead = self.player.update(WIDTH, HEIGHT)
            self.player.draw(DISPLAY)

            self.shot_bullets.update()
            self.shot_bullets.draw(DISPLAY)

            self.gun.update(self.player)
            self.gun.draw(DISPLAY)

            if is_dead:
                #reset
                self.player.moving = False
                self.player.rect.center = (WIDTH//2, HEIGHT//2-90)
                self.player.x_vel, self.player.y_vel = 0, 0
                self.ammo = 4
                self.last_score = self.score
                self.score = 0
                self.grunt.play()
                self.shot_bullets.empty()
                self.collectable_bullets.empty()
                self.randomise_bullets()
                self.start()
                return

            player_collided_bullets = pygame.sprite.spritecollide(self.player, self.collectable_bullets, True, pygame.sprite.collide_mask)
            shot_collided_bullets = pygame.sprite.groupcollide(self.shot_bullets, self.collectable_bullets, True, True, pygame.sprite.collide_mask)
            for i in player_collided_bullets + list(shot_collided_bullets.keys()):
                self.ammo += 1
                bullet_ = CollectableBullet(randint(60, WIDTH-60), randint(60, HEIGHT-100), self.bullet_img)
                self.collectable_bullets.add(bullet_)
                self.splash_texts.append(('+1', 256, i.rect.centerx, i.rect.centery))

            if pygame.mouse.get_pressed()[0]:
                if not self.clicked:
                    if self.ammo > 0:
                        #sound
                        self.gunshot.play()

                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        player_x, player_y = self.player.rect.centerx, self.player.rect.centery

                        #get pos difference between mouse and player
                        x, y = player_x-mouse_x, player_y-mouse_y

                        m_x, m_y = abs(y) and x / abs(x) or 0, abs(y) and y / abs(y) or 0 #1 or -1

                        #set positive (for ratios)
                        x, y = abs(x), abs(y)

                        #calculate ratio
                        total = x+y
                        base = self.gun.POWER / total

                        #make bullet
                        s_b = ShootingBullet(*self.player.rect.center, (x,y), (-m_x, -m_y), pygame.transform.scale_by(self.bullet_img, 0.5), self.gun.angle-90, (WIDTH, HEIGHT))
                        self.shot_bullets.add(s_b)

                        #set vars
                        self.player.x_vel, self.player.y_vel = base*x*m_x*1.2, base*y*m_y*0.7
                        self.ammo -= 1
                        self.score += 1
                    else:
                        self.gun_empty.play()

                self.clicked = True
            else:
                self.clicked = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

            SCREEN.blit(DISPLAY, (0, 0))

            pygame.display.update()

if __name__ == '__main__':
    g = Game()