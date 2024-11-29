import pygame
from algos import *
from states import *
from window import *

class EndGameAssets :
    def __init__(self, win_size):
        self.background  = self.loadImageAsset("endgame\Window.png")
        self.background  = pygame.transform.scale( self.background, win_size ) # this is to fit the background to the window 
        self.lose        = self.loadImageAsset("endgame\Header.png")
        self.score       = self.loadImageAsset("endgame\Score.png")
        self.record      = self.loadImageAsset("endgame\Record.png")
        self.close       = self.loadImageAsset("endgame\Close_BTN.png")
        self.close_act   = self.loadImageAsset("endgame\Close_BTN2.png")
        self.replay      = self.loadImageAsset("endgame\Replay_BTN.png")
        self.replay_act  = self.loadImageAsset("endgame\Replay_BTN2.png")
    def loadImageAsset(self, name):
        return pygame.image.load(f"assets\{name}")

class endGame :
    def __init__(self):
        self.assets = EndGameAssets(win.dim)
        self.lose_x = (win.dim[0]/2) - (self.assets.lose.get_width()/2)
        self.lose_y = (win.dim[1]/20)
        self.count  = 0
        self.exit_pos = (self.lose_x, 13*self.lose_y)
        self.replay_pos = (self.lose_x + self.assets.close.get_width() + 5, 13*self.lose_y)
        self.on_replay   = False
        self.on_close    = False

    def onEvent( self ):
        x, y = control_State.mouse_pos
        self.on_close  = False
        self.on_replay = False
        if is_point_inside_box( [x,y], self.exit_pos, self.assets.close.get_width(), self.assets.close.get_height() ) :
            self.on_close = True
        if is_point_inside_box( [x,y], self.replay_pos, self.assets.replay.get_width(), self.assets.replay.get_height() ) :
            self.on_replay = True
        if control_State.mouse_down :
            if is_point_inside_box( [x,y], self.exit_pos, self.assets.close.get_width(), self.assets.close.get_height() ) :
                game_State.set_exit()
            if is_point_inside_box( [x,y], self.replay_pos, self.assets.replay.get_width(), self.assets.replay.get_height() ) :
                print("start the game")
                game_State.set_start_game()
    
    def onControl(self):
        self.count += 1
        self.count = self.count%10

    def onDraw(self) :
        win.screen.fill((0, 0, 0))
        win.screen.blit( self.assets.background,(0,0) )
        if self.count < 7:
            win.screen.blit( self.assets.lose,(self.lose_x, self.lose_y) )
            # self.screen.blit( self.assets.score,(self.lose_x, 5*self.lose_y) )
            # self.screen.blit( self.assets.record,(self.lose_x, 9*self.lose_y) )
        if self.on_close :
            win.screen.blit( self.assets.close_act,self.exit_pos )
        else :
            win.screen.blit( self.assets.close,self.exit_pos )

        if self.on_replay :
            win.screen.blit( self.assets.replay_act, self.replay_pos)
        else :
            win.screen.blit( self.assets.replay, self.replay_pos)
 
        