from gameWindow import *
from endGame import *
from algos import *

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

class SpaceShooter(Game):
    def __init__(self, dim, title):
        super().__init__(dim, title)
        self.assets  = GameAssets(self.size)
        char = self.assets.move_left # in this version left right and char is the same
        char_x  = (self.size[0]/2) - char.get_width()/2
        char_y  = self.size[1] - self.size[1]/20 - char.get_height()
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

        self.isGameOver  = False
        self.gameOver = endGame( self.screen, self.size, self.clock )
        self.restart  = False
    def onRestart(self):
        self.helthBars = [ GameObject(self.healthBar, self.FirstBarPos[0] + i*self.health_bar_width, self.FirstBarPos[1] ) for i in range(0,8) ]

    def onControl(self):
        if self.restart :
            self.onRestart()
            self.isGameOver = False
            self.restart = False
        if self.isGameOver :
            self.gameOver.onControl()
        else :
            char = self.character
            if self.right_pressed and (char.x < (self.size[0]-char.asset.get_width())):
                char.x += self.move_dis
            
            if self.left_pressed and (char.x > 0):
                char.x -= self.move_dis

            if self.space_pressed :
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
                self.isGameOver = True

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
        if not self.is_start :
            self.end, self.is_start = self.start.onEvent(self.is_start)
        else :
            if self.isGameOver :
                self.end, self.restart = self.gameOver.onEvent()
            else :
                return super().onEvent()

    
    def onDraw(self):
        super().onDraw()
        if not self.is_start :
            self.start.onDraw()
        else:
            print(self.is_start)
            if self.isGameOver :
                self.gameOver.onDraw()
            else :
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
        