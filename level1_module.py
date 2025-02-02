
import pygame
from gameObjects import *
import math
import numpy as np 
import matplotlib.pyplot as plt  
from random import random
from algos import *
from sound import *
from states import *
from window import *

class newBulletControl(Control):
    def execute(self, resiver):
        resiver.shooted()

class colitionControl(Control):
    def execute(self, resiver):
        resiver.hitted()
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
        self.enemy_helth_table = self.loadImageAsset("enemy\Boss_HP_Table.png")
        self.enemy_helth_table = pygame.transform.scale(self.enemy_helth_table, (self.enemy_helth_table.get_width()/16, self.enemy_helth_table.get_height()/3))
        self.enemy_health_bar1 = self.loadImageAsset("enemy\Boss_HP_Bar_1.png")
        self.enemy_health_bar1 = pygame.transform.scale(self.enemy_health_bar1, (self.enemy_health_bar1.get_width()/(4), self.enemy_health_bar1.get_height()/3))
        self.enemy_health_bar2 = self.loadImageAsset("enemy\Boss_HP_Bar_2.png")
        self.enemy_health_bar2 = pygame.transform.scale(self.enemy_health_bar2, (self.enemy_health_bar1.get_width(), self.enemy_health_bar2.get_height()/3))
        self.enemy_health_bar3 = self.loadImageAsset("enemy\Boss_HP_Bar_3.png")
        self.enemy_health_bar3 = pygame.transform.scale(self.enemy_health_bar3, (self.enemy_health_bar1.get_width(), self.enemy_health_bar3.get_height()/3))
    def loadImageAsset(self, name):
        return pygame.image.load(f"assets\{name}")

class Player( GameObject ):
    def __init__(self, asset, x, y, health_bars):
        super().__init__(asset, x, y)
        self.max_health_bars = health_bars
        self.time = 0
        self.health_bars = health_bars
        self.bullets = 0
        self.move_dis = asset.get_width()/4

    def ResetStats(self):
        self.time = 0
        self.health_bars = self.max_health_bars
        self.bullets = 0


    def add_bullet(self):
        self.bullets += 1

    def add_time(self):
        self.time += 1

    def lose_life_bar(self):
        if self.health_bars > 0:
            self.health_bars -= 1

    def move_left(self):
        self.update(-self.move_dis)

    def move_right(self):
        self.update(self.move_dis)

    def get_score(self):
        if self.health_bars == 0 or self.bullets == 0 or self.time == 0:
            return 0
        return (100 * self.health_bars) - ((self.bullets *0.2) - (self.time*0.2))

    
class LevelBullets:
    def __init__(self, init_pos, asset, asset2, speed = 6):
        self.bullets              = []
        self.bullets_col          = []
        self.bullet_produse_delay = 6 #frames
        self.bulet_produse        = 0 #counter
        self.init_pos             = init_pos #(self.character.x + self.character.asset.get_width()/2, self.init_bullet_pos_y)
        self.asset                = asset
        self.asset2               = asset2 # on colition
        self.speed                = 10
        self.Sound                = GameSounds()
        self.controlColition      = colitionControl()
    
    def onReset(self):
        self.bullets = []
        self.bullets_col = []

    def addBullet(self, pos):
        if self.bulet_produse == self.bullet_produse_delay :
            self.bullets.append( Bullet(self.asset, pos[0], pos[1], self.speed, self.asset2) )
            self.bullets_col.append(0)
            self.bulet_produse = 0
    
    def popBullet(self):
        pop_bullet = False
        for i in range( len(self.bullets) ):
            bullet = self.bullets[i]
            if self.bullets_col[i] == 0 :
                bullet.move_forword()
            if bullet.y < 0 :
                pop_bullet = True
        if pop_bullet :
            self.bullets.pop(0)
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
                    self.controlColition.execute(self.Sound)
                    self.bullets[i].x -= (self.bullets[i].asset_colition.get_width()/2) + (self.bullets[i].asset.get_width()/2)
                    self.bullets[i].y -= (self.bullets[i].asset_colition.get_height())
                    return_val = True
        return return_val

    def onControl(self, event, pos):
        if event :
            self.addBullet(pos)
        if self.bulet_produse != self.bullet_produse_delay:
            self.bulet_produse += 1
        self.popBullet()
    def onDraw(self):
        for i in range( len(self.bullets )):
            bullet = self.bullets[i]
            win.screen.blit( bullet.get_asset( self.bullets_col[i] ), bullet.position() )

class EnemiesHealth:
    def __init__(self, assets, max_health = 4):
        self.table = assets[0]
        self.bar1  = assets[1]
        self.bar2  = assets[2]
        self.bar3  = assets[3]
        
        self.plus_pos = [ 
            [self.bar1, 0 ],
            [self.bar2, self.bar1.get_width() ],
            [self.bar2, self.bar1.get_width() + self.bar2.get_width() ],
            [self.bar3, self.bar1.get_width() + self.bar2.get_width() + self.bar3.get_width() ] 
            ]

        self.health = max_health

    def reduseHealth(self):
        self.health -= 1

    def onDraw(self, pos):
        # screen.blit( self.table, pos )
        for i in range(self.health) :
            win.screen.blit( self.plus_pos[i][0], ( pos[0] + 5 + self.plus_pos[i][1], pos[1] + 5 ) )

