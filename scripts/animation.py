import pygame
from . import utils

class Animation:
    def __init__(self, path, scale, timer):
        self.images = utils.load_images(path, scale)
        self.fliped_images = []
        for image in self.images:
            image = pygame.transform.flip(image, True, False)
            image.set_colorkey((0, 0, 0))
            self.fliped_images.append(image)
        self.index = 0
        self.timer = timer
        self.str_timer = timer
    
    def render(self, screen: pygame.Surface, x, y, dir):
        if dir == 'r':
            screen.blit(self.images[self.index], (x, y))
        else:
            screen.blit(self.fliped_images[self.index], (x, y))
    
    def get_current_image(self):
        return self.images[self.index]
    
    def update(self):
        self.timer -= 1
        if self.timer == 0:
            self.timer = self.str_timer
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        