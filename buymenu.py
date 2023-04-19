import pygame
import sys

# Import functions from external modules
from stonker import check_stock_price, current_balance, max_buy, confirm_buy


def draw_input_box(screen, rect, font, text):
    pygame.draw.rect(screen, (42, 157, 143), rect, 3)
    input_surface = font.render(text, True, (255, 255, 255))
    screen.blit(input_surface, (rect.x + 10, rect.y + 10))


def draw_button(screen, rect, font, text, color):
    pygame.draw.rect(screen, color, rect)
    button_surface = font.render(text, True, (38, 70, 83))
    screen.blit(button_surface, (rect.x + 20, rect.y + 15))


def draw_output_text(screen, font, text):
    output_text_surface = font.render(text, True, (0, 0, 0))
    output_text_rect = output_text_surface.get_rect()
    output_text_rect.center = (400, 500)
    screen.blit(output_text_surface, output_text_rect)


def draw_help_text(screen, font):
    help_text = "Press 'h' for help"
    help_text_surface = font.render(help_text, True, (0, 0, 0))
    help_text_rect = help_text_surface.get_rect()
    help_text_rect.topleft = (10, 10)
    screen.blit(help_text_surface, help_text_rect)


def handle_input_events(event, ticker_input_text, username):
    output_text = ""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            # Remove the last character from the ticker input text
            ticker_input_text = ticker_input_text[:-1]
        elif event.key == pygame.K_RETURN:
            if ticker_input_text == "":
                # If the user hasn't entered a ticker symbol, display an error message
                output_text = "Please enter a ticker symbol"
            else:
                # Check the stock price, current balance, and max buy amount
                stock_price = check_stock_price(ticker_input_text)
                balance = current_balance(username)
                max_buy_amount = max_buy(username, ticker_input_text)
                # Format the output text with the stock price, balance, and max buy amount
                output_text = f"Stock price for {ticker_input_text}: ${stock_price:.2f}\n"
                output_text += f"Your current balance: ${balance:.2f}\n"
                output_text += f"Maximum buy amount for {ticker_input_text}: {max_buy_amount}\n"
        else:
            # Add the pressed key to the ticker input text
            ticker_input_text += event.unicode
    return ticker_input_text, output_text



def handle_mouse_events(event, ticker_input_text, username, shares_amount):
    output_text = ""
    if event.type == pygame.MOUSEBUTTONDOWN:
        if buy_button_rect.collidepoint(event.pos):
            # Call confirm buy function and pass in ticker input text, username, and shares_amount
            success = confirm_buy(ticker_input_text, username, shares_amount)
            # Update output text with confirmation message
            if success:
                output_text = f"You have successfully bought {shares_amount} shares of {ticker_input_text}"
            else:
                output_text = "Unable to complete purchase. Please check your balance and try again."
        elif sell_button_rect.collidepoint(event.pos):
            # Update output text with sell message
            output_text = "Sell functionality not yet implemented"
    return output_text



def draw_buy_menu(screen, font, ticker_input_rect, ticker_input_text, buy_button_rect, sell_button_rect, output_text, help_text):
    # Draw the stock ticker input box
    pygame.draw.rect(screen, (42, 157, 143), ticker_input_rect, 3)
    ticker_input_surface = font.render(ticker_input_text, True, (255, 255, 255))
    screen.blit(ticker_input_surface, (ticker_input_rect.x + 10, ticker_input_rect.y + 10))

    # Draw the buy and sell buttons
    pygame.draw.rect(screen, (233, 196, 106), buy_button_rect)
    pygame.draw.rect(screen, (244, 162, 97), sell_button_rect)
    buy_button_surface = font.render("Buy", True, (38, 70, 83))
    sell_button_surface = font.render("Sell", True, (38, 70, 83))
    screen.blit(buy_button_surface, (buy_button_rect.x + 20, buy_button_rect.y + 15))
    screen.blit(sell_button_surface, (sell_button_rect.x + 20, sell_button_rect.y + 15))

    # Draw the output text
    output_text_surface = font.render(output_text, True, (0, 0, 0))
    output_text_rect = output_text_surface.get_rect()
    output_text_rect.center = (400, 500)
    screen.blit(output_text_surface, output_text_rect)

    # Draw the help text
    help_text_surface = font.render(help_text, True, (0, 0, 0))
    help_text_rect = help_text_surface.get_rect()
    help_text_rect.topleft = (10, 10)
    screen.blit(help_text_surface, help_text_rect)

    # Change color of buttons when hovered over
    mouse_pos = pygame.mouse.get_pos()
    if buy_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 200, 0), buy_button_rect)
    else:
        pygame.draw.rect(screen, (0, 255, 0), buy_button_rect)
    if sell_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (200, 0, 0), sell_button_rect)
    else:
        pygame.draw.rect(screen, (255, 0, 0), sell_button_rect)


def buy_menu(username):
    # Initialize Pygame
    pygame.init()

    # Set up the Pygame window
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Stock Market Menu")

    # Set up the font
    font = pygame.font.Font("Roboto-Regular.ttf", 28)

    # Set up the stock ticker input box
    ticker_input_rect = pygame.Rect(200, 200, 300, 50)
    ticker_input_text = ""

    # Set up the buy/sell buttons
    buy_button_rect = pygame.Rect(200, 300, 120, 50)
    sell_button_rect = pygame.Rect(380, 300, 120, 50)

    # Set up the output text
    output_text = ""
    help_text = "Press 'h' for help"

    # Main game loop
    while True:
        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                ticker_input_text = handle_input_events(event, ticker_input_text)
                if event.key == pygame.K_h:
                    output_text = "Enter a ticker symbol to get the stock price, current balance, and maximum buy amount.\n"
                    output_text += "Click the 'Buy' button to buy stocks, or the 'Sell' button to sell stocks (not yet implemented).\n"
                    output_text += "Press 'esc' to return to the main menu."
                elif event.key == pygame.K_ESCAPE:
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                output_text = handle_mouse_events(event, ticker_input_text, username, shares_amount, buy_button_rect, sell_button_rect)


        # Clear the screen
        screen.fill((38, 70, 83))

        # Draw the buy menu
        draw_buy_menu(screen, font, ticker_input_rect, ticker_input_text, buy_button_rect, sell_button_rect, output_text, help_text)

        # Update the screen
        pygame.display.update()