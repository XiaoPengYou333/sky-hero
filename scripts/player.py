from . import utils, settings, animation, level
import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.anims = {
            'idle' : animation.Animation('graph/entities/player/idle', settings.SCALE_COEF, 20),
            'run' : animation.Animation('graph/entities/player/run', settings.SCALE_COEF, 10), 
            'jump' : animation.Animation('graph/entities/player/jump', settings.SCALE_COEF, 9999),
            'wall_slide' : animation.Animation('graph/entities/player/wall_slide', settings.SCALE_COEF, 9999),
            'slide' : animation.Animation('graph/entities/player/slide', settings.SCALE_COEF, 9999)
        }
        self.mv_l = False
        self.mv_r = False
        self.dir = 'r'
        self.state = 'idle'
        self.s_y = 0
        self.gravity = 0.3
        self.time_in_air = 0
        self.slide = False
        slide_timer = 0
        
    def render(self, screen: pygame.Surface, camera_x, camera_y):
        self.anims[self.state].render(screen, self.x - camera_x, self.y - camera_y, self.dir)
        if settings.DEBUG_MODE == True:
            pygame.draw.rect(screen, 'red', self.get_hb().move(-camera_x, -camera_y), 10)
    
    def get_hb(self) -> pygame.Rect:
        self.image = self.anims[f'{self.state}'].get_current_image()
        return self.image.get_rect(topleft=(self.x, self.y)).inflate(-50, 0)

    def death(self):
        self.x = level.p_cors[0]
        self.y = level.p_cors[1]
        self.s_y = 0
    def collision_x(self):
        self.wall = False 
        p_hb = self.get_hb()
        collisions = level.get_collisions(p_hb)
        for hb in collisions:
            if p_hb.colliderect(hb):
                self.wall = True
                if self.mv_r:
                    p_hb.right = hb.left
                if self.mv_l:
                    p_hb.left = hb.right
                self.x = p_hb.x - 25
                
    def collision_y(self):
        p_hb = self.get_hb()
        collisions = level.get_collisions(p_hb)
        for hb in collisions:
            if p_hb.colliderect(hb):
                if self.s_y >= 0:
                    p_hb.bottom = hb.top
                    self.time_in_air = 0
                    self.s_y = 0
                elif self.s_y <= 0:
                    p_hb.top = hb.bottom
                self.y = p_hb.y
    
    def update(self):
        self.time_in_air += 1
        self.s_y += self.gravity
        self.y += self.s_y
        self.collision_y()
        if not self.slide:
            if self.mv_l == True:
                self.x -= 5
                self.collision_x()
                self.state = 'run'
                self.dir = 'l'
            if self.mv_r == True:
                self.x += 5
                self.collision_x()
                self.state = 'run'
                self.dir = 'r'
            if self.mv_r == False and self.mv_l == False:
                self.state = 'idle'
            if self.mv_r == True and self.mv_l == True:
                self.state = 'idle'
            if self.time_in_air > 5:
                self.state = 'jump'
        if self.slide:
            self.state = 'slide'
        self.anims[self.state].update()
            