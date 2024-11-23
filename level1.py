import pygame
from gameObjects import *

class GameAssets :
    def __init__(self, win_size):
        self.simple_char = self.loadImageAsset("Missile_03.png");
        self.simple_char = pygame.transform.scale(self.simple_char, ( self.simple_char.get_width()/4, self.simple_char.get_height()/4) )
        self.move_right  = self.loadImageAsset("Missile_03.png");
        self.move_right  = pygame.transform.scale(self.move_right, ( self.move_right.get_width()/4, self.move_right.get_height()/4) )
        self.move_left   = self.loadImageAsset("Missile_03.png")
        self.move_left   = pygame.transform.scale(self.move_left, ( self.move_left.get_width()/4, self.move_left.get_height()/4) )
        self.background  = self.loadImageAsset("small-bubbles-foam.jpg")
        self.background  = pygame.transform.scale( self.background, win_size ) # this is to fit the background to the window 
        self.bullet      = self.loadImageAsset("Rocket_Effect_01.png")
        self.bullet      = pygame.transform.scale( self.bullet, (self.bullet.get_width()/16, self.bullet.get_height()/16))
        self.bullet_expl = self.loadImageAsset("Explosion_01.png")
        self.bullet_expl = pygame.transform.scale( self.bullet_expl, (self.bullet_expl.get_width()/16, self.bullet_expl.get_height()/16))
        self.enemys      = [ self.loadImageAsset(f"enemy\{i}.png") for i in range(8,17) ]
        for i in range( len(self.enemys)):
            self.enemys[i] = pygame.transform.scale( self.enemys[i], (self.enemys[i].get_width()/8, self.enemys[i].get_height()/8))
        self.healthTable = self.loadImageAsset("health\Health_Bar_Table.png")
        self.healthTable = pygame.transform.scale(self.healthTable, (self.healthTable.get_width()/2, self.healthTable.get_height()/2))
        self.healthBar   = self.loadImageAsset("health\Health_Dot.png")
        # self.healthBar   = pygame.transform.scale(self.healthBar, (self.healthBar.get_width()/2, self.healthBar.get_height()/2))
        self.healthBar   = pygame.transform.scale(self.healthBar, (21, self.healthBar.get_height()/2))
    def loadImageAsset(self, name):
        return pygame.image.load(f"assets\{name}")
    
class LevelBullets:
    def __init__(self, init_pos, asset, asset2, speed = 6):
        self.bullets              = []
        self.bullets_col          = []
        self.bullet_produse_delay = 6 #frames
        self.bulet_produse        = 0 #counter
        self.init_pos             = init_pos #(self.character.x + self.character.asset.get_width()/2, self.init_bullet_pos_y)
        self.asset                = asset
        self.asset2               = asset2 # on colition
        self.speed                = 6
    
    def onReset(self):
        self.bullets = []
        self.bullets_col = []

    def addBullet(self):
        if self.bulet_produse == self.bullet_produse_delay :
            self.bullets.append( Bullet(self.asset, self.init_pos[0], self.init_pos[1], self.speed, self.asset2) )
            self.bullets_col.append(0)
            self.bulet_produse = 0
    
    def popBullet(self):
        pop_bullet = False
        for i in range( len(self.bullets) ):
            bullet = self.bullets[i]
            if self.bullets_col[i] == 0 :
                bullet.move_forword()
            if bullet.y < 0 or self.bullets_col[i] >= 6:
                pop_bullet = True
        if pop_bullet :
            self.bullets.pop(0)
            self.bullets_col.pop(0)
            print("delete buulet")

    def controlColitionPerEnemy(self, enemy):
        return_val = False
        for i in range(len(self.bullets)):
            bullet = self.bullets[i]
            # if bullet.collition( enemy ):
            if self.bullets_col[i] > 0 or enemy.collition( bullet ) :
                print( "collition ")
                self.bullets_col[i] += 1
                if self.bullets_col[i]%2 == 0:
                    self.bullets[i].x += 1
                else :
                    self.bullets[i].x -=1
                if self.bullets_col[i] == 1:
                    self.bullets[i].x -= (self.bullets[i].asset_colition.get_width()/2) + (self.bullets[i].asset.get_width()/2)
                    self.bullets[i].y -= (self.bullets[i].asset_colition.get_height())
                    return_val = True
        return return_val

    def onControl(self, event):
        if event :
            self.addBullet()
        if self.bulet_produse != self.bullet_produse_delay:
            self.bulet_produse += 1
        self.popBullet()
    def onDraw(self, screen):
        for i in range( len(self.bullets )):
            bullet = self.bullets[i]
            screen.blit( bullet.get_asset( self.bullets_col[i] ), bullet.position() )

class Level_1 :
    def __init__(self, screen, dim, clock, title, state, control ):
        self.assets  = GameAssets(dim)
        self.size = dim
        char = self.assets.move_left # in this version left right and char is the same
        char_x  = (dim[0]/2) - char.get_width()/2
        char_y  = dim[1] - dim[1]/20 - char.get_height()
        self.move_dis = char.get_width()/4 

        self.character = GameObject(char, char_x, char_y)

        #bullets
        self.init_bullet_pos_y =  char_y-self.assets.bullet.get_height()
        self.Bullets = LevelBullets( (self.character.x + self.character.asset.get_width()/2, self.init_bullet_pos_y), self.assets.bullet, self.assets.bullet_expl )
        self.enemes  = [ GameObject(self.assets.enemys[2], char_x, 140+self.assets.enemys[2].get_height()) ]

        # HEALTH:
        self.helthPos = (15,15)
        self.FirstBarPos = (15+3, 15+3)
        self.healthTable = self.assets.healthTable
        self.healthBar   = self.assets.healthBar
        self.health_bar_width = self.healthBar.get_width()
        self.helthBars = [ GameObject(self.healthBar, self.FirstBarPos[0] + i*self.health_bar_width, self.FirstBarPos[1] ) for i in range(0,8) ]
        self.isGameOver = False
        self.screen = screen
        self.gameState = state
        self.controlState = control

    def Reset(self):
        self.helthBars = [ GameObject(self.healthBar, self.FirstBarPos[0] + i*self.health_bar_width, self.FirstBarPos[1] ) for i in range(0,8) ]
        self.Bullets.onReset()

    def onControl(self):
        char = self.character
        if self.controlState.right and (char.x < (self.size[0]-char.asset.get_width())):
            char.x += self.move_dis
        
        if self.controlState.left and (char.x > 0):
            char.x -= self.move_dis

        self.Bullets.onControl(self.controlState.space)

        for enemy in self.enemes:
            if self.Bullets.controlColitionPerEnemy(enemy) :
                self.helthBars.pop()
        
        if len( self.helthBars ) == 0 :
            self.gameState.set_end_game()

    def onEvent(self):
        return self.gameState, self.controlState;

    
    def onDraw(self):
        self.screen.blit( self.assets.background,(0,0) )
        self.screen.blit( self.character.asset, self.character.position() )
        for enemy in self.enemes :
            self.screen.blit( enemy.asset, enemy.position() )
        
        self.Bullets.onDraw(self.screen)
        
        self.screen.blit(self.healthTable, self.helthPos)
        for bar in self.helthBars : 
            self.screen.blit( bar.asset, bar.position())
