import pygame
import random
from src.state_enum import States
from src.obstacles.movement import MovementObstacle
from src.utils import JsonManager
from src.constants import HEIGHT, RED, WHITE, OBSTACLES_PATH, MESSAGES_PATH
from src.player import Player
from src.die import Die
from src.grid import Grid
from src.button import Button
from src.pop_up import PopUp
from src.states.base import BaseState


class Game(BaseState):    
    def __init__(self, app):
        super().__init__(app)

        self.app = app

        self.title = Button(
            app,
            'Y10 Test',
            app.title_font,
            RED,
            (460, 240)
        )

        self.grid = Grid(app, 7)

        #files
        self.obstacles_data = JsonManager.load(OBSTACLES_PATH)
        self.messages_data = JsonManager.load(MESSAGES_PATH)

        self.restart()

    def restart(self):
        self.turn = 0
        self.game_over = False
        
        #popups
        self.pop_up = None
        self.new_popup("start")

        #obstacles
        self.obstacles = []
        self.load_obstacles()

        #players
        self.players = [
            Player(self.app, self.grid.get_pos(0), 1),
            Player(self.app, self.grid.get_pos(0), 2)
        ]
        
        self.current_player = self.players[self.turn]

        self.last_move = 0

        #dice
        self.dice = [
            Die(self, (270, 560)),
            Die(self, (650, 560))
        ]

        self.roll_btn = Button(
            self.app,
            'Roll!',
            self.app.big_font,
            RED,
            (460, 920)
        )

        self.reset_btn = Button(
            self.app,
            'Reset Game',
            self.app.subtitle_font,
            WHITE,
            (120, HEIGHT-30)
        )

        for p in self.players:
            p.squeeze()
        
    def update(self, delta):
        can_click = True
        if self.pop_up:
            if (update_val := self.pop_up.update()) == 'close':
                self.pop_up = None
            elif update_val == 'collide':
                can_click = False
        
        if not self.game_over:
            if self.current_player.update(delta) == 'at goal':
                #check win
                if self.current_player.square == self.grid.cell_num-1:
                    self.game_over = True
                    self.new_popup('win')
                    return

                #check obstacles interactions
                for o in self.obstacles:
                    if o.player_interact(self.current_player):
                        o.influence_player(self.current_player)
                        return
                    
                #check squeeze
                if self.players[0].square == self.players[1].square:
                    for p in self.players:
                        p.squeeze()            
                        
                self.roll_btn.toggle_enable()
                    
                self.turn = 1-self.turn
                self.current_player = self.players[self.turn]
                
        
            if self.roll_btn.is_clicked(
                self.app.mouse_input, self.app.mouse_pos
            ) and not self.app.lclicked and can_click:
                
                self.roll_btn.toggle_enable()
                
                total, double = self.get_dice_roll()
                self.last_move = total
                if double:
                    self.new_popup('double')
                
                self.current_player.rect.center = self.grid.get_pos(self.current_player.square)

                self.current_player.change_square(total)
            
                #change sq
                self.current_player.move_to(self.grid.get_pos(self.current_player.square))
                self.players[not self.turn].rect.center = self.grid.get_pos(
                    self.players[not self.turn].square
                )

        if self.reset_btn.is_clicked(
            self.app.mouse_input, self.app.mouse_pos
        ) and not self.app.lclicked:
            self.restart()
            
    def draw(self):
        self.title.draw()
        self.grid.draw()

        self.roll_btn.draw()
        self.reset_btn.draw()

        for d in self.dice:
            d.draw()

        for o in self.obstacles:
            o.draw()

        for p in self.players:
            p.draw()

        if self.pop_up:
            self.pop_up.draw()

    def get_dice_roll(self):
        total = 0
        r1 = None
        double = False
        for d in self.dice:
            d.roll()
            
            if r1:
                if r1 == d.get():
                    double = True
                total += r1+d.get()
            else:
                r1 = d.get()

        if double:
            total = -total
                
        return total, double

    def load_obstacles(self):
        #type
        for t in self.obstacles_data.keys():
            if t == 'movement':
                for start_sq, end_sq in self.obstacles_data['movement']:
                    o = MovementObstacle(self.app, start_sq, end_sq, self.grid)
                    self.obstacles.append(o)
            #if you have time add more obstacle types

    def new_popup(self, key=None, size=None):
        message = None
        
        if key:
            message, size = self.messages_data[key]
            if key == 'start':
                message = message.format(str(self.grid.cell_num))
            elif key == 'double':
                message = message.format(
                    str(self.turn+1),
                    str(self.turn+1),
                    str(abs(self.last_move))
                )
            elif key == 'win':
                message = message.format(str(self.turn+1))
        elif not size:
            return

        pop_up = PopUp(self.app, size)

        if message:
            b = Button(
                pop_up,
                message,
                self.app.normal_font,
                WHITE,
                pygame.Vector2(size)/2
            )
            pop_up.update_surf(b)
        
        self.pop_up = pop_up
        
        return pop_up

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.change_state(States.START)

