import pygame
from gameWindow import *
from endGame import *
from startGame import *
from states import *


class GameObject:
    def __init__(self, asset, x, y):
        self.asset = asset
        self.x     = x
        self.y     = y
    
    def position(self):
        return [self.x, self.y]

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
    def update(self, dx, dy):
        self.x += dx
        self.y += dy

class Bullet(GameObject):
    def __init__(self, asset, x, y, speed, asset_colition):
        super().__init__(asset, x, y)
        self.speed = speed
        self.asset_colition = asset_colition
    def move_forword( self ):
        self.update(0,-self.speed)
    def get_asset(self,is_colition):
        if is_colition > 0:
            return self.asset_colition
        return self.asset

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
class Level_1 :
    def __init__(self, screen, dim, clock, title, state, control ):
        self.assets  = GameAssets(dim)
        self.size = dim
        char = self.assets.move_left # in this version left right and char is the same
        char_x  = (dim[0]/2) - char.get_width()/2
        char_y  = dim[1] - dim[1]/20 - char.get_height()
        self.move_dis = char.get_width()/4 

        self.character = GameObject(char, char_x, char_y)
        self.bullets = []
        self.bullets_col = []
        self.enemes  = [ GameObject(self.assets.enemys[2], char_x, 140+self.assets.enemys[2].get_height()) ]
        self.init_bullet_pos_y =  char_y-self.assets.bullet.get_height()

        self.bullet_probuse_delay = 6 #frames
        self.bulet_produse = 0

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
        self.bullets = []
        self.bullets_col = []

    def onControl(self):
        char = self.character
        if self.controlState.right and (char.x < (self.size[0]-char.asset.get_width())):
            char.x += self.move_dis
        
        if self.controlState.left and (char.x > 0):
            char.x -= self.move_dis

        if self.controlState.space :
            if self.bulet_produse == self.bullet_probuse_delay :
                self.bullets.append( Bullet(self.assets.bullet, self.character.x + self.character.asset.get_width()/2, self.init_bullet_pos_y, 6, self.assets.bullet_expl ) )
                self.bullets_col.append( 0 )
                self.bulet_produse = 0
        if self.bulet_produse != self.bullet_probuse_delay:
            self.bulet_produse += 1
        
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
        for enemy in self.enemes:
            self.controlColitionPerEnemy(enemy)
        
        if len( self.helthBars ) == 0 :
            self.gameState.set_end_game()

    def controlColitionPerEnemy(self, enemy):
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
                    if len(self.helthBars) > 0:
                        self.helthBars.pop()
    def onEvent(self):
        return self.gameState, self.controlState;

    
    def onDraw(self):
        self.screen.blit( self.assets.background,(0,0) )
        self.screen.blit( self.character.asset, self.character.position() )
        for enemy in self.enemes :
            self.screen.blit( enemy.asset, enemy.position() )
        for i in range( len(self.bullets )):
            bullet = self.bullets[i]
            self.screen.blit( bullet.get_asset( self.bullets_col[i] ), bullet.position() )
        
        self.screen.blit(self.healthTable, self.helthPos)
        for bar in self.helthBars : 
            self.screen.blit( bar.asset, bar.position())

class gameManager:
    def __init__(self, screen, win_size, clock, title):
        self.gameState = gameSate()
        self.controlState = controlState()
        self.startGame = startGame( screen, win_size, clock, self.gameState, self.controlState )
        self.endGame   = endGame( screen, win_size, clock, self.gameState, self.controlState )
        self.level_1   = Level_1( screen, win_size, clock, title, self.gameState, self.controlState )
        
    def onDraw(self):
        if self.gameState.start_screen :
            self.level_1.Reset()
            self.startGame.onDraw()
        elif self.gameState.end_game :
            self.level_1.Reset()
            self.endGame.onDraw()
        elif self.gameState.level_1 :
            print("edw ksana")
            self.level_1.onDraw()
        else:
            pass
    def onEvent(self):
        if self.gameState.start_screen :
            self.gameState, self.controlState = self.startGame.onEvent()
        elif self.gameState.end_game :
            self.gameState, self.controlState = self.endGame.onEvent()
        elif self.gameState.level_1 :
            self.gameState, self.controlState = self.level_1.onEvent()
        else:
            pass
    def onControl(self):
        if self.gameState.start_screen :
            self.startGame.onControl()
        elif self.gameState.end_game :
            self.endGame.onControl()
        elif self.gameState.level_1 :
            self.level_1.onControl()
        else:
            pass
