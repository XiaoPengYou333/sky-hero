import pygame
from . import utils, settings, animation, level
from scripts.player import Player
import random

class Enemy(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.timer = 0
        self.max_time = random.randint(2 * settings.FPS, 5 * settings.FPS)
        self.wall = False
        self.anims = {
            'idle' : animation.Animation('graph/entities/enemy/idle', settings.SCALE_COEF, 20),
            'run' : animation.Animation('graph/entities/enemy/run', settings.SCALE_COEF, 10), 
            'jump' : animation.Animation('graph/entities/enemy/jump', settings.SCALE_COEF, 9999)
        }
        
    def flip(self):
        self.mv_l = not self.mv_l
        self.mv_r = not self.mv_r
        
    def ai(self):
        self.timer += 1
        if self.wall:
            self.flip()
        if self.timer == self.max_time:
            if self.state == 'idle':
                walk = random.randint(0, 1)
                if walk == 0:
                    self.mv_r = True
                else:
                    self.mv_l = True
            if self.state == 'run':
                self.mv_r = False
                self.mv_l = False
            self.timer = 0
            self.max_time = random.randint(2 * settings.FPS, 5 * settings.FPS)
        hb = self.get_hb()
        # pygame.draw.circle(pygame.display.get_surface(), 'red', (hb.right + 5 + level.tile_size * 2 - level.camera_x, hb.bottom + 10 - level.camera_y), 5)
        if self.time_in_air < 5:
            if self.mv_r:
                if level.check_cliff(hb.right + 5, hb.bottom + 10):
                    if level.check_cliff(hb.right + 5 + level.tile_size * 2, hb.bottom + 10):
                        self.flip()
                    else:
                        self.s_y = settings.JUMP_POWER - 1
                        self.time_in_air = 5
            if self.mv_l:
                if level.check_cliff(hb.left - 5, hb.bottom + 10):
                    if level.check_cliff(hb.left - 5 - level.tile_size * 2, hb.bottom + 10):
                        self.flip()
                    else:
                        self.s_y += settings.JUMP_POWER - 1
                        self.time_in_air = 5
    
            
        
        