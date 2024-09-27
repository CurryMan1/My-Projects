import pygame as pg
from random import randint

pg.init()
clock = pg.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Flappy Bird')

#font
font = pg.font.SysFont("Arial", 60)

#colour
white = (255, 255, 255)

#game vars
score = 0
ground_scroll = 0
speed = 4
pipe_gap = 150
pipe_frequency = 1750 #milliseconds
last_pipe = pg.time.get_ticks() - pipe_frequency
flying = False
game_over = False
passed_pipe = False

#images
bg = pg.image.load('bg.png')
ground = pg.image.load('ground.png')
restart = pg.image.load('restart.png')

pg.display.set_icon(pg.image.load('bird1.png'))

def draw_text(text, font, fg, x, y):
    img = font.render(text, True, fg)
    screen.blit(img, (x, y))

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height/2)
    score = 0
    return score

#sprites
class Bird(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = []
        self.index = 0
        self.counter = 0
        self.flap_cooldown = 5
        for num in range(1, 4):
            img = pg.image.load(f'bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.gravity = 0
        self.clicked = False

    def update(self):
        #gravity
        if flying:
            self.gravity += 0.5
            if self.gravity > 10:
                self.gravity = 15
            if self.rect.bottom < 768:
                self.rect.y += int(self.gravity)

        if not game_over:
            #jump
            if pg.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.gravity = -10
                self.clicked = True
            if pg.mouse.get_pressed()[0] == 0:
                self.clicked = False

            #animation
            self.counter += 1

            if self.counter > self.flap_cooldown:
                self.counter = 0
                self.index = (self.index + 1)%len(self.images)
            self.image = self.images[self.index]

            #tilt
            self.image = pg.transform.rotate(self.images[self.index], -2*(self.gravity))
        else:
            self.image = pg.transform.rotate(self.images[self.index], -90)

class Pipe(pg.sprite.Sprite):
    def __init__(self, x, y, position):
        super().__init__()
        self.image = pg.image.load('pipe.png')
        self.rect = self.image.get_rect()
        #position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pg.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap/2)]
        elif position == -1:
            self.rect.topleft = [x, y + int(pipe_gap/2)]

    def update(self):
        self.rect.x -= speed
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def draw(self) -> bool: #returns if button has been pressed
        action = False

        #get mouse pos
        pos = pg.mouse.get_pos()

        #mouse over button?
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1:
                action = True

        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

bird_group = pg.sprite.GroupSingle()
pipe_group = pg.sprite.Group()

flappy = Bird(100, int(screen_height/2))
bird_group.add(flappy)

button = Button(screen_width // 2 - 50, screen_height // 2 - 100, restart)

run = True
while run:
    clock.tick(fps)

    #background
    screen.blit(bg, (0,0))

    #pipe
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    #draw ground
    screen.blit(ground, (ground_scroll, 768))

    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
        and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
        and not passed_pipe:
            passed_pipe = True
        if passed_pipe:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                passed_pipe = False

    draw_text(str(score), font, white, int(screen_width / 2), 20)

    #hit pipe?
    if pg.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    #hit ground?
    if flappy.rect.bottom > 768:
        game_over = True
        flying = False

    if not game_over and flying == True:
        #new pipes
        time_now = pg.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = randint(-200, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        #scrolling ground
        ground_scroll -= speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update()

    #check for game over
    if game_over:
        clicked = button.draw()
        if clicked:
            game_over = False
            score = reset_game()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True

    pg.display.update()

pg.quit()
