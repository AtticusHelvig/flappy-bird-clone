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
    JUMP_GRAVITY = -8
    SPEED = 4
    
    NEW = "new"
    OVER = "over"
    ACTIVE = "active"
    
    BIRD_COLOR = "red" # red, yellow, or blue

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird Clone")
    
    favicon = pygame.image.load("assets/favicon.ico")
    pygame.display.set_icon(favicon)
    
    clock = pygame.time.Clock()
    
    sky_surf = pygame.image.load("assets/sprites/background-day.png").convert()
    ground_surf = pygame.image.load("assets/sprites/base.png").convert()
    ground_rect = ground_surf.get_rect(bottomleft=(0, HEIGHT))
    
    global bottom_pipe_surf
    global top_pipe_surf
    bottom_pipe_surf = pygame.image.load("assets/sprites/pipe-green.png").convert()
    top_pipe_surf = pygame.image.load("assets/sprites/pipe-green.png").convert()
    top_pipe_surf = pygame.transform.rotate(top_pipe_surf, 180)
    top_pipe_surf = pygame.transform.flip(top_pipe_surf, True, False)
    
    bottom_pipe_rect = bottom_pipe_surf.get_rect(topleft=(WIDTH, HEIGHT/2))
    top_pipe_rect = top_pipe_surf.get_rect(topleft=(bottom_pipe_rect.x, bottom_pipe_rect.y - GAP_SIZE))
    
    player_surf = pygame.image.load("assets/sprites/" + BIRD_COLOR + "bird-upflap.png").convert()
    player_rect = player_surf.get_rect(center=(WIDTH/3, HEIGHT/3))
    rotated_player_surf = player_surf
    up_flap_player_surf = pygame.image.load("assets/sprites/" + BIRD_COLOR + "bird-upflap.png").convert()
    mid_flap_player_surf = pygame.image.load("assets/sprites/" + BIRD_COLOR + "bird-midflap.png").convert()
    down_flap_player_surf = pygame.image.load("assets/sprites/" + BIRD_COLOR + "bird-downflap.png").convert()
    
    game_over_surf = pygame.image.load("assets/sprites/gameover.png").convert_alpha()
    game_over_rect = game_over_surf.get_rect(center=(WIDTH/2, (HEIGHT - GROUND_HEIGHT) / 2))
    
    title_surf = pygame.image.load("assets/sprites/title.png").convert_alpha()
    title_rect = title_surf.get_rect(center=(WIDTH/2, HEIGHT/5))
            
    STARTING_SCORE = 0
    score = STARTING_SCORE
    TRANSPARENT = "#111111"
    
    surf_0 = pygame.image.load("assets/sprites/0.png")
    surf_1 = pygame.image.load("assets/sprites/1.png")
    surf_2 = pygame.image.load("assets/sprites/2.png")
    surf_3 = pygame.image.load("assets/sprites/3.png")
    surf_4 = pygame.image.load("assets/sprites/4.png")
    surf_5 = pygame.image.load("assets/sprites/5.png")
    surf_6 = pygame.image.load("assets/sprites/6.png")
    surf_7 = pygame.image.load("assets/sprites/7.png")
    surf_8 = pygame.image.load("assets/sprites/8.png")
    surf_9 = pygame.image.load("assets/sprites/9.png")
    
    score_surf = pygame.Surface((WIDTH, surf_0.get_height()))
    score_surf.set_colorkey(TRANSPARENT)
    
    def update_score():
        global score_width
        score_width = 0
        score_surf.fill(TRANSPARENT)
        for digit in str(score):
            match digit:
                case "0":
                    score_surf.blit(surf_0, (score_width, 0))
                    score_width += surf_0.get_width()
                case "1":
                    score_surf.blit(surf_1, (score_width, 0))
                    score_width += surf_1.get_width()
                case "2":
                    score_surf.blit(surf_2, (score_width, 0))
                    score_width += surf_2.get_width()
                case "3":
                    score_surf.blit(surf_3, (score_width, 0))
                    score_width += surf_3.get_width()
                case "4":
                    score_surf.blit(surf_4, (score_width, 0))
                    score_width += surf_4.get_width()
                case "5":
                    score_surf.blit(surf_5, (score_width, 0))
                    score_width += surf_5.get_width()
                case "6":
                    score_surf.blit(surf_6, (score_width, 0))
                    score_width += surf_6.get_width()
                case "7":
                    score_surf.blit(surf_7, (score_width, 0))
                    score_width += surf_7.get_width()
                case "8":
                    score_surf.blit(surf_8, (score_width, 0))
                    score_width += surf_8.get_width()
                case "9":
                    score_surf.blit(surf_9, (score_width, 0))
                    score_width += surf_9.get_width()
                    
    def update_colors():
        global bottom_pipe_surf
        global top_pipe_surf
        if score % 10 == 9:
            bottom_pipe_surf = pygame.image.load("assets/sprites/pipe-red.png").convert()
            top_pipe_surf = pygame.image.load("assets/sprites/pipe-red.png").convert()
            top_pipe_surf = pygame.transform.rotate(top_pipe_surf, 180)
            top_pipe_surf = pygame.transform.flip(top_pipe_surf, True, False)
        else:
            bottom_pipe_surf = pygame.image.load("assets/sprites/pipe-green.png").convert()
            top_pipe_surf = pygame.image.load("assets/sprites/pipe-green.png").convert()
            top_pipe_surf = pygame.transform.rotate(top_pipe_surf, 180)
            top_pipe_surf = pygame.transform.flip(top_pipe_surf, True, False)
    
    player_gravity = 0
    time_since_flap = 100
    new_pipe = True
    
    game_state = NEW

    while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    player_gravity = JUMP_GRAVITY
                    time_since_flap = 0
                    if not game_state == ACTIVE:
                        player_rect.y = HEIGHT/3
                        bottom_pipe_rect.x = WIDTH
                        game_state = ACTIVE
                        score = STARTING_SCORE
                        new_pipe = True
                    player_gravity = JUMP_GRAVITY
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not game_state == ACTIVE:
                            player_rect.y = HEIGHT/3
                            bottom_pipe_rect.x = WIDTH
                            game_state = ACTIVE
                            score = STARTING_SCORE
                            new_pipe = True
                        player_gravity = JUMP_GRAVITY
                        time_since_flap = 0
                        
        if game_state == NEW:
            screen.blit(sky_surf, (0, 0))
            screen.blit(bottom_pipe_surf, bottom_pipe_rect)
            screen.blit(top_pipe_surf, top_pipe_rect)
            screen.blit(title_surf, title_rect)
            screen.blit(ground_surf, ground_rect)
            screen.blit(player_surf, player_rect)

                        
        if game_state == OVER:
                screen.blit(game_over_surf, game_over_rect)
                        
        if game_state == ACTIVE:
            screen.blit(sky_surf, (0, 0))
            
            screen.blit(bottom_pipe_surf, bottom_pipe_rect)
            screen.blit(top_pipe_surf, top_pipe_rect)
            bottom_pipe_rect.x -= SPEED
            if bottom_pipe_rect.right < 0:
                update_colors()
                bottom_pipe_rect.x = WIDTH
                bottom_pipe_rect.y = random.randint(int(HEIGHT/3), int(HEIGHT - GROUND_HEIGHT * 1.5))
                new_pipe = True
            top_pipe_rect.x = bottom_pipe_rect.x
            top_pipe_rect.y = bottom_pipe_rect.y - GAP_SIZE
            
            if player_rect.left > bottom_pipe_rect.right and new_pipe == True:
                score += 1
                new_pipe = False
            
            if player_rect.bottom < 0:
                player_rect.bottom = 0
            
            update_score()
            screen.blit(score_surf, ((WIDTH - score_width) / 2, HEIGHT / 7))
            
            title_rect.x -= SPEED
            if title_rect.right > 0:
                screen.blit(title_surf, title_rect)
            
            if player_rect.colliderect(bottom_pipe_rect) or player_rect.colliderect(top_pipe_rect):
                game_state = OVER

            
            screen.blit(ground_surf, ground_rect)
            
            # Player
            player_gravity += 0.5
            player_rect.y += int(player_gravity)
            
            time_since_flap += 1
            if time_since_flap < 5:
                player_surf = mid_flap_player_surf
            if time_since_flap < 15:
                player_surf = down_flap_player_surf
            else:
                player_surf = up_flap_player_surf
            
            rotated_player_surf = pygame.transform.rotate(player_surf, -player_gravity * 2)
            
            # Collision
            if player_rect.bottom >= ground_rect.top:
                player_rect.bottom = ground_rect.top
                game_state = OVER
                
            screen.blit(rotated_player_surf, player_rect)
            
                
        pygame.display.update()
        clock.tick(MAX_FPS)
        
if __name__ == "__main__":
    main()