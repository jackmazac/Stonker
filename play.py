#!/usr/bin/env python3

import pygame
import sys
from loginmenu import login_menu
from newusermenu import new_user_menu
from gamemenu import game_menu

def init_display():
    size = (400, 300)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Main Menu")
    return screen

def main():
    # Initialize PyGame
    pygame.init()

    # Set the window size and title
    size = (400, 300)
    title = "Main Menu"
    screen = init_display()

    # Set colors
    background_color = (0, 128, 128)
    button_color = (255, 255, 255)
    button_hover_color = (200, 200, 200)
    button_text_color = (0, 0, 0)
    title_text_color = (255, 255, 255)

    # Set fonts
    title_font = pygame.font.Font("fonts/OpenSans-Bold.ttf", 40)
    button_font = pygame.font.Font("fonts/OpenSans-Regular.ttf", 20)
    icon_font = pygame.font.Font("fonts/fontawesome-webfont.ttf", 20)

    # Load icons
    login_icon = icon_font.render(u"\uf155", True, button_text_color)
    new_user_icon = icon_font.render(u"\uf067", True, button_text_color)
    close_icon = icon_font.render(u"\uf00d", True, button_text_color)

    # Create buttons
    login_button = pygame.Rect(100, 100, 200, 50)
    new_user_button = pygame.Rect(100, 160, 200, 50)

    # Create close button
    close_button = pygame.Rect(370, 10, 20, 20)

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
                    username = login_menu()
                    if username:
                        game_menu(username)
                    screen = init_display()

                # Check for new user button click
                elif new_user_button.collidepoint(event.pos):
                    pygame.display.quit()
                    username = new_user_menu()
                    if username:
                        game_menu(username)
                    screen = init_display()

                # Check for close button click
                elif close_button.collidepoint(event.pos):
                    # Exit program
                    pygame.quit()
                    sys.exit()

        # Clear screen
        screen.fill(background_color)

        # Draw title
        title_text = title_font.render(title, True, title_text_color)
        title_rect = title_text.get_rect(center=(size[0]/2, 50))
        screen.blit(title_text, title_rect)

        # Draw buttons
        pygame.draw.rect(screen, button_color, login_button)
        pygame.draw.rect(screen, button_color, new_user_button)
        screen.blit(login_icon, login_button.move(20, 10))
        screen.blit(new_user_icon, new_user_button.move(20, 10))
        login_text = button_font.render("Login", True, button_text_color)
        new_user_text = button_font.render("Create New User", True, button_text_color)
        screen.blit(login_text, login_button.move(70, 15))
        screen.blit(new_user_text, new_user_button.move(50, 15))

        # Draw close button
        pygame.draw.rect(screen, button_color, close_button)
        screen.blit(close_icon, close_button.move(0, 0))

        # Check if mouse is hovering over buttons
        if login_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, button_hover_color, login_button, 3)
        if new_user_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, button_hover_color, new_user_button, 3)
        if close_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, button_hover_color, close_button, 3)

        # Update display
        pygame.display.update()

if __name__ == "__main__":
    main()