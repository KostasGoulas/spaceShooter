import pygame
from random import randint
BLACK=(0,0,0)

class Ball(pygame.sprite.Sprite):
    def __init__(self,color, width, height):
        super().__init__()

        self.uper_lim = -100000
        self.down_lim = +100000
        self.image=pygame.Surface([width,height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        #pygame.draw.rect(self.image, color, [0,0,width,height] )
        pygame.draw.circle(self.image,color, [width//2, height//2], width//2  )
        self.rect=self.image.get_rect()
    
    def set_uper_and_down_lims(self, up, down):
        self.uper_lim = up
        self.down_lim = down

    def move(self, dx, dy):
        self.rect.x=self.rect.x + dx
        if self.rect.y + dy > self.uper_lim and self.rect.y + dy < self.down_lim:
            self.rect.y=self.rect.y + dy
    def moveUp(self):
        self.move(0, -10)
    def moveDown(self):
        self.move(0, 10)



