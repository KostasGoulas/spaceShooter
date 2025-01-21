# import pygame
# from gameWiin import *
from endGame import *
from startGame import *
from states import *
from level1 import *
from level2 import Level_2
from scoreSystem import *
from sound import *
from algos import *
# import multiplayer_api as mp
from multiplayer_api import *
import boot_imp



class gameManager:
    def __init__(self):
        self.startGame    = startGame()
        self.endGame      = endGame()
        self.level_1      = Level_1()
        self.level_2      = Level_2()
        self.Score        = Score()
        self.Multiplayer  = None
        self.playerM      = None
        self.network_state = None
        self.is_connected = False
    def setScore(self):
        score = self.level_1.character.get_score()
        if score > 0 :
            self.Score.updateScore(score)

    def onDraw(self):
        if game_State.start_screen :
            self.level_1.Reset()
            self.level_2.Reset()
            self.startGame.onDraw()
        elif game_State.multiplayer and boot_imp.connections_count() == 2:
            if self.network_state == 's':
                pass
                # self.Multiplayer.onDraw()
            else :
                self.playerM.onDraw()
        elif game_State.end_game :
            self.level_1.Reset()
            self.level_2.Reset()
            self.endGame.onDraw()
            self.Score.onDraw()
        elif game_State.level_1 :
            self.level_1.onDraw()
        elif game_State.level_2 :
            self.level_2.onDraw()
        else:
            pass

    def onEvent(self):
        # if boot_imp.is_server_open() and boot_imp.connections_count == 0 :
        #     return
        if game_State.start_screen :
            self.startGame.onEvent()
        elif game_State.multiplayer :
            print( boot_imp.is_server_open() )
            if self.is_connected :
                return
            if not boot_imp.is_server_open() :
                boot_imp.set_connection_to_zero()
                boot_imp.server_open()
                self.network_state = 's'
                self.Multiplayer  = SpaceShooterMult('s')
                self.is_connected = True
                print("am i here?")
            elif self.network_state != 's' :
                self.network_state = 'c'
                self.playerM = SpaceShooterMult('c')
                boot_imp.add_connection()
                self.is_connected = True
        elif game_State.end_game :
            boot_imp.server_close()
            self.endGame.onEvent()
        elif game_State.level_1 :
            self.level_1.onEvent()
            self.setScore()
        elif game_State.level_2 :
            self.level_2.onEvent()
            self.setScore()
        else:
            pass

    def onControl(self):
        # if boot_imp.is_server_open() and boot_imp.connections_count == 0 :
        #     return
        if game_State.start_screen :
            self.startGame.onControl()
        elif game_State.multiplayer and boot_imp.connections_count() == 2:
            if self.network_state == 's':
                self.Multiplayer.onControl()
            else :
                self.playerM.onControl()
        elif game_State.end_game :
            self.endGame.onControl()
        elif game_State.level_1 :
            self.level_1.onControl()
        elif game_State.level_2 :
            self.level_2.onControl()
        else:
            pass
