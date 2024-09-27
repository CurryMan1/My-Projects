import pygame
import random
from src.utils import check_in_shape
from src.slider import Slider
from src.button import Button
from src.shape import Shape
from src.constants import WIN_SIZE, CENTER, BLACK, BLUE, WHITE, WIDTH, HEIGHT, GOLD, SHAPE_RADIUS


class App:
    ACCENT_COLOUR = BLUE

    def __init__(self):
        pygame.init()

        #display
        self.screen = pygame.display.set_mode(WIN_SIZE, pygame.SCALED | pygame.FULLSCREEN)
        pygame.display.set_caption('Chaos Game')

        self.point_to_draw = None

        #clock
        self.clock = pygame.time.Clock()

        #font
        self.title_font = pygame.font.Font('assets/font.ttf', 190)
        self.normal_font = pygame.font.Font('assets/font.ttf', 72)
        self.small_font = pygame.font.Font('assets/font.ttf', 40)

        self.running = True
        self.lclicked = False
        self.simulating = False
        self.delta = 0
        self.mouse_pos = ()
        self.mouse_input = ()
        self.keys = ()

        self.title = Button(
            self,
            'Chaos Game',
            self.title_font,
            WHITE,
            (WIDTH/2, 130)
        )

        self.sides_slider = Slider(
            self,
            (200, 960),
            200,
            50,
            3,
            20,
            'Sides'
        )

        self.start_btn = Button(
            self,
            'Start Simulation',
            self.normal_font,
            WHITE,
            (WIDTH/2, 960)
        )

        self.ratio_slider = Slider(
            self,
            (WIDTH-200, 960),
            200,
            50,
            1,
            1000,
            'Ratio',
            lambda x: x/1000
        )

        self.golden_ratio_btn = Button(
            self,
            'Golden Ratio',
            self.small_font,
            GOLD,
            (WIDTH-200, 510)
        )

        self.halfway_btn = Button(
            self,
            '0.5',
            self.small_font,
            WHITE,
            (WIDTH - 200, 570)
        )

        self.shape = Shape(
            self,
            SHAPE_RADIUS,
            CENTER
        )

        self.point_surf = pygame.Surface(WIN_SIZE, pygame.SRCALPHA)
        self.cur_point = None
        self.ratio = 1

    def run(self):
        while self.running:
            self.delta = min(self.clock.tick()/1000, 0.1)
            self.mouse_pos = pygame.mouse.get_pos()
            self.mouse_input = pygame.mouse.get_pressed()
            self.keys = pygame.key.get_pressed()

            self.screen.fill(BLACK)

            self.title.draw()

            if self.start_btn.is_clicked() and not self.lclicked:
                self.simulating = not self.simulating

                self.start_btn.change_text(f'{["Start", "Stop"][self.simulating]} Simulation')

                if self.simulating:
                    self.point_surf = pygame.Surface(WIN_SIZE, pygame.SRCALPHA)
                    self.ratio = self.ratio_slider.get()

                    #get edges from shape
                    edges = self.shape.get_edges()

                    in_shape = False
                    while not in_shape:
                        #pick random point
                        point = pygame.Vector2(CENTER) + (
                            random.randint(-SHAPE_RADIUS, SHAPE_RADIUS),
                            random.randint(-SHAPE_RADIUS, SHAPE_RADIUS)
                        )

                        in_shape = check_in_shape(point, edges)
                        if in_shape:
                            self.cur_point = point

                else:
                    self.cur_point = None

            self.start_btn.draw()

            if not self.simulating:
                self.sides_slider.update()
            self.sides_slider.draw()

            if not self.simulating:
                self.ratio_slider.update()
            self.ratio_slider.draw()

            if self.golden_ratio_btn.is_clicked():
                self.ratio_slider.set_value(0.618)
            self.golden_ratio_btn.draw()

            if self.halfway_btn.is_clicked():
                self.ratio_slider.set_value(0.5)
            self.halfway_btn.draw()

            self.shape.update(self.sides_slider.get())
            self.shape.draw()

            #draw dots if simulating
            if self.simulating:
                random_vertex = self.shape.get_random()

                diff = self.cur_point - random_vertex

                self.cur_point -= diff * self.ratio

                pygame.draw.circle(self.point_surf, BLUE, self.cur_point, 1)

            self.screen.blit(self.point_surf, (0, 0))

            #handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.sides_slider.increment(1)
                        self.ratio_slider.increment(1)
                    if event.key == pygame.K_LEFT:
                        self.sides_slider.increment(-1)
                        self.ratio_slider.increment(-1)

            #update self.lclicked
            if self.mouse_input[0]:
                self.lclicked = True
            else:
                self.lclicked = False

            pygame.display.flip()

    def stop(self):
        self.running = False


if __name__ == '__main__':
    app = App()
    app.run()
    pygame.quit()
