import pygame

class Button():
    def __init__(self, x: int, y: int, image: pygame.surface.Surface, scale_factor: float=1):
        self.image = pygame.transform.scale_by(image, scale_factor)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.can_click = False

    def is_clicked(self, screen: pygame.surface.Surface): #draws button too
        clicked = False
        
        if self.rect.collidepoint((pygame.mouse.get_pos())):
            if pygame.mouse.get_pressed()[0] == 0:
                self.can_click = True
            elif self.can_click:
                clicked = True
        else:
            self.can_click = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return clicked
