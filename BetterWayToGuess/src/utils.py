import pygame
import json
from os import listdir


class JSON:
    def __init__(self, filename: str, new_data=None):
        self.filename = filename

        if new_data:
            self.data = new_data
            self.update()
        else:
            self.data = self.load()

    def load(self):
        with open(self.filename, 'r') as f:
            data = json.load(f)
            return data

    def update(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def __repr__(self):
        return json.dumps(self.data, indent=4)

    def __getitem__(self, item):
        value = self.data[item]
        if isinstance(value, dict) or isinstance(value, list):
            return JSONProxy(self, self.data, item)
        return value

    def __setitem__(self, item, value):
        self.data[item] = value
        self.update()


class JSONProxy:
    def __init__(self, parent, data, key):
        self.parent = parent
        self.data = data #parent data
        self.key = key

    def __getitem__(self, item):
        value = self.data[self.key][item]
        if isinstance(value, dict) or isinstance(value, list):
            return JSONProxy(self.parent, self.data[self.key], item)
        return value

    def __setitem__(self, item, value):
        self.data[self.key][item] = value
        self.parent.update()

    def __repr__(self):
        return json.dumps(self.data[self.key], indent=4)


def load_img(path, transparent=False, scale=None, rotate=None):
    img = pygame.image.load(path)

    if scale:
        img = pygame.transform.smoothscale_by(img, scale)

    if rotate:
        img = pygame.transform.rotate(img, rotate)

    if transparent:
        img = img.convert_alpha()
    else:
        img = img.convert()

    return img


def load_imgs(path, transparent=False, scale=None, rotate=None):
    images = []

    for file in listdir(path):
        img = load_img(f'{path}/{file}', transparent, scale, rotate)
        images.append(img)

    return images


def round_to_multiple(number, multiple):
    return multiple * round(number / multiple)
