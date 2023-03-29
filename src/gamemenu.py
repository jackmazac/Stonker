import pygame
from stonker import check_inventory


def game_menu(username):
    pygame.init()
    win_width = 800
    win_height = 600
    game_display = pygame.display.set_mode((win_width, win_height))
    clock = pygame.time.Clock()

    running = True

    while running:
        game_display.fill((255, 255, 255))

        # Get user's inventory info
        balance, stocks, total_value = check_inventory(username)

        # Draw inventory info on left side of screen
        font = pygame.font.SysFont(None, 30)
        text = font.render(f"Balance: ${balance}", True, (0, 0, 0))
        game_display.blit(text, (50, 50))

        text = font.render("Stocks:", True, (0, 0, 0))
        game_display.blit(text, (50, 100))
        y = 130
        for stock, quantity in stocks.items():
            text = font.render(f"{stock}: {quantity}", True, (0, 0, 0))
            game_display.blit(text, (50, y))
            y += 30

        text = font.render(f"Total Value: ${total_value}", True, (0, 0, 0))
        game_display.blit(text, (50, y + 30))

        # Draw right side of screen with game options
        font = pygame.font.SysFont(None, 50)
        text = font.render("Game Menu", True, (0, 0, 0))
        game_display.blit(text, (win_width // 2 - 100, 50))

        button_font = pygame.font.SysFont(None, 30)
        button = pygame.Rect(win_width // 2 - 100, 150, 200, 50)
        pygame.draw.rect(game_display, (0, 128, 0), button)
        text = button_font.render("Buy Stocks", True, (255, 255, 255))
        game_display.blit(text, (win_width // 2 - 75, 160))

        button = pygame.Rect(win_width // 2 - 100, 220, 200, 50)
        pygame.draw.rect(game_display, (0, 128, 0), button)
        text = button_font.render("Sell Stocks", True, (255, 255, 255))
        game_display.blit(text, (win_width // 2 - 75, 230))

        button = pygame.Rect(win_width // 2 - 100, 290, 200, 50)
        pygame.draw.rect(game_display, (0, 128, 0), button)
        text = button_font.render("Tutorials", True, (255, 255, 255))
        game_display.blit(text, (win_width // 2 - 75, 300))

        # Handle user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button.collidepoint(mouse_pos):
                    print("Buy Stocks button clicked")
                    # Call function to buy stocks
                button = pygame.Rect(win_width // 2 - 100, 220, 200, 50)
                if button.collidepoint(mouse_pos):
                    print("Sell Stocks button clicked")
                    # Call function to sell stocks
                button = pygame.Rect(win_width // 2 - 100, 290, 200, 50)
                if button.collidepoint(mouse_pos):
                    print("Tutorials button clicked")
                    # Call function to display tutorials
        # update the display
        pygame.display.update()