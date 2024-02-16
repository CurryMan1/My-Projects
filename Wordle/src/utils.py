import pygame


def load_img(path, transparent=False, scale=None, rotate=None):
    img = pygame.image.load(f'assets/img/{path}')

    if scale:
        img = pygame.transform.scale_by(img, scale)

    if rotate:
        img = pygame.transform.rotate(img, rotate)

    if transparent:
        img = img.convert_alpha()
    else:
        img = img.convert()

    return img
