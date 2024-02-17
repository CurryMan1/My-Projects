import pygame
import webbrowser as wb
from src.switch import Switch
from src.buttons.text_button import TextButton
from src.buttons.image_button import ImageButton
from src.constants import WIN_SIZE, WIDTH, HEIGHT, BLACK, DARK_GREY
from src.utils import load_img
from src.scenes.base import BaseScene
from src.scene_enum import Scenes


class Settings(BaseScene):
    def __init__(self, app):
        super().__init__(app)

        self.last_frame = None

        self.surface_tint = pygame.Surface(WIN_SIZE)
        self.surface_tint.fill((0, 0, 0))
        self.surface_tint.set_alpha(128)

        #menu box
        self.menu_box = pygame.Surface((900, 1000), pygame.SRCALPHA)
        self.menu_box_rect = self.menu_box.get_rect(center=(WIDTH/2, HEIGHT/2))
        pygame.draw.rect(self.menu_box, DARK_GREY, pygame.Rect((0, 0), (900, 1000)), border_radius=100)
        pygame.draw.rect(self.menu_box, BLACK, pygame.Rect((8, 8), (884, 984)), border_radius=92)

        #title
        self.title = TextButton(
            app,
            'SETTINGS',
            app.big_font,
            center=(WIDTH/2, 150)
        )

        #hard mode
        self.hard_mode_label = TextButton(
            app,
            'Hard Mode',
            app.normal_font,
            midleft=(600, 400)
        )
        self.hard_mode_switch = Switch(
            app, 180, 90,
            center=(1225, 400)
        )

        #keyboard
        self.keyboard_label = TextButton(
            app,
            'Keyboard\nInput',
            app.normal_font,
            midleft=(600, 600)
        )
        self.keyboard_switch = Switch(
            app, 180, 90,
            center=(1225, 600)
        )
        self.keyboard_switch.set(True, False)

        #github logo
        self.github_btn = ImageButton(
            app,
            load_img('github.png', True, 0.3),
            load_img('selected_github.png', True, 0.3),
            center=(WIDTH/2, 950)
        )

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.change_scene(Scenes.START)

    def update(self, delta):
        self.hard_mode_switch.update(delta)
        self.keyboard_switch.update(delta)

        if self.github_btn.is_clicked() and not self.app.clicked:
            wb.open('https://github.com/CurryMan1')

    def draw(self):
        #background
        self.app.screen.blit(self.last_frame, (0, 0))
        self.app.screen.blit(self.surface_tint, (0, 0))

        #menubox
        self.app.screen.blit(self.menu_box, self.menu_box_rect)

        #title
        self.title.draw()

        #hard mode
        self.hard_mode_label.draw()
        self.hard_mode_switch.draw()

        #keyboard
        self.keyboard_label.draw()
        self.keyboard_switch.draw()

        #github
        self.github_btn.draw()

    def set_last_frame(self, frame):
        self.last_frame = frame
