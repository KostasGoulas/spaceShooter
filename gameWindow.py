import pygame
from startGame import *

# basic class
class GameWindow :
    def __init__(self, dim, title) :
        pygame.init()
        self.size = dim
        self.screen = pygame.display.set_mode(dim)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.end = False
    
    def onEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.end = True
    
    def onControl(self):
        pass

    def onDraw(self) :
        self.screen.fill((250, 250, 250))

    def run(self) :
        while not self.end :
            self.onEvent()
            self.onControl()
            self.onDraw()
            pygame.display.update()
            self.clock.tick(30)


# basic game window with event handle for right left and space keys:
class Game(GameWindow):
    def __init__(self, dim, title):
        super().__init__(dim, title)
        self.right_pressed = False
        self.left_pressed = False
        self.space_pressed = False
        self.start = startGame( self.screen, dim, self.clock )
        self.is_start = False
    def onEvent(self):
        super().onEvent()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] :
            self.right_pressed = True
            print("Right pressed")
        else:
            self.right_pressed = False
        if keys[pygame.K_LEFT] :
            self.left_pressed = True
            print("Left pressed")
        else :
            self.left_pressed = False
        if keys[pygame.K_SPACE] : 
            self.space_pressed = True
            print("Space Pressed")
        else :
            self.space_pressed = False
        