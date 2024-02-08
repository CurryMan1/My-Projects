import pygame
from src.constants import WIN_SIZE
from src.utils import load_img
from src.state_enum import States
from src.states.start import Start


class App:
    def __init__(self):
        pygame.init()

        #display
        self.screen = pygame.display.set_mode(WIN_SIZE, pygame.SCALED | pygame.FULLSCREEN)
        pygame.display.set_caption('Sigma Rock Paper Scissors')
        pygame.display.set_icon(load_img('icon.jpg'))

        #clock
        self.clock = pygame.time.Clock()

        #font
        self.title_font = pygame.font.Font('assets/fonts/smooth.ttf', 200)
        self.normal_font = pygame.font.Font('assets/fonts/smooth.ttf', 60)

        #states
        self.states = {
            States.START: Start(self)
        }

        self.current_state = self.states[States.START]

        #game vars
        self.running = True
        self.restart = False
        self.delta = 0
        self.mouse_pos = ()
        self.mouse_input = ()

    def run(self):
        while self.running:
            self.delta = min(self.clock.tick()/1000, 0.1)
            self.mouse_pos = pygame.mouse.get_pos()
            self.mouse_input = pygame.mouse.get_pressed()

            #handle events
            for event in pygame.event.get():
                self.current_state.handle_event(event)
                if event.type == pygame.QUIT:
                    self.running = False

            #update and draw state
            self.current_state.update()
            self.current_state.draw()

            pygame.display.flip()

    def stop(self):
        self.running = False


if __name__ == '__main__':
    app = App()
    app.run()
    pygame.quit()
