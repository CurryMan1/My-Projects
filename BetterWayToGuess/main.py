import pygame
from src.constants import BACKGROUND_COLOUR, WIN_SIZE
from src.state_enum import States
from src.results_generator import ResultsGenerator
from src.states.start import Start
from src.states.loading_screen import LoadingScreen
from src.states.results_displayer import ResultsDisplayer


class App:
    def __init__(self):
        pygame.init()

        #display
        self.screen = pygame.display.set_mode(WIN_SIZE, pygame.SCALED | pygame.FULLSCREEN)
        pygame.display.set_caption('BetterWayToGuess')

        #clock
        self.clock = pygame.time.Clock()

        #font
        self.title_font = pygame.font.Font('assets/Brownland.otf', 300)
        self.subtitle_font = pygame.font.Font('assets/Brownland.otf', 180)
        self.normal_font = pygame.font.Font('assets/Brownland.otf', 70)

        #game vars
        self.running = True
        self.lclicked = False
        self.delta = 0
        self.mouse_pos = pygame.Vector2(0, 0)
        self.last_mouse_pos = pygame.Vector2(0, 0)
        self.mouse_input = ()
        self.keys = ()

        self.results_generator = None
        self.results = {} # data of currently open test

        #states
        self.states = {
            States.START: Start(self),
            States.RESULTS_DISPLAYER: ResultsDisplayer(self),
            States.LOADING_SCREEN: LoadingScreen(self)
        }
        self.current_state = self.states[States.START]

    def run(self):
        while self.running:
            self.delta = min(self.clock.tick() / 1000, 0.2)
            self.last_mouse_pos = self.mouse_pos
            self.mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            self.mouse_input = pygame.mouse.get_pressed()
            self.keys = pygame.key.get_pressed()

            self.screen.fill(BACKGROUND_COLOUR)

            #update and draw state
            self.current_state.update(self.delta)
            self.current_state.draw()

            if self.mouse_input[0]:
                self.lclicked = True
            elif not self.mouse_input[0]:
                self.lclicked = False

            #handle events
            for event in pygame.event.get():
                self.current_state.handle_event(event)
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.flip()

    def generate_results(self, answers, guesses):
        self.results_generator = ResultsGenerator(answers, guesses)

    def change_state(self, state):
        self.current_state = self.states[state]

    def get_state(self, state):
        return self.states[state]

    def stop(self):
        self.running = False


if __name__ == "__main__":
    app = App()
    app.run()
    pygame.quit()
