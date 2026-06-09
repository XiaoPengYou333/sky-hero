from . import utils, settings, animation
import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.anims = {
            'idle' : animation.Animation('graph/entities/player/idle', settings.SCALE_COEF, 20),
            'run' : animation.Animation('graph/entities/player/run', settings.SCALE_COEF, 10), 
            'jump' : animation.Animation('graph/entities/player/jump', settings.SCALE_COEF, 9999)
        }
        self.mv_l = False
        self.mv_r = False
        self.dir = 'r'
        self.state = 'idle'
        self.s_y = 0
        self.gravity = 0.3
        self.time_in_air = 0
        
    def render(self, screen: pygame.Surface):
        self.anims[self.state].render(screen, self.x, self.y, self.dir)
    
    def get_hb(self):
        self.image = self.anims[f'{self.state}'].get_current_image()
        return self.image.get_rect(topleft=(self.x, self.y))
    
    def update(self):
        self.time_in_air += 1
        self.s_y += self.gravity
        self.y += self.s_y
        if self.y >= settings.SCREEN_HEIGHT - self.get_hb().height:
            self.y = settings.SCREEN_HEIGHT - self.get_hb().height
            self.s_y = 0
            self.time_in_air = 0
        if self.mv_l == True:
            self.x -= 5
            self.state = 'run'
            self.dir = 'l'
        if self.mv_r == True:
            self.x += 5
            self.state = 'run'
            self.dir = 'r'
        if self.mv_r == False and self.mv_l == False:
            self.state = 'idle'
        if self.mv_r == True and self.mv_l == True:
            self.state = 'idle'
        if self.time_in_air > 5:
            self.state = 'jump'
        self.anims[self.state].update()
            