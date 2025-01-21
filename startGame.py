import pygame 
from algos import *
from states import *
from sound import *
from window import *

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
    def __init__(self):
        self.assets = StartGameAssets(win.dim)
        self.str_x = (win.dim[0]/2) - (self.assets.startBtn.get_width()/2)
        self.str_y = (win.dim[1]/2) - (self.assets.startBtn.get_height()/2) - 120
        self.str_mult_x = self.str_x 
        self.str_mult_y = self.str_y + 280 
        self.onStart = False
        self.onMultyPlayers = False
        self.font = pygame.font.Font(pygame.font.get_default_font(), 25)
        self.controlClick = ClickControl()
        self.sounds       = GameSounds()
    def onEvent( self ):
        end = False
        self.onStart = False
        self.onMultyPlayers = False
        x, y = control_State.mouse_pos
        if is_point_inside_box( [x,y], (self.str_x,self.str_y), self.assets.startBtn.get_width(), self.assets.startBtn.get_height() ) :
            self.onStart = True
        if control_State.mouse_down :
            print("edw")
            if is_point_inside_box( [x,y], (self.str_x,self.str_y), self.assets.startBtn.get_width(), self.assets.startBtn.get_height() ) :
                print ( " edw ftanw ")
                game_State.set_start_game()
                self.controlClick.execute(self.sounds)
        
        if is_point_inside_box( [x,y], (self.str_mult_x,self.str_mult_y), self.assets.startBtn.get_width(), self.assets.startBtn.get_height() ) :
            self.onMultyPlayers = True
        if control_State.mouse_down :
            print("edw")
            if is_point_inside_box( [x,y], (self.str_mult_x,self.str_mult_y), self.assets.startBtn.get_width(), self.assets.startBtn.get_height() ) :
                print ( " edw ftanw ")
                # game_State.set_start_game()
                game_State.set_mult()
                self.controlClick.execute(self.sounds)
    
    def onControl(self):
        pass

    def onDraw(self) :
        win.screen.fill((0, 0, 0))
        win.screen.blit( self.assets.background,(0,0) )
        if self.onStart :
            win.screen.blit( self.assets.startBtn_act, (self.str_x-8, self.str_y-2))
            text_surface = self.font.render("Single Player", True, (255, 200, 200, 250))
        else:
            win.screen.blit( self.assets.startBtn, (self.str_x, self.str_y))
            text_surface = self.font.render("Single Player", True, (100, 100, 100, 50))
        win.screen.blit(text_surface, (self.str_x+20, self.str_y+90 ))
        
        if self.onMultyPlayers :
            win.screen.blit( self.assets.startBtn_act, (self.str_mult_x-8, self.str_mult_y-2 ))
            text_surface = self.font.render(" Multi Player", True, (255, 200, 200, 250))
        else:
            win.screen.blit( self.assets.startBtn, (self.str_mult_x, self.str_mult_y))
            text_surface = self.font.render(" Multi Player", True, (100, 100, 100, 50))
        win.screen.blit(text_surface, (self.str_mult_x+20, self.str_mult_y+90 ))

