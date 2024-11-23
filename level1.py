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
        return 1000 * self.health_bars / ((self.bullets *0.8) + (self.time*0.2))

    
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
                continue;
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
    def onDraw(self, screen):
        for i in range( len(self.bullets )):
            bullet = self.bullets[i]
            screen.blit( bullet.get_asset( self.bullets_col[i] ), bullet.position() )

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

    def onDraw(self, screen, pos):
        # screen.blit( self.table, pos )
        for i in range(self.health) :
            screen.blit( self.plus_pos[i][0], ( pos[0] + 5 + self.plus_pos[i][1], pos[1] + 5 ) )

class LevelEnemies:
    def __init__(self, char_pos, enemy_assets, health_assets):
        self.players_pos = char_pos
        self.enemy_assets = enemy_assets
        self.health_assets = health_assets
        self.enemes  = []
        self.dead_enemies = []
        # self.createEnemy(enemy_assets[2], (char_pos[0], 140+self.enemy_assets[2].get_height()) )
        self.fillLevelWithEnemy()
    
    def fillLevelWithEnemy(self):
        pos_ref = (self.players_pos[0] - 150, 140+self.enemy_assets[2].get_height())
        for i in range(4):
            self.createEnemy( self.enemy_assets[i] , (pos_ref[0] + i*100, pos_ref[1]), EnemiesHealth(self.health_assets, 4) )

    def createEnemy(self, asset, pos, health ):
        self.enemes.append( [GameObject(asset, pos[0], pos[1]), health] )

    def enemyHited( self, enemy ):
        enemy[1].health -= 1
    
    def cleanUpEnemies(self):
        dead_enemies_new = []
        for enemy in self.dead_enemies :
            if enemy[1].health <= -6 :
                continue;
            dead_enemies_new.append(enemy)
        
        self.dead_enemies = dead_enemies_new
        
        enemies_new = []
        for enemy in self.enemes :
            if enemy[1].health <= 0 :
                self.dead_enemies.append(enemy)
                continue;
            enemies_new.append(enemy)
        self.enemes = enemies_new

    def onDraw( self, screen ):
        for enemy in self.enemes :
            screen.blit( enemy[0].asset, enemy[0].position() )
            enemy[1].onDraw(screen, [enemy[0].position()[0], enemy[0].position()[1] - 10] )
        for enemy in self.dead_enemies :
            enemy[1].health -= 1
            screen.blit( enemy[0].asset, enemy[0].position() )


class Level_1 :
    def __init__(self, screen, dim, clock, title, state, control ):
        self.assets  = GameAssets(dim)
        self.size = dim
        char = self.assets.move_left # in this version left right and char is the same
        char_x  = (dim[0]/2) - char.get_width()/2
        char_y  = dim[1] - dim[1]/20 - char.get_height()
        self.move_dis = char.get_width()/4 

        # self.character = GameObject(char, char_x, char_y)
        self.character = Player(char, char_x, char_y, 8)

        #bullets
        self.init_bullet_pos_y =  char_y-self.assets.bullet.get_height()
        self.Bullets = LevelBullets( (self.character.x + self.character.asset.get_width()/2, self.init_bullet_pos_y), self.assets.bullet, self.assets.bullet_expl )

        #enemys
        self.Enemies = LevelEnemies((char_x, char_y), self.assets.enemys, [self.assets.enemy_helth_table, self.assets.enemy_health_bar1, self.assets.enemy_health_bar2, self.assets.enemy_health_bar3])
        # self.enemes  = [ GameObject(self.assets.enemys[2], char_x, 140+self.assets.enemys[2].get_height()) ]

        # HEALTH:
        self.helthPos = (15,15)
        self.FirstBarPos = (15+3, 15+3)
        self.healthTable = self.assets.healthTable
        self.HealthTableObject = GameObject( self.healthTable, self.helthPos[0], self.helthPos[1] )
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
        self.Enemies.enemes.clear()
        self.Enemies.fillLevelWithEnemy()
        self.character.ResetStats()

    def onControl(self):
        char = self.character
        if self.controlState.right and (char.x < (self.size[0]-char.asset.get_width())):
            char.x += self.move_dis
        
        if self.controlState.left and (char.x > 0):
            char.x -= self.move_dis

        self.Bullets.onControl(self.controlState.space, [char.x + char.asset.get_width()/2, char.y] )
        if self.controlState.space :
            self.character.add_bullet()


        for enemy in self.Enemies.enemes:
            if self.Bullets.controlColitionPerEnemy(enemy[0]) :
                self.Enemies.enemyHited(enemy)
        
        if self.Bullets.controlColitionPerEnemy(self.HealthTableObject) :
            self.helthBars.pop()
                
        self.Enemies.cleanUpEnemies()
        
        if len(self.Enemies.enemes) == 0 and len(self.Enemies.dead_enemies) == 0:
            print( self.character.get_score() )
            self.gameState.set_end_game()
            
        # self.helthBars.pop()
        
        if len( self.helthBars ) == 0 :
            self.gameState.set_end_game()

    def onEvent(self):
        self.character.add_time()
        return self.gameState, self.controlState;

    def onDraw(self):
        self.screen.blit( self.assets.background,(0,0) )
        self.screen.blit( self.character.asset, self.character.position() )

        self.Enemies.onDraw(self.screen)
        self.screen.blit(self.healthTable, self.helthPos)
        for bar in self.helthBars : 
            self.screen.blit( bar.asset, bar.position())
        self.Bullets.onDraw(self.screen)
