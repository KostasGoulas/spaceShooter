from gameWindow import *
from endGame import *
from algos import *



class SpaceShooter(Game):
    def __init__(self, dim, title):
        super().__init__(dim, title)

    def onControl(self):
        self.manager.onControl()

    def onEvent(self):
        super().onEvent()
        self.manager.onEvent()

    def onDraw(self):
        super().onDraw()
        self.manager.onDraw()




