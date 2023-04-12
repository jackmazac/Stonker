#BUTTON CLASS SYNTAX:
#button(screen that button sits on,button width, button height,color of idle button,color of pressed button,position of button)
import pygame
#import Menu
from sys import exit
clock=pygame.time.Clock()
screen1=pygame.display.set_mode((500,500))
class button(pygame.sprite.Sprite): 

    def __init__(self,screen,width,height,colorIdle,colorPressed,pos):
        #super(Button, self).__init__(*groups)            
       
        # Core Attributes
        self.screen = screen
        self.buttonPos = (pos[0], pos[1]) # Coordinates
        self.hover = False
        self.height=height
        self.width=width
        self.colorIdle=colorIdle
        self.colorPressed=colorPressed
        self.buttonIdleSurface=pygame.Surface((width,height))
        self.buttonIdleSurface.fill(colorIdle)
        self.buttonPressedSurface=pygame.Surface((width,height))
        self.buttonPressedSurface.fill(colorPressed)
        self.buttonIdleRect = pygame.rect.Rect((self.buttonPos), (self.width,self.height))
        self.buttonPressedRect = pygame.rect.Rect((self.buttonPos), (self.width,self.height))

        
        # Load the png image
        #self.start_button_idle = pygame.image.load("Media/Graphics/START_Button_idle.png")
        #self.start_button_pressed = pygame.image.load("Media/Graphics/START_Button_pressed.png")

        # Creates rectangle objects to place the image
        
    def draw(self):
        self.check_hover()

    def check_hover(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.buttonIdleRect.collidepoint(mouse_pos):
            self.screen.blit(self.buttonPressedSurface, self.buttonPressedRect)
            if self.hover != True: # logic to only play sound once
                #self.game.choose_sound.play()
                self.hover = True
        else:
            self.screen.blit(self.buttonIdleSurface, self.buttonIdleRect)
            if self.hover == True:
                self.hover = False

    # Choosing an option w/ Mouse Click
    def MouseClick(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.game.choose_sound.play()
            #return self.difficulty 


    