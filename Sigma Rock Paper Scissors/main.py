import pygame
from src.tools.constants import WIN_SIZE
from src.tools.utils import load_img, load_imgs
from src.tools.state_enum import States
from src.states.start import Start
from src.states.game import Game
from src.states.pause import Pause
from src.states.settings import Settings


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
        self.title_font = pygame.font.Font('assets/fonts/smooth.ttf', 240)
        self.normal_font = pygame.font.Font('assets/fonts/smooth.ttf', 72)
        self.small_font = pygame.font.Font('assets/fonts/smooth.ttf', 60)

        #images
        self.background = load_img('background.jpeg')
        self.characters = load_imgs('characters', True, 0.4) #only works because they are in alphabetical order

        #states
        self.states = {
            States.START: Start(self),
            States.SETTINGS: Settings(self),
            States.GAME: Game(self),
            States.PAUSE: Pause(self)
        }

        self.current_state = self.states[States.START]

        #game vars
        self.running = True
        self.restart = False
        self.can_click = True
        self.delta = 0
        self.mouse_pos = ()
        self.mouse_input = ()

    def run(self):
        while self.running:
            self.delta = min(self.clock.tick()/1000, 0.1)
            self.mouse_pos = pygame.mouse.get_pos()

            mouse_input = pygame.mouse.get_pressed()
            if self.can_click:
                self.mouse_input = mouse_input
            else:
                self.mouse_input = (0, 0, 0)
                if not mouse_input[0]:
                    self.can_click = True

            #handle events
            for event in pygame.event.get():
                self.current_state.handle_event(event)
                if event.type == pygame.QUIT:
                    self.running = False

            #blit bg
            self.screen.blit(self.background, (0, 0))

            #update and draw state
            self.current_state.update()
            self.current_state.draw()

            pygame.display.flip()

    def change_state(self, state):
        self.can_click = False

        self.current_state = self.states[state]
        if state == States.START:
            self.states[States.GAME].ending = False

    def get_state(self, state):
        return self.states[state]

    def stop(self):
        self.running = False


if __name__ == '__main__':
    app = App()
    app.run()
    pygame.quit()
