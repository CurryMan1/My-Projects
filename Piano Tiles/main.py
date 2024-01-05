import random, time
from ui import *

#pygame setup
pygame.init()
pygame.display.set_caption('Piano Tiles')

screen = pygame.display.set_mode((WIDTH, HEIGHT))
display = pygame.surface.Surface((WIDTH, HEIGHT))

clock = pygame.time.Clock()


class Tile(Button, pygame.sprite.Sprite):
    def __init__(self, column, height=HEIGHT/4):
        super().__init__(column*TILE_WIDTH, -height, TILE_WIDTH, height, 3, BLACK, WHITE)
        self.column = column

    def update(self, delta) -> bool:
        self.rect.y += TILE_SPEED * delta

        if self.rect.centery >= HEIGHT:
            return True


def draw_lines():
    #draw lines
    for i in range(3):
        x = TILE_WIDTH * (i + 1)
        pygame.draw.line(display, BLACK, (x, 0), (x, HEIGHT))
    #draw super line
    pygame.draw.line(display, BLACK, (0, SUPER_LINE_PX), (WIDTH, SUPER_LINE_PX))


def play(song: str):
    #groups
    tile_group = []
    splash_texts = []

    note = 0
    time_elapsed = 0
    last_column = None

    music_playing = False
    failed = False
    score = 0
    lives = 3

    clicked = False

    while True:
        #update clock and get deltaTime
        delta = clock.tick(FPS) / 1000
        time_elapsed += min(0.5, delta)

        #mouse
        mouse_click = False
        if pygame.mouse.get_pressed()[0]:
            if not clicked:
                mouse_click = True
            clicked = True
        else:
            clicked = False
        mouse_pos = pygame.mouse.get_pos()

        #check for song finish
        if time_elapsed >= songs[song]['duration']:
            return main(score)

        #check if it's time to add a tile
        if note < len(songs[song]['notes']):
            if time_elapsed >= songs[song]['notes'][note]:
                note += 1

                column = random.randint(0, 3)
                while column == last_column:
                    column = random.randint(0, 3)

                tile_group.append(Tile(column))
                last_column = column

        if time_elapsed >= DELAY and not music_playing: #delays song
            #start song
            pygame.mixer.music.load(f'assets/songs/{song}')
            pygame.mixer.music.play()

            music_playing = True

        #fill display grey
        display.fill(GREY)

        draw_lines()

        #update and draw tiles
        updated_list = tile_group[:]
        tile_clicked = False
        for tile in tile_group:
            if tile.update(delta): #means user missed tile
                splash_texts.append(['-200', tile.column*TILE_WIDTH+(TILE_WIDTH/2), HEIGHT-90, RED, 256])
                score -= 200

                updated_list.remove(tile)
                continue

            if tile.draw(display, mouse_click, mouse_pos): #means tile clicked
                tile_clicked = True

                difference = abs(tile.rect.centery - SUPER_LINE_PX)
                if difference < 100:
                    splash_texts.append(['Perfect', mouse_pos[0], mouse_pos[1], PURPLE, 256])
                    score += 60
                elif difference < 180:
                    splash_texts.append(['Great', mouse_pos[0], mouse_pos[1], BLUE, 256])
                    score += 40
                elif difference < 260:
                    splash_texts.append(['Good', mouse_pos[0], mouse_pos[1], GREEN, 256])
                    score += 20

                updated_list.remove(tile)
        tile_group = updated_list[:]
        if mouse_click and not tile_clicked:
            splash_texts.append(['-200', mouse_pos[0], mouse_pos[1], RED, 256])
            score -= 200

        updated_list = splash_texts[:]
        for sp in splash_texts:
            draw_text(sp[0], sp[3], sp[1], sp[2], 40, display, sp[4])
            sp[4] -= 12
            if sp[4] <= 0:
                updated_list.remove(sp)
        splash_texts = updated_list[:]

        ############################
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        screen.blit(display, (0, 0))
        pygame.display.update()


def main(score=0):
    song = ''
    screen_shake = 0

    while True:
        clock.tick(FPS) #delta is not needed

        #fill
        display.fill(GREY)

        #draw text
        draw_text(f'Last Score: {score}', BLACK, WIDTH / 2, 70, 60, display)

        draw_text('Enter File Name:', BLACK, WIDTH / 2, HEIGHT/2-60, 60, display)
        draw_text(song, BLACK, WIDTH/2, HEIGHT/2, 60, display)

        #handle event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if song in songs:
                        play(song)
                    else:
                        screen_shake = 20
                elif event.key == pygame.K_BACKSPACE:
                    song = song[:-1]
                else:
                    song += event.unicode

        screen_offset = [0, 0]
        if screen_shake > 0:
            screen_offset = [random.randint(-6, 6), random.randint(-6, 6)]
            screen_shake -= 1

        ############################
        screen.blit(display, screen_offset)
        pygame.display.update()


if __name__ == '__main__':
    main()
