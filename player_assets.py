import pygame
from random import randint
# import math

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
    def __init__(self, color, width, height):
        super().__init__(color, width, height)

# class colitionControl(math.Control):
#     def execute(self, resiver):
#         resiver.hitted()


class LevelBullets:
    def __init__(self, player):
        self.bullets              = []
        self.bullets_col          = []
        self.bullet_produse_delay = 6 #frames
        self.bulet_produse        = 0 #counter
        # self.controlColition      = colitionControl()
        self.BLACK=(0,0,0)
        self.WHITE=(255,255,255)
        self.GREEN=(0,255,0)
        self.player = player
        self.all_sprites_list=pygame.sprite.Group()
    def onReset(self):
        self.bullets = []
        self.bullets_col = []

    def addBullet(self, pos):
        if self.bulet_produse == self.bullet_produse_delay :
            bullet = Ball(self.GREEN, 10, 10 )
            bullet.rect.center = pos
            self.bullets.append( bullet )
            self.all_sprites_list.add( bullet )
            
            self.bullets_col.append(0)
            self.bulet_produse = 0
    
    def popBullet(self):
        pop_bullet = False
        for i in range( len(self.bullets) ):
            bullet = self.bullets[i]
            if self.bullets_col[i] == 0 :
                bullet.moveForword( self.player )
            if bullet.rect.x > 800 or bullet.rect.x < 0 :
                pop_bullet = True
        if pop_bullet :
            self.bullets.pop(0)
            self.all_sprites_list.empty()
            for bullet in self.bullets:
                self.all_sprites_list.add(bullet)
            self.bullets_col.pop(0)
            print("delete buulet")

        bullets_new = []
        bullet_col_new = []
        for i in range( len(self.bullets) ):
            bullet = self.bullets[i]
            if self.bullets_col[i] >= 6:
                continue
            bullets_new.append(bullet)
            bullet_col_new.append(self.bullets_col[i])
        self.bullets = bullets_new
        self.bullets_col = bullet_col_new

    # def controlColitionPerEnemy(self, enemy):
    #     return_val = False
    #     for i in range(len(self.bullets)):
    #         bullet = self.bullets[i]
    #         # if bullet.collition( enemy ):
    #         if self.bullets_col[i] > 0 or enemy.collition( bullet ) :
    #             print( "collition ")
    #             self.bullets_col[i] += 1
    #             if self.bullets_col[i]%2 == 0:
    #                 self.bullets[i].x += 1
    #             else :
    #                 self.bullets[i].x -=1
    #             if self.bullets_col[i] == 1:
    #                 self.bullets[i].x -= (self.bullets[i].asset_colition.get_width()/2) + (self.bullets[i].asset.get_width()/2)
    #                 self.bullets[i].y -= (self.bullets[i].asset_colition.get_height())
    #                 return_val = True
    #     return return_val

    def onControl(self, event, pos):
        if event :
            print( " ADDDED ")
            self.addBullet(pos)
        if self.bulet_produse != self.bullet_produse_delay:
            self.bulet_produse += 1
        self.popBullet()
    def onDraw(self, win):
        for i in range( len(self.bullets )):
            bullet = self.bullets[i]
            # bullet.update()
            # bullet.draw()
            self.all_sprites_list.update()
            self.all_sprites_list.draw()
            # win.screen.blit( bullet.rect, bullet.get_position() )
