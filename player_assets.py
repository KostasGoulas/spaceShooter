import pygame
from random import randint
from algos import is_point_inside_box

BLACK=(0,0,0)


class Ball(pygame.sprite.Sprite):
    def __init__(self,color, width, height):
        super().__init__()
        self.uper_lim = -100000
        self.down_lim = +100000
        self.image=pygame.Surface([width,height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.width = width
        self.height = height
        

        #pygame.draw.rect(self.image, color, [0,0,width,height] )
        pygame.draw.circle(self.image,color, [width//2, height//2], width//2  )
        self.rect=self.image.get_rect()
 
    def get_position(self):
        return (self.rect.x, self.rect.y)

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
    def moveForword(self, player):
        if player == 0 :
            self.move(5,0)
        else :
            self.move(-5, 0)


class Player(Ball):
    def __init__(self, color, width, height, player):
        super().__init__(color, width, height)
        self.player = player

class Bullet(Ball):
    def __init__(self, color, width, height, player):
        super().__init__(color, width, height)
        self.player = player
    def update(self):
        self.moveForword(self.player)

    def collition( self, obj ):
        # return True
        p1 = [obj.rect.x , obj.rect.y]
        if is_point_inside_box(self.rect.center, p1, obj.width, obj.height):
            return True
        return False


class Health():
    def __init__(self, max_helth, color, position):
        self.health_bars = max_helth
        self.pos = position
        self.color = color
        self.font = pygame.font.Font(pygame.font.get_default_font(), 60)
    
    def hited(self):
        if self.health_bars != 0:
            self.health_bars -= 1
    def empty(self):
        return self.health_bars == 0
    
    def draw(self, win):
        text_surface = self.font.render(str(self.health_bars), True, self.color)
        win.screen.blit( text_surface,self.pos )
