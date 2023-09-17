def main():
    import pygame
    from sys import exit
    import random

    WIDTH = 288
    HEIGHT = 512
    MAX_FPS = 60
    
    PIPE_WIDTH = 52
    GROUND_HEIGHT = 112
    GAP_SIZE = 440

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird Clone")
    
    favicon = pygame.image.load("assets/favicon.ico")
    pygame.display.set_icon(favicon)
    
    clock = pygame.time.Clock()
    
    sky_surf = pygame.image.load("assets/sprites/background-day.png").convert()
    ground_surf = pygame.image.load("assets/sprites/base.png").convert()
    ground_rect = ground_surf.get_rect(bottomleft=(0, HEIGHT))
    
    bottom_pipe_surf = pygame.image.load("assets/sprites/pipe-green.png").convert()
    top_pipe_surf = pygame.image.load("assets/sprites/pipe-green.png").convert()
    top_pipe_surf = pygame.transform.rotate(top_pipe_surf, 180)
    top_pipe_surf = pygame.transform.flip(top_pipe_surf, True, False)
    
    bottom_pipe_rect = bottom_pipe_surf.get_rect(topleft=(WIDTH/2, HEIGHT/2))
    top_pipe_rect = top_pipe_surf.get_rect(topleft=(bottom_pipe_rect.x, bottom_pipe_rect.y - GAP_SIZE))
    
    player_surf = pygame.image.load("assets/sprites/yellowbird-upflap.png").convert()
    player_rect = player_surf.get_rect(center=(WIDTH/3, HEIGHT/3))
    
    speed = 2
    player_gravity = 0
    
    game_active = True

    while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    player_gravity = -8
                    if not game_active:
                        player_rect.y = HEIGHT/3
                        bottom_pipe_rect.x = WIDTH
                        game_active = True
                    player_gravity = -8
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not game_active:
                            player_rect.y = HEIGHT/3
                            bottom_pipe_rect.x = WIDTH
                            game_active = True
                        player_gravity = -8
                        
        if game_active:
            screen.blit(sky_surf, (0, 0))
            
            screen.blit(bottom_pipe_surf, bottom_pipe_rect)
            screen.blit(top_pipe_surf, top_pipe_rect)
            bottom_pipe_rect.x -= speed
            if bottom_pipe_rect.right < 0:
                bottom_pipe_rect.x = WIDTH
                bottom_pipe_rect.y = random.randint(int(HEIGHT/3), int(HEIGHT - GROUND_HEIGHT * 1.5))
            top_pipe_rect.x = bottom_pipe_rect.x
            top_pipe_rect.y = bottom_pipe_rect.y - GAP_SIZE
            
            if player_rect.colliderect(bottom_pipe_rect) or player_rect.colliderect(top_pipe_rect):
                game_active = False

            
            screen.blit(ground_surf, ground_rect)
            
            # Player
            player_gravity += 0.5
            player_rect.y += int(player_gravity)
            screen.blit(player_surf, player_rect)
            
            # Collision
            if player_rect.bottom >= ground_rect.top:
                player_rect.bottom = ground_rect.top
                game_active = False
            
                
        pygame.display.update()
        clock.tick(MAX_FPS)
        
if __name__ == "__main__":
    main()