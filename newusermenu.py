import pygame
from stonker import new_user
    


# Set up new user page
def new_user_menu():
    ## initialize Pygame
    pygame.init()

    # set up the window
    win = pygame.display.set_mode((500, 500))

    # set up the fonts
    font = pygame.font.Font(None, 32)

    # set up the text boxes
    username_box = pygame.Rect(150, 200, 200, 32)
    password_box = pygame.Rect(150, 250, 200, 32)

    # set up the buttons
    create_button = pygame.Rect(200, 300, 100, 50)
    back_button = pygame.Rect(50, 50, 50, 50)

    # set up the colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    gray = (128, 128, 128)

    # set up the text strings
    username_str = ''
    password_str = ''

    # main loop
    running = True
    while running:

        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # check if the user clicked on the create user button
                    if create_button.collidepoint(event.pos):
                        # call the new user function and pass in the text from the boxes
                        new_user(username_str, password_str)
                    # check if the user clicked on the back button
                    elif back_button.collidepoint(event.pos):
                        # go back to the main menu screen
                        running = False
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

        # draw the window
        win.fill(white)

        # draw the text boxes
        pygame.draw.rect(win, black, username_box, 2)
        pygame.draw.rect(win, gray, password_box, 2)

        # render the text
        username_text = font.render(username_str, True, black)
        password_text = font.render('*' * len(password_str), True, black)

        # draw the text
        win.blit(username_text, (username_box.x + 5, username_box.y + 5))
        win.blit(password_text, (password_box.x + 5, password_box.y + 5))

        # draw the buttons
        pygame.draw.rect(win, gray, create_button)
        pygame.draw.rect(win, gray, back_button)

        # render the button text
        create = font.render('Create', True, black)
        back_text = font.render('Back', True, black)

        # draw the button text
        win.blit(create, (create_button.x + 25, create_button.y + 10))
        win.blit(back_text, (back_button.x + 10, back_button.y + 10))

        # update the display
        pygame.display.update()


    # quit Pygame
    pygame.quit()

# Start the new user menu
new_user_menu()

