import pygame
from random import randint
from algos import is_point_inside_box

BLACK=(0,0,0)


class GameAssets_m :
    def __init__(self, width):
        self.playerRed = self.loadImageAsset("spaceRed.png")
        self.playerRed = pygame.transform.scale(self.playerRed, (width, width))
        self.playerBlue = self.loadImageAsset("spaceBlue.png")
        self.playerBlue = pygame.transform.scale(self.playerBlue, (width, width))
    def loadImageAsset(self, name):
        return pygame.image.load(f"assets\{name}")

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
        velocity = 10
        if player == 0 :
            self.move(velocity,0)
        else :
            self.move(-velocity, 0)

class GameObject:
    def __init__(self, asset, x, y):
        self.uper_lim = -100000
        self.down_lim = +100000
        self.asset = asset
        self.x     = x
        self.y     = y
    
    def get_position(self):
        return [self.x, self.y]
    
    def set_uper_and_down_lims(self, up, down):
        self.uper_lim = up
        self.down_lim = down

    def collition( self, obj ):
        p1 = [obj.x                      , obj.y]
        p2 = [obj.x+obj.asset.get_width(), obj.y]
        p3 = [obj.x+obj.asset.get_width(), obj.y-obj.asset.get_height()]
        p4 = [obj.x                      , obj.y-obj.asset.get_height()]
        if is_point_inside_box(p1, self.position(), self.asset.get_width(), self.asset.get_height()):
            return True
        elif is_point_inside_box(p2, self.position(), self.asset.get_width(), self.asset.get_height()):
            return True
        elif is_point_inside_box(p3, self.position(), self.asset.get_width(), self.asset.get_height()):
            return True
        elif is_point_inside_box(p4, self.position(), self.asset.get_width(), self.asset.get_height()):
            return True
        return False
    def move(self, dx, dy):
        self.x=self.x + dx
        if self.y + dy > self.uper_lim and self.y + dy < self.down_lim:
            self.y=self.y + dy
    def moveUp(self):
        self.move(0, -10)
    def moveDown(self):
        self.move(0, 10)
    def moveForword(self, player):
        if player == 0 :
            self.move(5,0)
        else :
            self.move(-5, 0)

class Player(GameObject):
    def __init__(self, player, width, x, y):
        assets = GameAssets_m(width)
        self.x = x
        self.y = y
        self.width = assets.playerRed.get_width()
        self.height = assets.playerRed.get_height()
        if player == 0:
            super().__init__(assets.playerBlue, x, y)
        else :
            super().__init__(assets.playerRed, x, y)

        self.player = player

class Bullet(Ball):
    def __init__(self, color, width, height, player):
        super().__init__(color, width, height)
        self.player = player
    def update(self):
        self.moveForword(self.player)

    def collition( self, obj ):
        # return True
        p1 = [obj.x , obj.y]
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
