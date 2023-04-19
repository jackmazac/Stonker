import pygame
from stonker import new_user

def new_user_menu():
    # Define colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    #BLUE = (0, 128, 255)
    button_text_color = WHITE
    button_font = pygame.font.Font("fonts/OpenSans-Regular.ttf", 20)
    button_hover_color = GRAY

    # Initialize Pygame
    pygame.init()

    # Set up the font
    font = pygame.font.Font("fonts/OpenSans-Regular.ttf", 28)

    # Set up the window
    win = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Create New User")

    # Set up the text boxes
    username_box = pygame.Rect(150, 200, 200, 32)
    password_box = pygame.Rect(150, 250, 200, 32)

    # Set up the buttons
    create_button = pygame.Rect(200, 320, 100, 40)
    back_button = pygame.Rect(30, 30, 50, 50)

    # Set up the text strings
    username_str = ''
    password_str = ''

    # Set up the icon font
    icon_font = pygame.font.Font("fonts/fontawesome-webfont.ttf", 20)
    
    # Main loop
    running = True
    while running:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Check if the user clicked on the create user button
                    if create_button.collidepoint(event.pos):
                        # Call the new user function and pass in the text from the boxes
                        new_user(username_str, password_str)
                        running = False
                    # Check if the user clicked on the back button
                    elif back_button.collidepoint(event.pos):
                        return True
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

        # Draw the window
        win.fill(BLACK)

        # Draw the title
        title_text = font.render("Create New User", True, WHITE)
        title_rect = title_text.get_rect(center=(win.get_width()/2, 80))
        win.blit(title_text, title_rect)

        # Draw the text boxes
        pygame.draw.rect(win, WHITE, username_box, 2)
        pygame.draw.rect(win, WHITE, password_box, 2)

        # Render the text
        username_text = font.render(username_str, True, WHITE)
        password_text = font.render('*' * len(password_str), True, WHITE)

        # Draw the text
        win.blit(username_text, (username_box.x + 5, username_box.y + 5))
        win.blit(password_text, (password_box.x + 5, password_box.y + 5))

        # Draw the buttons
        pygame.draw.rect(win, GRAY, create_button)
        pygame.draw.rect(win, GRAY, back_button)

        # Draw icons on buttons
        create_icon = icon_font.render(u"\uf055", True, button_text_color)
        back_icon = icon_font.render(u"\uf060", True, button_text_color)
        win.blit(create_icon, (create_button.x + 5, create_button.y + 10))
        win.blit(back_icon, (back_button.x + 10, back_button.y + 10))

        # Render the button text
        create = button_font.render('Create User', True, button_text_color)
        back_text = button_font.render('Back', True, button_text_color)

        # Draw the button text
        win.blit(create, (create_button.x + 35, create_button.y + 10))
        win.blit(back_text, (back_button.x + 30, back_button.y + 10))

        # Check if mouse is hovering over buttons
        if create_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(win, button_hover_color, create_button, 3)
        if back_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(win, button_hover_color, back_button, 3)

        # Update the display
        pygame.display.update()
    return False
