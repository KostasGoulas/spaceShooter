import pygame
from gameWindow import *
from endGame import *
from startGame import *
from states import *
from level1 import *
from level2 import Level_2
from scoreSystem import *
from sound import *
from algos import *



class gameManager:
    def __init__(self):
        self.startGame    = startGame()
        self.endGame      = endGame()
        self.level_1      = Level_1()
        self.level_2      = Level_2()
        self.Score        = Score()
    def setScore(self):
        score = self.level_1.character.get_score()
        if score > 0 :
            self.Score.updateScore(score)

    def onDraw(self):
        if game_State.start_screen :
            self.level_1.Reset()
            self.level_2.Reset()
            self.startGame.onDraw()
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
        if game_State.start_screen :
            self.startGame.onEvent()
        elif game_State.end_game :
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
        if game_State.start_screen :
            self.startGame.onControl()
        elif game_State.end_game :
            self.endGame.onControl()
        elif game_State.level_1 :
            self.level_1.onControl()
        elif game_State.level_2 :
            self.level_2.onControl()
        else:
            pass
