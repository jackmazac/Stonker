import pygame
import assetSelectionMenu
from sys import exit
pygame.init()
gameClock=pygame.time.Clock()
MainDisplay=pygame.display.set_mode((1250,675))
MainDisplay.fill('Gray')
AssetSelectionMenu=assetSelectionMenu.assetSelectionMenu(MainDisplay)
AssetSelectionMenuIsActive=True
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
    AssetSelectionMenu.draw(AssetSelectionMenuIsActive)
    pygame.display.update()

