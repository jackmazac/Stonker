import pygame
from stonker import check_inventory, sell_from_portfolio

def draw_sell_menu(screen, font, sell_button_rect, output_text, sell_symbol_input_rect, sell_symbol_input_text,
                    sell_shares_input_rect, sell_shares_input_text, help_text):
    # Draw the "Sell" button
    pygame.draw.rect(screen, (233, 196, 106), sell_button_rect)
    sell_button_surface = font.render("Sell", True, (38, 70, 83))
    screen.blit(sell_button_surface, (sell_button_rect.x + 20, sell_button_rect.y + 15))

    # Draw the output text
    output_text_surface = font.render(output_text, True, (0, 0, 0))
    output_text_rect = output_text_surface.get_rect()
    output_text_rect.center = (400, 500)
    screen.blit(output_text_surface, output_text_rect)

    # Draw the sell symbol input box
    pygame.draw.rect(screen, (255, 255, 255), sell_symbol_input_rect)
    pygame.draw.rect(screen, (0, 0, 0), sell_symbol_input_rect, 3)
    sell_symbol_input_surface = font.render(sell_symbol_input_text, True, (0, 0, 0))
    screen.blit(sell_symbol_input_surface, (sell_symbol_input_rect.x + 10, sell_symbol_input_rect.y + 10))

    # Draw the sell shares input box
    pygame.draw.rect(screen, (255, 255, 255), sell_shares_input_rect)
    pygame.draw.rect(screen, (0, 0, 0), sell_shares_input_rect, 3)
    sell_shares_input_surface = font.render(sell_shares_input_text, True, (0, 0, 0))
    screen.blit(sell_shares_input_surface, (sell_shares_input_rect.x + 10, sell_shares_input_rect.y + 10))

    # Draw the help text
    help_text_surface = font.render(help_text, True, (0, 0, 0))
    help_text_rect = help_text_surface.get_rect()
    help_text_rect.center = (400, 570)
    screen.blit(help_text_surface, help_text_rect)

def handle_mouse_events(event, username, stocks, sell_button_rect, sell_symbol_input_rect, sell_symbol_input_text,
                         sell_shares_input_rect, sell_shares_input_text):
    output_text = ""
    sell_symbol_input_active = False
    sell_shares_input_active = False

    # Handle mouse events
    if event.type == pygame.MOUSEBUTTONDOWN:
        if sell_button_rect.collidepoint(event.pos):
            # Switch to the sell symbol input loop
            sell_symbol_input_active = True
            output_text = "Enter a ticker symbol to sell shares:"
            sell_symbol_input_text = ""
            sell_shares_input_text = ""

    # Handle keyboard events
    if event.type == pygame.KEYDOWN:
        if sell_symbol_input_active:
            if event.key == pygame.K_RETURN:
                # Check if the entered ticker symbol is valid
                if sell_symbol_input_text not in valid_sell_symbols:
                    output_text = f"Invalid ticker symbol: {sell_symbol_input_text}"
                else:
                    # Switch to the sell shares input loop
                    sell_symbol_input_active = False
                    sell_shares_input_active = True
                    output_text = f"Enter the number of {sell_symbol_input_text} shares to sell:"

            elif sell_shares_input_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Attempt to sell the entered number of shares
                        success = sell_from_portfolio(username, sell_symbol_input_text, sell_shares_input_text)
                        if success:
                            output_text = f"You have successfully sold {sell_shares_input_text} shares of {sell_symbol_input_text}"
                        else:
                            output_text = "Unable to complete sale. Please check your inventory and try again."
                        # Reset the input variables
                        sell_symbol_input_text = ""
                        sell_shares_input_text = ""
                        sell_symbol_input_active = True
                    elif event.key == pygame.K_BACKSPACE:
                        # Remove the last character from the sell shares input text
                        sell_shares_input_text = sell_shares_input_text[:-1]
                    elif event.unicode.isdigit():
                        # Add the pressed key to the sell shares input text if it's a digit
                        sell_shares_input_text += event.unicode

            # Clear the screen
            screen.fill((38, 70, 83))

            # Draw the sell menu
            draw_sell_menu(screen, font, sell_button_rect, sell_symbol_input_rect, sell_symbol_input_text, sell_shares_input_rect, sell_shares_input_text, output_text)

            # Update the screen
            pygame.display.update()

def sell_menu(username):
    pygame.init()
    
    # Set up the Pygame screen
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Stonker - Sell Stocks")

    # Load fonts
    font = pygame.font.Font("assets/fonts/OpenSans-Regular.ttf", 20)

    # Load the user's stocks and valid sell symbols
    balance, stocks, total_value = check_inventory(username)
    valid_sell_symbols = [stock[0] for stock in stocks]

    # Set up the sell button rectangle
    sell_button_rect = pygame.Rect(350, 400, 100, 50)

    # Set up the sell symbol input box
    sell_symbol_input_rect = pygame.Rect(150, 150, 500, 50)
    sell_symbol_input_active = True
    sell_symbol_input_text = ""

    # Set up the sell shares input box
    sell_shares_input_rect = pygame.Rect(150, 250, 500, 50)
    sell_shares_input_active = False
    sell_shares_input_text = ""

    # Set up the initial output text
    output_text = "Enter a ticker symbol to sell shares:"

    # Run the Pygame loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_events(event, username, stocks, sell_button_rect)
            elif event.type == pygame.KEYDOWN:
                handle_keyboard_events(event, valid_sell_symbols)

        # Draw the sell menu
        draw_sell_menu(screen, font, sell_button_rect, sell_symbol_input_rect, sell_symbol_input_text, sell_shares_input_rect, sell_shares_input_text, output_text)

        # Update the screen
        pygame.display.update()
