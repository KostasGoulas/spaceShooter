import pygame

class EndGameAssets :
    def __init__(self, win_size):
        self.background  = self.loadImageAsset("endgame\Window.png")
        self.background  = pygame.transform.scale( self.background, win_size ) # this is to fit the background to the window 
        self.lose        = self.loadImageAsset("endgame\Header.png")
        self.score       = self.loadImageAsset("endgame\Score.png")
        self.record      = self.loadImageAsset("endgame\Record.png")
    def loadImageAsset(self, name):
        return pygame.image.load(f"assets\{name}")

class endGame :
    def __init__(self, screen, win_size,  clock):
        self.screen = screen
        self.clock  = clock
        self.assets = EndGameAssets(win_size)
        self.lose_x = (win_size[0]/2) - (self.assets.lose.get_width()/2)
        self.lose_y = (win_size[1]/20)
        self.count  = 0
    def onEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.end = True
    
    def onControl(self):
        self.count += 1
        self.count = self.count%10

    def onDraw(self) :
        self.screen.fill((0, 0, 0))
        self.screen.blit( self.assets.background,(0,0) )
        if self.count > 5:
            print( self.count )
            self.screen.blit( self.assets.lose,(self.lose_x, self.lose_y) )
            self.screen.blit( self.assets.score,(self.lose_x, 5*self.lose_y) )
            self.screen.blit( self.assets.record,(self.lose_x, 9*self.lose_y) )
 
        