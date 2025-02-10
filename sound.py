import pygame

class GameSounds:
    def __init__(self):
        # self.shoot = pygame.mixer.Sound("assets\sounds\shoot-1-81135.mp3")
        self.shoot = pygame.mixer.Sound("assets\sounds\shot.wav")
        self.click = pygame.mixer.Sound("assets\sounds\click.mp3")
        self.hit   = pygame.mixer.Sound("assets\sounds\explr.wav")

        # background music
        pygame.mixer.music.load("assets\sounds\8-bit-loop-189494.mp3")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.2)
    
    def clicked(self):
        self.click.play()
    def shooted(self):
        self.shoot.play()
    def hitted(self):
        self.hit.play()