import pygame 
from scripts import settings, player, level

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
settings.SCREEN_WIDTH = screen.get_width()
settings.SCREEN_HEIGHT = screen.get_height()
clock = pygame.time.Clock()
level.load_level(0)
p_x, p_y = level.get_player_cor()
main_player = player.Player(p_x, p_y)
while True:
    clock.tick(settings.FPS)
    screen.fill((0, 0, 0))
    main_player.render(screen)
    level.render(screen)
    main_player.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            if event.key == pygame.K_LEFT:
                main_player.mv_l = True
            if event.key == pygame.K_RIGHT:
                main_player.mv_r = True
            if event.key == pygame.K_SPACE and main_player.time_in_air < 5:
                main_player.s_y = -20
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                main_player.mv_l = False
            if event.key == pygame.K_RIGHT:
                main_player.mv_r = False
    pygame.display.update()