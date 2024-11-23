import pygame
from gameWindow import *
from endGame import *
from startGame import *
from states import *
from level1 import *
from scoreSystem import *

class gameManager:
    def __init__(self, screen, win_size, clock, title):
        self.gameState = gameSate()
        self.controlState = controlState()
        self.startGame = startGame( screen, win_size, clock, self.gameState, self.controlState )
        self.endGame   = endGame( screen, win_size, clock, self.gameState, self.controlState )
        self.level_1   = Level_1( screen, win_size, clock, title, self.gameState, self.controlState )
        self.Score     = Score()

    def setScore(self):
        score = self.level_1.character.get_score()
        if score > 0 :
            self.Score.updateScore(score)
            self.Score.updateHightScore()

    def onDraw(self):
        if self.gameState.start_screen :
            self.level_1.Reset()
            self.startGame.onDraw()
        elif self.gameState.end_game :
            self.level_1.Reset()
            self.endGame.onDraw()
            self.Score.onDraw()
        elif self.gameState.level_1 :
            self.level_1.onDraw()
        else:
            pass

    def onEvent(self):
        if self.gameState.start_screen :
            self.gameState, self.controlState = self.startGame.onEvent()
        elif self.gameState.end_game :
            self.gameState, self.controlState = self.endGame.onEvent()
        elif self.gameState.level_1 :
            self.gameState, self.controlState = self.level_1.onEvent()
            self.setScore()
        else:
            pass

    def onControl(self):
        if self.gameState.start_screen :
            self.startGame.onControl()
        elif self.gameState.end_game :
            self.endGame.onControl()
        elif self.gameState.level_1 :
            self.level_1.onControl()
        else:
            pass
