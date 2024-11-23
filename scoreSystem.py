
class Score:
    def __init__(self):
        self.score = 0
        self.HightScore = 0
    def updateScore(self, score):
        self.score = score
    def updateHightScore(self):
        if self.score > self.HightScore :
            self.HightScore = self.score
    def onDraw(self):
        pass
