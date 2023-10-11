import pygame

class MenuBox():
    def __init__(self, x: int, y: int, width: int, height: int):
        if width % 50 != 0 or height % 50 != 0:
            raise ValueError("Values must be divisible by 50")

        #setup
        self.pos = (x, y)

        width //= 10
        height //= 10

        corner = pygame.image.load('assets/Menu/MenuBox/corner.jpg')
        edge = pygame.image.load('assets/Menu/MenuBox/edge.jpg')
        self.image = pygame.surface.Surface((width, height))

        #draw menubox
        self.image.fill((145, 145, 145))
        corner_no = 0
        angles = [-90, 180, 90, -90]
        #no idea why this angle thing works but it does!
        for i in range(2):
            x = i*(width-5)
            y = i*(height-5)
            self.image.blit(corner, (0, y))
            for j in range(width//5 - 2):
                self.image.blit(edge, ((j+1)*5, y))

            corner = pygame.transform.rotate(corner, angles[corner_no])
            edge = pygame.transform.rotate(edge, 90)
            corner_no += 1

            self.image.blit(corner, (width-5, y))
            for k in range(height//5 - 2):
                self.image.blit(edge, (x, (k+1)*5))

            corner = pygame.transform.rotate(corner, angles[corner_no])
            edge = pygame.transform.rotate(edge, 90)
            corner_no += 1

        #save menubox
        self.image = pygame.transform.scale_by(self.image, 10)

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.image, self.pos)
