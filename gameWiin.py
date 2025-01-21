import pygame
from gameManager import *
from states import *
from window import *

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
        win.setWinFilds(self.screen, dim, title, self.clock)
        self.manager = gameManager()
        self.right_pressed = False
        self.left_pressed = False
        self.space_pressed = False
        self.icon = pygame.image.load("assets\icon.svg")
        pygame.display.set_icon(self.icon)
        self.conntrol = ClickControl()
    def onEvent(self):
        self.end = game_State.exit
        control_State.reset()
        keys = pygame.key.get_pressed()
        x, y = pygame.mouse.get_pos()
        control_State.mouse_pos = (x,y)
        if pygame.mouse.get_pressed()[0] :
            print("click")
            control_State.mouse_down = True
        if keys[pygame.K_RIGHT] :
            control_State.set_right()
            print("Right pressed")
        if keys[pygame.K_LEFT] :
            control_State.set_left()
            print("Left pressed")
        if keys[pygame.K_SPACE] : 
            control_State.set_space()
            print("Space Pressed")
        if keys[pygame.K_UP] :
            control_State.set_up()
            print("Up pressed")
        if keys[pygame.K_DOWN] :
            control_State.set_down()
            print("Down pressed")
        super().onEvent()
    def onDraw(self):
        if not game_State.exit :
            super().onDraw()
        