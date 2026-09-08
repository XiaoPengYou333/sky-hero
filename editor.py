import pygame
from scripts import utils, level
from scripts.level import *
import pickle
import random

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
mv_right = False
mv_left = False
mv_down = False
mv_up = False
del_count = 0
counter = 0
df_counter = 0
resource_names = list(resources.keys())
current_resource_index = 0 
variant = 0
p_counter = 0
def render_grid():
    x_start = level.camera_x // tile_size * tile_size - level.camera_x
    y_start = level.camera_y // tile_size * tile_size - level.camera_y
    for x in range(x_start, x_start + screen.get_width() + tile_size, tile_size):
        pygame.draw.line(screen, (140, 140, 140), (x, 0), (x, screen.get_height()))
    for y in range(y_start, y_start + screen.get_height() + tile_size, tile_size):
        pygame.draw.line(screen, (140, 140, 140), (0, y), (screen.get_width(), y))
        
def save():
    f = open('levels/level 0', 'wb')
    pickle.dump((level.tiles, level.p_counter), f)
    f.close()

def transform():
    global tiles, variant
    for cors, tile in level.tiles.items():
        gx, gy = cors
        if tile['type'] in ('dirt', 'stone'):
            left = False
            right = False
            down = False
            top = False
            if (gx - 1, gy) in level.tiles and level.tiles[(gx - 1, gy)]['type'] == tile['type']:
                left = True
            if (gx + 1, gy) in level.tiles and level.tiles[(gx + 1, gy)]['type'] == tile['type']:
                right = True
            if (gx, gy + 1) in level.tiles and level.tiles[(gx, gy + 1)]['type'] == tile['type']:
                down = True
            if (gx, gy - 1) in level.tiles and level.tiles[(gx, gy - 1)]['type'] == tile['type']:
                top = True
            if not left and not top and right:
                tile['variant'] = 0
            if left and not top and right:
                tile['variant'] = 1
            if left and not top and not right:
                tile['variant'] = 2
            if left and top and not right and down:
                tile['variant'] = 3
            if left and top and not right and not down:
                tile['variant'] = 4
            if left and top and right and down:
                tile['variant'] = 5
            if not left and top and right and not down:
                tile['variant'] = 6
            if not left and top and right and down:
                tile['variant'] = 7
            if left and top and right and not down:
                tile['variant'] = 8
            if top and not left and not down and right:
                tile['variant'] = 9
         
load_level(0, False)
while True:
    clock.tick(120)
    screen.fill((0, 0, 0))
    counter += 1
    m_pos = pygame.mouse.get_pos()
    tile_x = (m_pos[0] + level.camera_x) // tile_size * tile_size
    tile_y = (m_pos[1] + level.camera_y) // tile_size * tile_size
    try:
        image:pygame.Surface = resources[resource_names[current_resource_index]][variant]
    except:
        print(resource_names[current_resource_index])
        print(variant)
        raise
    render(screen)
    image.set_alpha(150)
    screen.blit(image, (tile_x - level.camera_x, tile_y - level.camera_y))
    image.set_alpha(255)
    render_grid()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                num_x = tile_x // tile_size
                num_y = tile_y // tile_size
                tile = {
                    'type' : resource_names[current_resource_index],
                    'variant' : variant,
                    'x' : num_x,
                    'y' : num_y
                }
                if (num_x, num_y) in tiles and tiles[(num_x, num_y)]['type'] == 'spawners' and tiles[(num_x, num_y)]['variant'] == 0:
                    level.p_counter -= 1
                if tile['type'] == 'spawners' and tile['variant'] == 0:
                    level.p_counter += 1
                if level.p_counter <= 1:
                    level.tiles[(num_x, num_y)] = tile
                else: 
                    level.p_counter = 1
                if tile['type'] == 'decor':
                    tile['variant'] = random.randint(0, 7)
            if event.button == 3:
                num_x = tile_x // tile_size
                num_y = tile_y // tile_size
                if (num_x, num_y) in level.tiles:
                    if level.tiles[(num_x, num_y)]['type'] == 'spawners' and level.tiles[(num_x, num_y)]['variant'] == 0:
                        level.p_counter -= 1
                    del level.tiles[(num_x, num_y)]
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                current_resource_index += 1
                variant = 0
                if current_resource_index == len(resource_names):
                    current_resource_index = 0
            if event.y < 0:
                current_resource_index -= 1
                if current_resource_index == -1:
                    current_resource_index = len(resource_names) -1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                variant += 1
                if variant == len(resources[resource_names[current_resource_index]]):
                    variant = 0
            if event.key == pygame.K_DELETE:
                del_count += 1
                df_counter = counter
                if del_count == 2:
                    level.p_counter = 0
                    level.tiles.clear()
                    del_count = 0
                    df_counter = 0
            if event.key == pygame.K_ESCAPE:
                save()
                exit()
            if event.key == pygame.K_RIGHT:
                mv_right = True
            if event.key == pygame.K_LEFT:
                mv_left = True
            if event.key == pygame.K_UP:
                mv_up = True
            if event.key == pygame.K_DOWN:
                mv_down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                mv_right = False
            if event.key == pygame.K_LEFT:
                mv_left = False
            if event.key == pygame.K_UP:
                mv_up = False
            if event.key == pygame.K_DOWN:
                mv_down = False 
        transform()
    if counter - df_counter >= 180:
        del_count = 0
    if mv_down == True:
        level.camera_y += 5
    if mv_left == True:
        level.camera_x -= 5
    if mv_right == True:
        level.camera_x += 5
    if mv_up == True:
        level.camera_y -= 5
    pygame.display.update()














