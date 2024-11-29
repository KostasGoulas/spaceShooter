import pygame

class GameSounds:
    def __init__(self):
        self.shoot = pygame.mixer.Sound("assets\sounds\shoot-1-81135.mp3")
        self.click = pygame.mixer.Sound("assets\sounds\click.mp3")
    
    def clicked(self):
        self.click.play()
    def shooted(self):
        self.shoot.play()