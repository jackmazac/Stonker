import stonker
import pygame
import sys
from loginmenu import login_menu
from newusermenu import new_user_menu

def main_menu():

    # Initialize PyGame
    pygame.init()

    # Set the window size and title
    size = (400, 300)
    title = "Main Menu"
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(title)

    # Set colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    gray = (128, 128, 128)

    # Set fonts
    title_font = pygame.font.Font(None, 40)
    button_font = pygame.font.Font(None, 30)

    # Create buttons
    login_button = pygame.Rect(100, 100, 200, 50)
    new_user_button = pygame.Rect(100, 160, 200, 50)

    # Create close button
    close_button = pygame.Rect(370, 10, 20, 20)

    # Set button colors
    button_color = gray
    button_hover_color = white

    # Set button text
    login_text = button_font.render("Login", True, black)
    new_user_text = button_font.render("Create New User", True, black)

    # Set close button text
    close_text = button_font.render("X", True, black)

    # Set mouse hover text
    mouse_hover_text = button_font.render("Click to Continue", True, white)

    # Game loop
    while True:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit program on X button
                pygame.quit()
                sys.exit()

            # Check for button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check for login button click
                if login_button.collidepoint(event.pos):
                    pygame.display.quit()
                    login_menu()

                # Check for new user button click
                elif new_user_button.collidepoint(event.pos):
                    pygame.display.quit()
                    new_user_menu()

                # Check for close button click
                elif close_button.collidepoint(event.pos):
                    # Exit program
                    pygame.quit()
                    sys.exit()

        # Clear screen
        screen.fill(white)

        # Draw title
        title_text = title_font.render(title, True, black)
        title_rect = title_text.get_rect(center=(size[0]/2, 50))
        screen.blit(title_text, title_rect)

        # Draw buttons
        pygame.draw.rect(screen, button_color, login_button)
        pygame.draw.rect(screen, button_color, new_user_button)
        screen.blit(login_text, login_button.move(65, 15))
        screen.blit(new_user_text, new_user_button.move(15, 15))

        # Draw close button
        pygame.draw.rect(screen, button_color, close_button)
        screen.blit(close_text, close_button.move(5, 0))

        # Check if mouse is hovering over buttons
        if login_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, button_hover_color, login_button, 3)
            screen.blit(mouse_hover_text, login_button.move(10, 5))
        if new_user_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, button_hover_color, new_user_button, 3)
            screen.blit(mouse_hover_text, new_user_button.move(10, 5))

        # Update display
        pygame.display.update()
        
        # quit Pygame
        pygame.quit()

main_menu()