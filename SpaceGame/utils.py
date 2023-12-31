import pygame
from os import listdir

#colour
WHITE = (255, 255, 255)
COFFEE_BLUE = (192, 255, 238)
DARK_BLUE = (28, 28, 122)
RED = (255, 0, 0)
ORANGE = (255, 115, 59)
YELLOW = (255, 255, 0)

#font
PIXEL_FONT = 'assets/other/pixel_font.ttf'

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

def draw_text(text, font, fg, x, y, size, surf, center=False, opacity=None):
    font = pygame.font.Font(font, size)
    img = font.render(text, True, fg)
    if opacity:
        img.set_alpha(opacity)

    if center:
        surf.blit(img, (x-img.get_width()/2, y-img.get_height()/2))
    else:
        surf.blit(img, (x, y))