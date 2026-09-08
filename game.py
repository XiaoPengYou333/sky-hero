import pygame 
from scripts import settings, player, level, enemy

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
settings.SCREEN_WIDTH = screen.get_width()
settings.SCREEN_HEIGHT = screen.get_height()
clock = pygame.time.Clock()
level.load_level(0, True)
bg = pygame.image.load('graph/images/background.png')
bg = pygame.transform.scale(bg, screen.get_size())
p_x, p_y = level.get_player_cor()
enemy_cors = level.get_enemies()
main_player = player.Player(p_x, p_y)
enemies = []
for x, y in enemy_cors:
        enemies.append(enemy.Enemy(x, y))

while True:
    clock.tick(settings.FPS)
    screen.blit(bg, (0, 0))
    level.camera_x += (main_player.x - settings.SCREEN_WIDTH / 2 - level.camera_x) / 25
    level.camera_y += (main_player.y - settings.SCREEN_HEIGHT + 600 - level.camera_y + 350) / 1
    level.camera_x = round(level.camera_x)
    level.camera_y = round(level.camera_y)
    level.render(screen)
    main_player.render(screen, level.camera_x, level.camera_y)
    main_player.update()
    if level.get_barrier_collisions(main_player.get_hb()):
        main_player.death()
    for en in enemies:
        en.render(screen, level.camera_x, level.camera_y)
        en.update()
        en.ai()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            if event.key == pygame.K_LEFT:
                main_player.mv_l = True
            if event.key == pygame.K_RIGHT:
                main_player.mv_r = True
            if event.key == pygame.K_SPACE and main_player.time_in_air < 5:
                main_player.s_y = settings.JUMP_POWER
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                main_player.mv_l = False
            if event.key == pygame.K_RIGHT:
                main_player.mv_r = False
    pygame.display.update()