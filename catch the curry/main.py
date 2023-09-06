import pygame
from pygame.locals import *
from random import randint

pygame.init()

clock = pygame.time.Clock()
fps = 60

falling_speed = 6
curry_frequency = 1000 #milliseconds
last_curry = 0-curry_frequency
curry_falling = False
score = 0
lives = 3

screen_width = 1700
screen_height = 900

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Catch The Curry')

#images
bg = pygame.image.load('images/bg.jpg')#1 point
heart = pygame.transform.scale(pygame.image.load('images/Heart.png'), (100, 100))
basket = pygame.image.load('images/Basket.png')
restart_btn_img = pygame.transform.scale(pygame.image.load('images/Restart.jpg'), (1080, 200))

chicken_curry = pygame.transform.scale(pygame.image.load('images/Chicken Curry.png'), (100, 61)) #3 points
mutton_curry = pygame.transform.scale(pygame.image.load('images/Mutton Curry.png'), (100, 60)) #2 points
paneer_curry = pygame.transform.scale(pygame.image.load('images/Paneer Curry.png'), (100, 58)) #1 point
curries = [paneer_curry, mutton_curry, chicken_curry]

#colour
black = (0, 0, 0)

#font
font = pygame.font.Font("C:/Users/user/Documents/Hardhik's Stuff/Random Stuff/Fonts/Futura Extra Black font.ttf", 60)
def draw_text(text, font, fg, x, y):
    img = font.render(text, True, fg)
    screen.blit(img, (x-int(img.get_width()/2), y))

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def draw(self):
        action = False

        #get mouse pos
        pos = pygame.mouse.get_pos()

        #mouse over button?
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

class Basket(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.points = randint(1, 3)
        self.image = basket
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
    def update(self):
        self.rect.x = pygame.mouse.get_pos()[0]-int(self.rect.width/2)

class Curry(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.points = randint(1, 3)
        self.image = curries[self.points-1]
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.is_touching_ground = False
    def update(self):
        self.rect.y += int(falling_speed)
        if self.rect.bottom >= screen_height:
            self.is_touching_ground = True

restart_button = Button(int((screen_width/2)-(restart_btn_img.get_width()/2)),
                        int((screen_height/2)-(restart_btn_img.get_height()/2)),
                        restart_btn_img)

basket_sprite = Basket(int(screen_width/2), 840)
basket_group = pygame.sprite.GroupSingle()
basket_group.add(basket_sprite)

curry_group = pygame.sprite.Group()

screen.blit(bg, (0, 0))

run = True
while run:
    clock.tick(fps)

    if curry_falling:
        #collisions
        if len(curry_group.sprites()) > 0:
            latest_curry = curry_group.sprites()[0]
            if pygame.sprite.groupcollide(basket_group, curry_group, False, False):
                score += latest_curry.points
                latest_curry.kill()
                if falling_speed <= 20:
                    falling_speed += 0.1
                elif curry_frequency > 400:
                    curry_frequency -= 2

            if latest_curry.is_touching_ground:
                lives -= 1
                latest_curry.kill()
                if lives == 0:
                    curry_falling = False

        #screen
        screen.blit(bg, (0, 0))
        for i in range(0, heart.get_width() * lives, heart.get_width()):
            screen.blit(heart, ((i + 10), 10))
        draw_text(f'Score: {score}', font, black, int(screen_width / 2), 20)
        basket_group.draw(screen)
        curry_group.draw(screen)

        time_now = pygame.time.get_ticks()
        if time_now - last_curry > curry_frequency:
            new_curry = Curry(randint(0, screen_width - 100), 20)
            curry_group.add(new_curry)
            last_curry = time_now

        basket_group.update()
        curry_group.update()

    elif restart_button.draw():
        curry_group.empty()
        curry_falling = True
        lives = 3
        score = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()