#modules
import pygame
import json
from math import ceil
from os import listdir
from os.path import join

#files
from button import *
from player import *
from objects import *
from menubox import *

#initialise pygame
pygame.init()

#music
pygame.mixer.init()
pygame.mixer.music.load(join('assets', 'Sound', 'Mystery.mp3'))
#pygame.mixer.music.play(-1)

#____display____
FPS = 60
WIDTH, HEIGHT = 1000, 800
BLOCK_SIZE = 96

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

pygame.display.set_caption('Dimension')

#____img____
title = pygame.transform.scale_by(pygame.image.load(join('assets', 'Menu', 'Extra', 'title.png')), 10)
bg = pygame.transform.scale_by(pygame.image.load(join('assets', 'Background', 'bg.jpg')), 0.4)

#buttons
play_btn_img = pygame.transform.scale_by(pygame.image.load(join('assets', 'Menu', 'Buttons', 'Play.png')), 5)
levels_btn_img = pygame.transform.scale_by(pygame.image.load(join('assets', 'Menu', 'Buttons', 'Levels.png')), 5)
settings_btn_img = pygame.transform.scale_by(pygame.image.load(join('assets', 'Menu', 'Buttons', 'Settings.png')), 4)
back_btn_img = pygame.transform.scale_by(pygame.image.load(join('assets', 'Menu', 'Buttons', 'Back.png')), 6)
right_btn_img = pygame.transform.scale_by(pygame.image.load(join('assets', 'Menu', 'Buttons', 'Right.png')), 5)
left_btn_img = pygame.transform.scale_by(pygame.image.load(join('assets', 'Menu', 'Buttons', 'Left.png')), 5)

#art
choose_character = pygame.transform.scale_by(pygame.image.load(join('assets', 'Menu', 'Extra', 'choose_character.png')), 6)
choose_level = pygame.transform.scale_by(pygame.image.load(join('assets', 'Menu', 'Extra', 'choose_level.png')), 10)

def load_animations(path, width, height, direction=False, scale=None, choosing_player=False):
    animations = {}
    if choosing_player:
        sheets = ['idle.png']
    else:
        sheets = listdir(path)

    for sheet in sheets:
        #base image
        sprite_sheet = pygame.image.load(f'{path}/{sheet}')
        #str
        sheet = sheet.replace('.png', '')
        #list of all images IN base image
        sheet_list = []

        for i in range(int(sprite_sheet.get_width() / width)):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sheet_list.append(pygame.transform.scale2x(surface))

        if scale:
            sheet_list = [pygame.transform.scale_by(f, scale) for f in sheet_list]

        if choosing_player:
            return sheet_list

        if direction:
            flipped_sheet_list = [pygame.transform.flip(f, True, False) for f in sheet_list]

            animations[sheet + '_right'] = sheet_list
            animations[sheet + '_left'] = flipped_sheet_list
        else:
            animations[sheet] = sheet_list

    return animations

