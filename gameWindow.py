import pygame
from gameManager import *

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
        self.manager = gameManager( self.screen, dim, self.clock, title )
        self.right_pressed = False
        self.left_pressed = False
        self.space_pressed = False
    def onEvent(self):
        super().onEvent()
        self.end = self.manager.gameState.exit
        self.manager.controlState.reset()
        keys = pygame.key.get_pressed()
        x, y = pygame.mouse.get_pos()
        self.manager.controlState.mouse_pos = (x,y)
        if pygame.mouse.get_pressed()[0] :
            print("click")
            self.manager.controlState.mouse_down = True
        if keys[pygame.K_RIGHT] :
            self.manager.controlState.set_right()
            print("Right pressed")
        if keys[pygame.K_LEFT] :
            self.manager.controlState.set_left()
            print("Left pressed")
        if keys[pygame.K_SPACE] : 
            self.manager.controlState.set_space()
            print("Space Pressed")
    def onDraw(self):
        if not self.manager.gameState.exit :
            super().onDraw()
        