class LevelEnemies:
    def __init__(self, char_pos, enemy_assets, health_assets ):
        self.players_pos = char_pos
        self.enemy_assets = enemy_assets
        self.health_assets = health_assets
        self.enemes  = []
        self.dead_enemies = []
        self.droping_enemies = []
        self.dead_droping_enemies = []
    
        # self.createEnemy(enemy_assets[2], (char_pos[0], 140+self.enemy_assets[2].get_height()) )
        self.fillLevelWithEnemy()
        self.count1 = 0
        self.count2 = 0
        self.inArray1 = np.linspace(-(2 * np.pi), 2 * np.pi, 80)
        self.inArray2 = np.linspace(-(2 * np.pi), 2 * np.pi, 160)
        self.prev_dx = 0
        self.drop_v  = 24
        self.drop_g  = 1.1
    
    def fillLevelWithEnemy(self):
        pos_ref = (self.players_pos[0] - 250, 140+self.enemy_assets[2].get_height())
        dif = 50
        for i in range(4):
            self.createEnemy( self.enemy_assets[i] , (pos_ref[0] + i*160, dif + pos_ref[1]), EnemiesHealth(self.health_assets, 4)  )
            dif *= -1

    def createEnemy(self, asset, pos, health ):
        self.enemes.append( [GameObject(asset, pos[0], pos[1]), health] )

    def enemyHited( self, enemy ):
        enemy[1].health -= 1
    
    def cleanUpEnemies(self):
        dead_dr_enemies_new = []
        for enemy in self.dead_droping_enemies :
            if enemy[1].health <= -12 :
                continue
            dead_dr_enemies_new.append(enemy)
        self.dead_droping_enemies = dead_dr_enemies_new
        dead_enemies_new = []
        for enemy in self.dead_enemies :
            if enemy[1].health <= -6 :
                self.droping_enemies.append(enemy)
                continue
            dead_enemies_new.append(enemy)
        self.dead_enemies = dead_enemies_new

        drop_en = []
        for enemy in self.droping_enemies:
            if enemy[0].y > win.screen.get_height() + self.enemy_assets[0].get_height():
                print("clean")
                self.dead_droping_enemies.append(enemy)
                continue
            drop_en.append(enemy)
        self.droping_enemies = drop_en
        
        enemies_new = []
        for enemy in self.enemes :
            if enemy[1].health <= 0 :
                self.dead_enemies.append(enemy)
                continue
            enemies_new.append(enemy)
        self.enemes = enemies_new
    

    def moveEnemies(self, x, dx, secreen_width, char_pos):
        y_cos = math.cos(self.inArray1[self.count1])
        x_sin = math.sin(self.inArray2[self.count2])
        for enemy in self.enemes:
            enemy[0].update(2*x_sin,10*y_cos)
        nearest = -1
        min = 1e4 
        for i in range(len(self.enemes)):
            enemy = self.enemes[i]
            if abs(enemy[0].x - x) < min :
                min = abs(enemy[0].x - x)
                nearest = i
        
        w = 0
        r = random()
        if r > 0.5 :
            w = 0.5
        else :
            w = 0
            
        if nearest != -1 :
            if self.enemes[ nearest ][0].x + (w*dx/2) > 0 and self.enemes[ nearest ][0].x + (w*dx/2) < secreen_width - self.enemy_assets[0].get_width():
                self.enemes[nearest][0].update(w*dx/2, 0)
                self.prev_dx = w*dx
        
        for enemy in self.droping_enemies:
            du = dv(char_pos, enemy[0].position())
            du = normalize(du)
            enemy[0].update( du[0]*-10, du[1]*10+self.drop_v )

        for enemy in self.dead_droping_enemies:
            enemy[0].update( -1*w, self.drop_v )


    def onDraw( self ):
        self.count1 += 1
        self.count1 %= len(self.inArray1)
        self.count2 += 1
        self.count2 %= len(self.inArray2)
        for enemy in self.enemes :
            win.screen.blit( enemy[0].asset, enemy[0].position() )
            enemy[1].onDraw( [enemy[0].position()[0], enemy[0].position()[1] - 10] )
        for enemy in self.dead_enemies :
            enemy[1].health -= 1
            win.screen.blit( enemy[0].asset, enemy[0].position() )
        
        for enemy in self.droping_enemies:
            win.screen.blit( enemy[0].asset, enemy[0].position() )
        for enemy in self.dead_droping_enemies :
            enemy[1].health -= 1
            win.screen.blit( enemy[0].asset, enemy[0].position() )

