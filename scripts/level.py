import pygame
import pickle
from . import utils, settings

p_counter = 0
tiles = {}
camera_x = 0
camera_y = 0
tile_size = 180
resources = {
    'decor' : utils.load_images('graph/resources/decor', tile_size / 16),
    'dirt' : utils.load_images('graph/resources/dirt', tile_size / 16),
    'large_decor' : utils.load_images('graph/resources/large_decor', tile_size / 16),
    'spawners' : utils.load_images('graph/resources/spawners', tile_size / 16),
    'stone' : utils.load_images('graph/resources/stone', tile_size / 16),
    'barier' : utils.load_images('graph/resources/barier', tile_size / 16)
}
print(resources['decor'])
def get_collisions(hb:pygame.Rect) -> list[pygame.Rect]:
    hbs = []
    for tile in tiles.values():
        #поменять в будущем
        if tile['type'] in {'stone', 'dirt'}:
            b_hb = pygame.rect.Rect(tile['x'] * tile_size, tile['y'] * tile_size, tile_size, tile_size)
            if hb.colliderect(b_hb):
                hbs.append(b_hb)
    return hbs
def get_player_cor():
    global p_cors
    for key, tile in tiles.items():
        if tile['type'] == 'spawners' and tile['variant'] == 0:
            p_cors = (tile['x'] * tile_size, tile['y'] * tile_size)
            del tiles[key]
            return p_cors
        
def get_barrier_collisions(hb:pygame.Rect) -> bool:
    left = hb.left // tile_size
    right = hb.right // tile_size + 1
    top = hb.top // tile_size
    bottom = hb.bottom // tile_size + 1
    for x in range(left, right + 1):
        for y in range(top, bottom + 1):
            if (x, y) in barriers:
                barrier_hb = pygame.rect.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                if barrier_hb.colliderect(hb):
                    return True
    return False            
                
        
def get_enemies():
    enemy_cors = []
    for key, tile in tiles.copy().items():
        if tile['type'] == 'spawners' and tile['variant'] == 1:
            enemy_cors.append((key[0] * tile_size, key[1] * tile_size))
            del tiles[key]
    return enemy_cors

def load_level(number, game:bool):
    global tiles, p_counter
    try:
        f = open(f'levels/level {number}', 'rb')
        tiles, p_counter = pickle.load(f)
        f.close()
        for cors, tile in tiles.items():
            gx, gy = cors
            tile['x'] = gx
            tile['y'] = gy
        if game:
            load_barriers()
    except Exception as e:
        print(e)
    
def load_barriers():
    global barriers
    barriers = set()
    for tile in tiles.copy().values():
        if tile['type'] == 'barier':
            barriers.add((tile['x'], tile['y']))
            del tiles[(tile['x'], tile['y'])]

            
def render(screen:pygame.Surface):
    for tile in tiles.values():
        try:
            screen.blit(
                resources[tile['type']][tile['variant']],
                (tile['x'] * tile_size - camera_x, tile['y'] * tile_size - camera_y)
            )
        except IndexError:
            print((tile['type'], tile['variant']))

def check_cliff(x, y):
    x = x // tile_size
    y = y // tile_size
    for i in range(settings.CLIFF_HEIGHT):
        if (x, y + i) in tiles:
            return False
    return True

def check_block(x, y):
            pass