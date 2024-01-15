import pygame
import json

#mixer init
pygame.mixer.init()

#game consts
WIDTH, HEIGHT = 650, 850
FPS = 60
TILE_WIDTH = WIDTH/4
TILE_SPEED = 700 #per second

#get delay
SUPER_LINE_PERCENT = 0.65
SUPER_LINE_PX = HEIGHT * SUPER_LINE_PERCENT
DELAY = SUPER_LINE_PX / TILE_SPEED

#font
FONT = "assets/Futura Extra Black font.ttf"

#colour
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
WHITE = (255, 255, 255)
RED = (140, 0, 0)
PURPLE = (53, 0, 73)
GREEN = (0, 122, 0)
BLUE = (0, 0, 122)


#draw text function
def draw_text(text, fg, x, y, size, surf, opacity=None):
    font = pygame.font.Font(FONT, size)
    img = font.render(text, True, fg)

    if opacity:
        img.set_alpha(opacity)

    surf.blit(img, (x-img.get_width()//2, y-img.get_height()//2)) #centered


class JsonManager:
    @staticmethod
    def load(file: str) -> dict:
        with open(file, 'r') as f:
            data = json.load(f)
            f.close()
            return data

    @staticmethod
    def write(file: str, content: dict) -> None:
        with open(file, 'w') as f:
            json.dump(content, f, indent=4)
            f.close()


#files
SONGS_FILE = 'assets/songs.json'
songs = JsonManager.load(SONGS_FILE)
