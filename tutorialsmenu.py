import pygame

def tutorials_menu():
    pygame.init()
    win_width = 800
    win_height = 600
    game_display = pygame.display.set_mode((win_width, win_height))
    clock = pygame.time.Clock()

    running = True

    while running:
        game_display.fill((255, 255, 255))

        font = pygame.font.SysFont(None, 50)
        text = font.render("Tutorials", True, (0, 0, 0))
        game_display.blit(text, (win_width // 2 - 100, 50))

        # Draw list of available tutorials
        tutorial_list = ["Tutorial 1: Introduction to Stock Market", "Tutorial 2: Fundamental Analysis", "Tutorial 3: Technical Analysis", "Tutorial 4: Risk Management"]
        font = pygame.font.SysFont(None, 30)
        y = 150
        for tutorial in tutorial_list:
            text = font.render(tutorial, True, (0, 0, 0))
            game_display.blit(text, (50, y))
            y += 30

        # Draw back button
        font = pygame.font.SysFont(None, 30)
        button = pygame.Rect(win_width // 2 - 100, win_height - 100, 200, 50)
        pygame.draw.rect(game_display, (0, 128, 0), button)
        text = font.render("Back to Game Menu", True, (255, 255, 255))
        game_display.blit(text, (win_width // 2 - 100, win_height - 90))

        # Handle user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button.collidepoint(mouse_pos):
                    running = False

        # update the display
        pygame.display.update()
