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
            (WIDTH-200, 1020)
        )

        self.shape = Shape(
            self,
            SHAPE_RADIUS,
            CENTER
        )

    def run(self):
        while self.running:
            self.delta = min(self.clock.tick()/1000, 0.1)
            self.mouse_pos = pygame.mouse.get_pos()
            self.mouse_input = pygame.mouse.get_pressed()
            self.keys = pygame.key.get_pressed()

            self.screen.fill(BLACK)

            self.title.draw()

            self.sides_slider.update()
            self.sides_slider.draw()

            if self.start_btn.is_clicked() and not self.lclicked:
                self.simulating = True
            self.start_btn.draw()

            self.ratio_slider.update()
            self.ratio_slider.draw()

            if self.golden_ratio_btn.is_clicked():
                self.ratio_slider.set_value(0.618)
            self.golden_ratio_btn.draw()

            self.shape.update(self.sides_slider.get())
            self.shape.draw()

            #draw dots if simulating
            if self.simulating:
                #pick random point
                point = pygame.Vector2(CENTER)+(
                    random.randint(-SHAPE_RADIUS, SHAPE_RADIUS),
                    random.randint(-SHAPE_RADIUS, SHAPE_RADIUS)
                )

                self.point_to_draw = point
                #get edges from shape
                edges = self.shape.get_edges()

                #check if point is in shape
                in_shape = check_in_shape(point, edges)
                print(in_shape)
                self.simulating = False

            if self.point_to_draw:

                pygame.draw.circle(self.screen, BLUE, self.point_to_draw, 20)

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
