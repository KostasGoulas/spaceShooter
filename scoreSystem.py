import pygame
from algos import truncate
from database import *
from window import *

class Score:
    def __init__(self):
        self.DB = GamesDataBase()
        self.score = 0
        self.name = "USER"
        
        hs = self.DB.readFirst()
        self.hightscore_name = ""
        self.HightScore = 0
        if len(hs) > 0 :
            self.hightscore_name = hs[1]
            self.HightScore = float(hs[2])
        
        self.font = pygame.font.Font(pygame.font.get_default_font(), 50)
        self.count = 0

    def updateScore(self, score):
        self.score = score

    def updateHightScore(self):
        # id is based 1 
        if self.score > self.HightScore :
            self.HightScore = self.score
            size = self.DB.size()
            print(size)
            if size == 0 :
                self.insertToDataBase(self.name, self.HightScore)
            else :
                tmp = self.UpdateDataBase(1,self.name, self.HightScore)
                if size > 1:
                    for i in range( 2, size ):
                        tmp = self.UpdateDataBase( i, tmp[1], float(tmp[2]))
                self.insertToDataBase(self.name, float(tmp[2]) )

    def insertToDataBase(self, name, score):
        self.DB.insert(name, score)

    def UpdateDataBase(self, id, name, score):
        return self.DB.update(id, name, score)

    def readFromDataBase(self):
        return self.DB.readTable()
    
    def readFirst(self):
        return self.DB.readFirst()
    
    def onDraw(self):
        self.updateHightScore()
        score = self.score
        hightscore = self.HightScore
        width  = win.screen.get_width()
        height = win.screen.get_height()
        score = "%.3f" %score
        hightscore = "%.3f" %hightscore
        text_surface = self.font.render(f"SCORE {score}", True, (255, 255, 255, 100))
        if self.count < 8:
            win.screen.blit(text_surface, (width/2 - 50*5, height/5 ))
        text_surface = self.font.render(f"Hight SCORE {hightscore}", True, (255, 255, 255, 100))
        if self.count < 8:
            win.screen.blit(text_surface, (width/2 - 50*5, 2*height/5 ))
        self.count += 1
        self.count %= 10
