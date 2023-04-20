import pygame
from stonker import check_login

def login_menu():
    # Initialize Pygame
    pygame.init()

    # Set up the window
    win = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Login")

    # Load the background image
    background_image = pygame.image.load('background_image.jpg')

    # Set up the fonts
    title_font = pygame.font.Font("fonts/OpenSans-Bold.ttf", 40)
    label_font = pygame.font.Font("fonts/OpenSans-Regular.ttf", 20)
    button_font = pygame.font.Font("fonts/OpenSans-Regular.ttf", 20)
    icon_font = pygame.font.Font("fonts/fontawesome-webfont.ttf", 20)

    # Set up the text boxes
    username_box = pygame.Rect(150, 200, 200, 32)
    password_box = pygame.Rect(150, 250, 200, 32)

    # Set up the buttons
    login_button = pygame.Rect(200, 320, 100, 50)
    back_button = pygame.Rect(50, 50, 50, 50)

    # Set up the colors
    box_color = (255, 255, 255)
    label_color = (255, 255, 255)
    button_color = (255, 255, 255)
    button_hover_color = (200, 200, 200)
    button_text_color = (0, 0, 0)

    # Load icons
    login_icon = icon_font.render(u"\uf090", True, button_text_color)
    back_icon = icon_font.render(u"\uf060", True, button_text_color)

    # Set up the text strings
    username_str = ''
    password_str = ''

    # Set up animation variables
    login_button_speed = 1
    back_button_rotation = 0

    # Game loop
    while True:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit program on X button
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Check if the user clicked on the login button
                    if login_button.collidepoint(event.pos):
                        # Call the login function and pass in the text from the boxes
                        if check_login(username_str, password_str):
                            from gamemenu import game_menu
                            pygame.display.quit()
                            game_menu(username_str)
                    # Check if the user clicked on the back button
                    elif back_button.collidepoint(event.pos):
                        # Go back to the main menu screen
                        from mainmenu import main_menu
                        pygame.display.quit()
                        main_menu()
            elif event.type == pygame.KEYDOWN:
                if username_box.collidepoint(pygame.mouse.get_pos()):
                    if event.unicode.isalnum() and len(username_str) < 12:
                        username_str += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        username_str = username_str[:-1]
                elif password_box.collidepoint(pygame.mouse.get_pos()):
                    if len(password_str) < 20:
                        if event.unicode.isalnum() or event.key == pygame.K_SPACE:
                            password_str += event.unicode
                        elif event.key == pygame.K_BACKSPACE:
                            password_str = password_str[:-1]

        # Draw the background image
        win.blit(background_image, (0, 0))

        # Draw title
        title_text = title_font.render("Login", True, label_color)
        title_rect = title_text.get_rect(center=(250, 100))
        win.blit(title_text, title_rect)

        # Draw username label
        username_label_text = label_font.render("Username:", True, label_color)
        username_label_rect = username_label_text.get_rect(center=(150, 183))
        win.blit(username_label_text, username_label_rect)

        # Draw password label
        password_label_text = label_font.render("Password:", True, label_color)
        password_label_rect = password_label_text.get_rect(center=(150, 233))
        win.blit(password_label_text, password_label_rect)

        # Draw the text boxes
        pygame.draw.rect(win, box_color, username_box, 2)
        pygame.draw.rect(win, box_color, password_box, 2)

        # Render the text
        username_text = label_font.render(username_str, True, label_color)
        password_text = label_font.render('*' * len(password_str), True, label_color)

        # Draw the text
        win.blit(username_text, (username_box.x + 5, username_box.y + 5))
        win.blit(password_text, (password_box.x + 5, password_box.y + 5))

        # Draw the buttons
        pygame.draw.rect(win, button_color, login_button)
        pygame.draw.rect(win, button_color, back_button)

        # Draw the icons
        win.blit(login_icon, (login_button.x + 15, login_button.y + 15))
        rotated_back_icon = pygame.transform.rotate(back_icon, back_button_rotation)
        back_icon_rect = rotated_back_icon.get_rect(center=back_button.center)
        win.blit(rotated_back_icon, back_icon_rect)

        # Render the button text
        login_text = button_font.render('Login', True, button_text_color)
        back_text = button_font.render('Back', True, button_text_color)

        # Draw the button text
        win.blit(login_text, (login_button.x + 50, login_button.y + 15))
        win.blit(back_text, (back_button.x + 15, back_button.y + 15))

        # Check if mouse is hovering over buttons
        if login_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(win, button_hover_color, login_button, 3)
        if back_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(win, button_hover_color, back_button, 3)

        # Update button animations
        # if login_button.x >= 300:
        #     login_button_speed = -1
        # elif login_button.x <= 200:
        #     login_button_speed = 1
        # login_button.x += login_button_speed

        # back_button_rotation += 1
        # if back_button_rotation >= 360:
        #     back_button_rotation = 0

        # Update display
        pygame.display.update()
