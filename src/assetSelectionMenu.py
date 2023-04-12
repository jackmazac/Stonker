import button
class assetSelectionMenu():
    def __init__(self,display):
        self.screen=display
        self.position=(0,0)
        self.size=(100,675)
        self.buttonTSLA=button.button(self.screen,125,75,'Blue','Red',(0,0))
        self.buttonSPX=button.button(self.screen,125,75,'Blue','Red',(0,100))
    
    

    def draw(self,isActive):
        if isActive:
            self.buttonTSLA.draw()
            self.buttonSPX.draw()
        else:
            isActive=False