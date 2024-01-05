"""
This file is for write songs for the tiles.
It will write to assets/songs.json in the format
{
    "file_path":
        "notes": [timestamp, timestamp, etc.]
        "duration": duration
}
"""

import random
import pygame
import mutagen
from mutagen.mp3 import MP3
from utils import JsonManager, draw_text, SONGS_FILE, songs


#pygame setup
pygame.init()
pygame.display.set_caption('Listener')
WIDTH = 900
screen = pygame.display.set_mode((WIDTH, WIDTH))
display = pygame.Surface((WIDTH, WIDTH), pygame.SRCALPHA)
clock = pygame.time.Clock()

#other
CIRCLE_GROWTH_RATE = 1200
CIRCLE_TRANSPARENCY_RATE = 200


def main():
    clicked = True
    circles = []

    notes = []
    note_count = -1
    time_elapsed = 0

    while True:
        delta = clock.tick() / 1000  #framerate as fast as possible

        #fill screen
        screen.fill((0, 0, 0, 255))

        #get mouse clicked
        if pygame.mouse.get_pressed()[0]:
            if not clicked:
                note_count += 1
                if note_count == 0:
                    #start song
                    pygame.mixer.music.load(file_path)
                    pygame.mixer.music.play()
                else:
                    #add note
                    notes.append(time_elapsed)

                #add circ
                mouse_pos = pygame.mouse.get_pos()
                colour = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255]
                circles.append([mouse_pos, 2, colour])
            clicked = True
        else:
            clicked = False

        #draw circles
        for circle in circles:
            #change radius
            circle[1] += CIRCLE_GROWTH_RATE*delta
            circle[2][3] -= CIRCLE_TRANSPARENCY_RATE*delta

            #draw circ
            pygame.draw.circle(display, circle[2], circle[0], circle[1])
            if circle[2][3] <= 0:
                circles.remove(circle)

        #text
        if note_count < 0:
            draw_text('Click to start song', (255, 255, 255), WIDTH / 2, 30, 50, screen)
        else:
            draw_text(f'Listening...  Notes: {note_count}', (255, 255, 255), WIDTH / 2, 30, 50, screen)
            time_elapsed += delta

            if time_elapsed >= duration:
                #write into file
                songs[file_name] = {'notes': notes,
                                    'duration': duration}
                JsonManager.write(SONGS_FILE, songs)

                print('Song successfully saved!')

                raise SystemExit

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit

        ###########################
        screen.blit(display, (0, 0))
        pygame.display.update()


if __name__ == '__main__':
    #get music file
    while True:
        try:
            file_name = input('Enter Song Name (in assets/songs): ')
            file_path = f"assets/songs/{file_name}"
            audio = MP3(file_path)
            duration = audio.info.length
            print(duration)
            break
        except mutagen.MutagenError:
            print(f'"{file_name}" not found in assets/songs')

    main()
