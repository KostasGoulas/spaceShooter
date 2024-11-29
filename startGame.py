import pygame 
from algos import *
from states import *

class StartGameAssets :
    def __init__(self, win_size):
        self.background   = self.loadImageAsset("small-bubbles-foam.jpg")
        self.background   = pygame.transform.scale( self.background, win_size ) # this is to fit the background to the window 
        self.startBtn     = self.loadImageAsset("startgame\Bonus_BTN_01.png")
        self.startBtn_act = self.loadImageAsset("startgame\Bonus_BTN_02.png")
    def loadImageAsset(self, name):
        return pygame.image.load(f"assets\{name}")

class ClickControl(Control):
    def execute(self, resiver):
        resiver.clicked()
class startGame :
    def __init__(self, screen, win_size,  clock, state, control, sounds):
        self.screen = screen
        self.size = win_size
        self.clock = clock
        self.assets = StartGameAssets(win_size)
        self.str_x = (win_size[0]/2) - (self.assets.startBtn.get_width()/2)
        self.str_y = (win_size[1]/2) - (self.assets.startBtn.get_height()/2)
        self.onStart = False
        self.gameState    = state
        self.controlState = control
        self.font = pygame.font.Font(pygame.font.get_default_font(), 50)
        self.controlClick = ClickControl()
        self.sounds = sounds
    def onEvent( self ):
        end = False
        self.onStart = False
        x, y = self.controlState.mouse_pos
        if is_point_inside_box( [x,y], (self.str_x,self.str_y), self.assets.startBtn.get_width(), self.assets.startBtn.get_height() ) :
            self.onStart = True
        if self.controlState.mouse_down :
            print("edw")
            if is_point_inside_box( [x,y], (self.str_x,self.str_y), self.assets.startBtn.get_width(), self.assets.startBtn.get_height() ) :
                print ( " edw ftanw ")
                self.gameState.set_start_game()
                self.controlClick.execute(self.sounds)
        return self.gameState, self.controlState
    
    def onControl(self):
        pass

    def onDraw(self) :
        self.screen.fill((0, 0, 0))
        self.screen.blit( self.assets.background,(0,0) )
        if self.onStart :
            self.screen.blit( self.assets.startBtn_act, (self.str_x-8, self.str_y-2))
            text_surface = self.font.render("START", True, (255, 200, 200, 250))
        else:
            self.screen.blit( self.assets.startBtn, (self.str_x, self.str_y))
            text_surface = self.font.render("START", True, (100, 100, 100, 50))
        self.screen.blit(text_surface, (self.str_x+20, self.str_y+80 ))

