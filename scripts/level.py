import pygame
import pickle
from . import utils

tiles = {}
camera_x = 0
camera_y = 0
tile_size = 128
resources = {
    'decor' : utils.load_images('graph/resources/decor', tile_size / 16),
    'grass' : utils.load_images('graph/resources/grass', tile_size / 16),
    'large_decor' : utils.load_images('graph/resources/large_decor', tile_size / 16),
    'spawners' : utils.load_images('graph/resources/spawners', tile_size / 16),
    'stone' : utils.load_images('graph/resources/stone', tile_size / 16),
}

def get_player_cor():
    for tile in tiles.values():
        if tile['type'] == 'spawners' and tile['variant'] == 0:
            return (tile['x'], tile['y'])

def load_level(number):
    global tiles, p_counter
    try:
        f = open(f'levels/level {number}', 'rb')
        tiles, p_counter = pickle.load(f)
        f.close()
    except:
        pass
def render(screen:pygame.Surface):
    for tile in tiles.values():
        screen.blit(resources[tile['type']][tile['variant']], (tile['x'] - camera_x, tile['y'] - camera_y))