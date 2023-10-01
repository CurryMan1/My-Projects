#modules
import pygame
import json
from math import ceil
from os import listdir
from os.path import join

#files
from button import Button
from player import Player

#initialise pygame
pygame.init()

#music
pygame.mixer.init()
pygame.mixer.music.load(join('assets', 'Sound', 'Mystery.mp3'))
pygame.mixer.music.play(-1)

#display
FPS = 60
WIDTH, HEIGHT = 1000, 800

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

pygame.display.set_caption('Dimension')

#img
title = pygame.transform.scale_by(pygame.image.load(join('assets', 'Menu', 'Text', 'title.png')), 10)
bg = pygame.transform.scale_by(pygame.image.load(join('assets', 'Background', 'bg.jpg')), 0.4)

play_img = pygame.transform.scale_by(pygame.image.load(join('assets', 'Menu', 'Buttons', 'Play.png')), 5)
levels_img = pygame.transform.scale_by(pygame.image.load(join('assets', 'Menu', 'Buttons', 'Levels.png')), 5)
mb_img = pygame.transform.scale_by(pygame.image.load(join('assets', 'Menu', 'Levels', 'MenuBox.png')), 10)
back_img = pygame.image.load(join('assets', 'Menu', 'Buttons', 'Back.png'))

def load_animations(path, direction=False):
    animations = {}
    sheets = listdir(path)
    for sheet in sheets:
        #base image
        sprite_sheet = pygame.image.load(f'{path}/{sheet}')
        #str
        sheet = sheet.replace('.png', '')
        #list of all images IN base image
        sheet_list = []

        for i in range(int(sprite_sheet.get_width() / 32)):
            surface = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * 32, 0, 32, 32)
            surface.blit(sprite_sheet, (0, 0), rect)
            sheet_list.append(pygame.transform.scale2x(surface))
        if direction:
            flipped_sheet_list = [pygame.transform.flip(f, True, False) for f in sheet_list]

            animations[sheet + '_right'] = sheet_list
            animations[sheet + '_left'] = flipped_sheet_list
        else:
            animations[sheet] = sheet_list

    return animations


class Game():
    def __init__(self):
        self.data = json.load(open(join('assets', 'Data', 'levels.json'), 'r'))
        self.chosen_character = 'PinkMan'

        self.player = Player(0, 0, load_animations(join('assets', 'MainCharacters', self.chosen_character), True))
        self.player_group = pygame.sprite.GroupSingle()
        self.player_group.add(self.player)

        self.start()

    def start(self):
        play_btn = Button(int(WIDTH/2 - play_img.get_width()),
                          int(HEIGHT/2),
                          play_img)

        levels_btn = Button(int(WIDTH / 2),
                            int(HEIGHT / 2),
                            levels_img)


        while 1:
            CLOCK.tick(FPS)

            #blit
            SCREEN.blit(bg, (-150, 0))
            SCREEN.blit(title, (int(WIDTH/2 - title.get_width()/2), int(HEIGHT/2)-150))

            if play_btn.is_clicked(SCREEN):
                self.go_level()

            if levels_btn.is_clicked(SCREEN):
                self.choose_level()

            #event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit

            pygame.display.update()

    def choose_level(self):
        back_button = Button(0, 0, back_img, 6)

        mouse_off = False

        #level_btns
        level_btns = []
        for y in range(5):
            for x in range(10):
                level_no = f'{y*10 + (x + 1):02}'
                level_img = pygame.image.load(join('assets', 'Menu', 'Levels', f'{level_no}.png'))
                button = Button(x*90 + 50, y*90 + 175, level_img, 4.5)
                level_btns.append(button)

        #loop
        while 1:
            CLOCK.tick(FPS)

            #bg
            SCREEN.blit(bg, (-150, 0))

            SCREEN.blit(mb_img, (25, 145))

            if pygame.mouse.get_pressed()[0] == 0:
                mouse_off = True

            #level_btns
            for i, level in enumerate(level_btns):
                #draw button and check if clicked
                if level.is_clicked(SCREEN):
                    if mouse_off:
                        self.go_level(i+1)

            if back_button.is_clicked(SCREEN):
                self.start()

            #event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit

            pygame.display.update()

    def go_level(self, level=None):


        #game loop
        while 1:
            CLOCK.tick(FPS)

            #bg
            for x in range(0, ceil(WIDTH/64)*64, 64):
                for y in range(0, ceil(HEIGHT/64)*64, 64):
                    SCREEN.blit(pygame.image.load(join('assets', 'Background', 'Brown.png')), (x, y))

            self.player_group.draw(SCREEN)
            self.player_group.update()

            #event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit

            pygame.display.update()

if __name__ == "__main__":
    g = Game()