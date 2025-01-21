import pygame
from random import randint
BLACK=(0,0,0)

class Ball(pygame.sprite.Sprite):
    def __init__(self,color, width, height):
        super().__init__()

        self.image=pygame.Surface([width,height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        #pygame.draw.rect(self.image, color, [0,0,width,height] )
        pygame.draw.circle(self.image,color, [width//2, height//2], width//2  )
        self.rect=self.image.get_rect()

    def move(self, dx, dy):
        self.rect.x=self.rect.x + dx
        self.rect.y=self.rect.y + dy
    def moveUp(self):
        self.move(0, -5)
    def moveDown(self):
        self.move(0, 5)



