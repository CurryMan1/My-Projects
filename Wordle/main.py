import pygame
from src.constants import WIN_SIZE, BLACK
from src.scene_enum import Scenes
from src.scenes.start import Start


class App:
    def __init__(self):
        pygame.init()

        #display
        self.screen = pygame.display.set_mode(WIN_SIZE, pygame.SCALED | pygame.FULLSCREEN)

        #font
        self.title_font = pygame.font.Font('assets/fonts/wordle_font.otf', 240)
        self.normal_font = pygame.font.Font('assets/fonts/wordle_font.otf', 72)

        #states
        self.scenes = {
            Scenes.START: Start(self)
        }

        self.current_state = self.scenes[Scenes.START]

        #game vars
        self.running = True
        self.restart = False
        self.can_click = True
        self.delta = 0
        self.mouse_pos = ()
        self.mouse_input = ()

    def run(self):
        while self.running:
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
            self.screen.fill(BLACK)

            #update and draw state
            self.current_state.update()
            self.current_state.draw()

            pygame.display.flip()

    def change_state(self, state):
        self.can_click = False

        self.current_state = self.states[state]

    def get_state(self, state):
        return self.states[state]

    def stop(self):
        self.running = False


if __name__ == '__main__':
    app = App()
    app.run()
    pygame.quit()
