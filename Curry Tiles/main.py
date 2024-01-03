import pygame

pygame.init()

WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
display = pygame.surface.Surface((WIDTH, HEIGHT))


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        ############################
        screen.blit(display, (0, 0))
        pygame.display.update()


if __name__ == '__main__':
    main()
