import pygame
from algos import truncate

class Score:
    def __init__(self, screen):
        self.screen = screen
        self.score = 0
        self.HightScore = 0
        self.font = pygame.font.Font(pygame.font.get_default_font(), 50)
        self.count = 0
    def updateScore(self, score):
        self.score = score
    def updateHightScore(self):
        if self.score > self.HightScore :
            self.HightScore = self.score
    def writeToDataBase(self):
        pass
    def readFromDataBase(self):
        pass
    def onDraw(self):
        self.updateHightScore()
        score = self.score
        hightscore = self.HightScore
        width  = self.screen.get_width()
        height = self.screen.get_height()
        score = "%.3f" %score
        hightscore = "%.3f" %hightscore
        text_surface = self.font.render(f"SCORE {score}", True, (255, 255, 255, 100))
        if self.count < 8:
            self.screen.blit(text_surface, (width/2 - 50*5, height/5 ))
        text_surface = self.font.render(f"Hight SCORE {hightscore}", True, (255, 255, 255, 100))
        if self.count < 8:
            self.screen.blit(text_surface, (width/2 - 50*5, 2*height/5 ))
        self.count += 1
        self.count %= 10
