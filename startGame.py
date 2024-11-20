import pygame 
from algos import *

class StartGameAssets :
    def __init__(self, win_size):
        self.background   = self.loadImageAsset("small-bubbles-foam.jpg")
        self.background   = pygame.transform.scale( self.background, win_size ) # this is to fit the background to the window 
        self.startBtn     = self.loadImageAsset("startgame\Bonus_BTN_01.png")
        self.startBtn_act = self.loadImageAsset("startgame\Bonus_BTN_02.png")
    def loadImageAsset(self, name):
        return pygame.image.load(f"assets\{name}")
class startGame :
    def __init__(self, screen, win_size,  clock):
        self.screen = screen
        self.size = win_size
        self.clock = clock
        self.assets = StartGameAssets(win_size)
        self.str_x = (win_size[0]/2) - (self.assets.startBtn.get_width()/2)
        self.str_y = (win_size[1]/2) - (self.assets.startBtn.get_height()/2)
        self.onStart = False
    def onEvent( self, is_start ):
        end = False
        start = is_start
        self.onStart = False
        x, y = pygame.mouse.get_pos()
        if is_point_inside_box( [x,y], (self.str_x,self.str_y), self.assets.startBtn.get_width(), self.assets.startBtn.get_height() ) :
            self.onStart = True
        for event in pygame.event.get():
            self.on_replay   = False
            self.on_close    = False
            if event.type == pygame.QUIT:
                end = True
            if event.type == pygame.MOUSEBUTTONDOWN :
                x, y = pygame.mouse.get_pos()
                if is_point_inside_box( [x,y], (self.str_x,self.str_y), self.assets.startBtn.get_width(), self.assets.startBtn.get_height() ) :
                    start = True
        return end, start

    def onDraw(self) :
        self.screen.fill((0, 0, 0))
        self.screen.blit( self.assets.background,(0,0) )
        if self.onStart :
            self.screen.blit( self.assets.startBtn_act, (self.str_x-8, self.str_y-2))
        else:
            self.screen.blit( self.assets.startBtn, (self.str_x, self.str_y))