def get_block(size, level):
    size = int(size/2)
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, (level//20)*64, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def horizontal_collide(player, objects, dx):
    player.move(dx, 0)

    collided_objects = pygame.sprite.spritecollide(player, objects, False, pygame.sprite.collide_mask)

    player.move(-dx,  0)
    return collided_objects

def vertical_collide(player, objects, dy):
    collided_objects = pygame.sprite.spritecollide(player, objects, False, pygame.sprite.collide_mask)
    for obj in collided_objects:
        if dy > 0:
            #on top
            player.rect.bottom = obj.rect.top
            player.jump_count = 0
            if obj.name == 'trampoline':
                player.y_vel = obj.power
                player.jump_count = 2
                obj.cur_animation = 'jump'
            else:
                player.y_vel = 0
        elif dy < 0:
            #hit head
            player.rect.top = obj.rect.bottom
            player.y_vel *= -1

    return collided_objects

class Game():
    def __init__(self):
        self.data = json.load(open(join('assets', 'Data', 'level1.json'), 'r'))
        self.chosen_character = 'NinjaFrog'

        animations = load_animations(join('assets', 'MainCharacters', self.chosen_character), 32, 32, True)

        self.player = Player(200, 0, animations)
        self.player_group = pygame.sprite.GroupSingle()
        self.player_group.add(self.player)

        self.start()

    def start(self):
        play_btn = Button(int(WIDTH / 2 - play_btn_img.get_width()),
                          int(HEIGHT/2),
                          play_btn_img)

        levels_btn = Button(int(WIDTH / 2),
                            int(HEIGHT / 2),
                            levels_btn_img)

        settings_btn = Button(WIDTH - settings_btn_img.get_width(),
                              0,
                              settings_btn_img)

        while 1:
            CLOCK.tick(FPS)

            #blit
            SCREEN.blit(bg, (-150, 0))
            SCREEN.blit(title, (int(WIDTH/2 - title.get_width()/2), int(HEIGHT/2)-150))

            if play_btn.is_clicked(SCREEN):
                self.go_level(0)

            if levels_btn.is_clicked(SCREEN):
                self.choose_level()

            if settings_btn.is_clicked(SCREEN):
                self.settings()

            #event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit

            pygame.display.update()

    def choose_level(self):
        back_button = Button(0, 0, back_btn_img)

        #menubox
        mb = MenuBox(25, 25, 950, 750)

        #level_btns
        level_btns = []
        for y in range(5):
            for x in range(10):
                level_no = f'{y*10 + (x + 1):02}'
                level_img = pygame.transform.scale_by(pygame.image.load(join('assets', 'Menu', 'Levels', f'{level_no}.png')), 4.5)
                button = Button(x*90 + 52, y*90 + 300, level_img)
                level_btns.append(button)

        #loop
        while 1:
            CLOCK.tick(FPS)

            #bg
            SCREEN.blit(bg, (-150, 0))

            #menubox
            mb.draw(SCREEN)

            #choose_level.png
            SCREEN.blit(choose_level, (int(WIDTH/2-choose_level.get_width()/2), 62))

            #level_btns
            for i, level in enumerate(level_btns):
                #draw button and check if clicked
                if level.is_clicked(SCREEN):
                    self.go_level(i)

            if back_button.is_clicked(SCREEN):
                self.start()

            #event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit

            pygame.display.update()

    def settings(self):
        '''
        NEXT TIME
        -Make a volume slider
        '''

        #back button
        back_button = Button(0, 0, back_btn_img)

        #menubox
        mb = MenuBox(25, 25, 950, 750)

        #players
        main_characters = ['MaskDude', 'NinjaFrog', 'PinkMan', 'VirtualGuy']
        hidden_index = 3
        main_char_animations = {}
        for char in main_characters:
            main_char_animations[char] = load_animations(join('assets', 'MainCharacters', char), 32, 32, False, 3, True)

        shown_players = ['MaskDude', 'NinjaFrog', 'PinkMan']
        positions = [(150, 170), (WIDTH/2-160, 170), (WIDTH-342, 170)]
        animation_count = 0
        delay = 3

        #size middle char
        main_char_animations[shown_players[1]] = [pygame.transform.scale_by(img, 5/3) for img in main_char_animations['NinjaFrog']]

        #left, right arrows
        left_btn = Button(250, 370, left_btn_img)
        right_btn = Button(WIDTH-250-right_btn_img.get_width(), 370, right_btn_img)

        #loop
        while 1:
            CLOCK.tick(FPS)

            #bg
            SCREEN.blit(bg, (-150, 0))

            #menubox
            mb.draw(SCREEN)

            #choose_character.png
            SCREEN.blit(choose_character, (int(WIDTH/2-choose_character.get_width()/2), 62))

            #buttons
            if left_btn.is_clicked(SCREEN):
                shown_players = shown_players[1:] + [main_characters[hidden_index]]
                hidden_index = (hidden_index+1)%4

                main_char_animations[shown_players[0]] = [pygame.transform.scale_by(img, 3/5) for img in main_char_animations[shown_players[0]]]
                main_char_animations[shown_players[1]] = [pygame.transform.scale_by(img, 5/3) for img in main_char_animations[shown_players[1]]]

            if right_btn.is_clicked(SCREEN):
                shown_players = [main_characters[hidden_index]] + shown_players[:-1]
                hidden_index = (hidden_index - 1) % 4

                main_char_animations[shown_players[2]] = [pygame.transform.scale_by(img, 3/5) for img in main_char_animations[shown_players[2]]]
                main_char_animations[shown_players[1]] = [pygame.transform.scale_by(img, 5/3) for img in main_char_animations[shown_players[1]]]

            #animation
            for i, player in enumerate(shown_players):
                SCREEN.blit((main_char_animations[player][animation_count//delay]), positions[i])

            if animation_count < len(main_char_animations['MaskDude'])*delay-1:
                animation_count += 1
            else:
                animation_count = 0

            if back_button.is_clicked(SCREEN):
                #change character
                self.chosen_character = shown_players[1]
                animations = load_animations(join('assets', 'MainCharacters', self.chosen_character), 32, 32, True)
                self.player.animations = animations

                self.start()

            #event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit

            pygame.display.update()

    def go_level(self, level):
        objects = pygame.sprite.Group()
        blocks = pygame.sprite.Group()
        trampolines = pygame.sprite.Group()

        #blocks
        for i in range(30):
            blocks.add(Block(i * BLOCK_SIZE - 1000, HEIGHT - BLOCK_SIZE, BLOCK_SIZE, get_block(BLOCK_SIZE, level), 'block'))

        blocks.add(Block(400, HEIGHT-(4*BLOCK_SIZE), BLOCK_SIZE, get_block(BLOCK_SIZE, level), 'block'))

        #trampoline
        animations = load_animations(join('assets', 'Traps', 'Trampoline'), 28, 28, False, 2)
        trampoline = Trampoline(40, HEIGHT - BLOCK_SIZE - 28*4, 28, 28, animations, -28, 'trampoline')
        trampolines.add(trampoline)

        #bg
        bg = pygame.surface.Surface((WIDTH, HEIGHT))
        segment = pygame.image.load(join('assets', 'Background', listdir(join('assets', 'Background'))[level%7+1]))
        for x in range(0, ceil(WIDTH / 64) * 64, 64):
            for y in range(0, ceil(HEIGHT / 64) * 64, 64):
                bg.blit(segment, (x, y))

        #final group
        objects.add(blocks, trampolines)

        #area size
        scroll_area_size = 200

        #game loop
        while 1:
            CLOCK.tick(FPS)

            SCREEN.blit(bg, (0, 0))

            #offset
            offset_x = 0

            objects.draw(SCREEN)
            objects.update()

            self.player_group.draw(SCREEN)
            self.player_group.update()

            #collisions
            vertical_collided = vertical_collide(self.player, objects, self.player.y_vel)

            collide_left = horizontal_collide(self.player, objects, -self.player.SPEED * 2)
            collide_right = horizontal_collide(self.player, objects, self.player.SPEED * 2)

            #keys, animations
            keys = pygame.key.get_pressed()
            self.player.x_vel = 0
            self.player.cur_animation = 'idle'

            if keys[pygame.K_LEFT] and not collide_left:
                self.player.cur_animation = 'run'
                self.player.direction = 'left'

                self.player.x_vel = -self.player.SPEED

            elif keys[pygame.K_RIGHT] and not collide_right:
                self.player.cur_animation = 'run'
                self.player.direction = 'right'

                self.player.x_vel = self.player.SPEED


            if self.player.y_vel > self.player.GRAVITY*3:
                self.player.cur_animation = 'fall'
            elif self.player.y_vel < 0: #and NOT EQUAL TO 0
                self.player.cur_animation = 'jump'

            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                if not self.player.clicked and self.player.jump_count < 2:
                    self.player.y_vel = self.player.JUMP_POWER
                    self.player.clicked = True
                    self.player.jump_count += 1
            else:
                self.player.clicked = False

            #offset
            x_pos = self.player.rect.centerx
            if (x_pos < scroll_area_size and self.player.x_vel < 0)\
                    or\
                (x_pos > WIDTH-scroll_area_size and self.player.x_vel > 0):

                offset_x = -self.player.x_vel
                self.player.x_vel = 0

            #update offset for each obj
            for obj in objects:
                obj.offset_x = offset_x

            #event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit

            pygame.display.update()

if __name__ == "__main__":
    g = Game()