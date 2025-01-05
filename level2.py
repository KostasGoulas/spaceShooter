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

import level2_module as l2


class Level_2 :
    def __init__(self ):
        self.sounds = GameSounds()
        self.assets = l2.GameAssets(win.dim)
        char = self.assets.move_left # in this version left right and char is the same
        char_x  = (win.dim[0]/2) - char.get_width()/2
        char_y  = win.dim[1] - win.dim[1]/20 - char.get_height()
        self.move_dis = char.get_width()/4 

        # self.character = GameObject(char, char_x, char_y)
        self.character = l2.Player(char, char_x, char_y, 8)

        #bullets
        self.init_bullet_pos_y =  char_y-self.assets.bullet.get_height()
        self.Bullets = l2.LevelBullets( (self.character.x + self.character.asset.get_width()/2, self.init_bullet_pos_y), self.assets.bullet, self.assets.bullet_expl )

        #enemys
        self.Enemies = l2.LevelEnemies((char_x, char_y), self.assets.enemys, [self.assets.enemy_helth_table, self.assets.enemy_health_bar1, self.assets.enemy_health_bar2, self.assets.enemy_health_bar3])
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

        self.collide_explor = [ False, self.character.position ]
        self.ex_c = 0

        self.controlBullet   = l2.newBulletControl()
        self.controlColition = l2.colitionControl()

    def Reset(self):
        self.helthBars = [ GameObject(self.healthBar, self.FirstBarPos[0] + i*self.health_bar_width, self.FirstBarPos[1] ) for i in range(0,8) ]
        self.Bullets.onReset()
        self.Enemies.enemes.clear()
        self.Enemies.fillLevelWithEnemy()
        self.character.ResetStats()
        self.move_dis = self.character.asset.get_width()/4 

    def onControl(self):
        char = self.character
        dx   = 0
        if control_State.right and (char.x < (win.dim[0]-char.asset.get_width())):
            char.x += self.move_dis
            dx = self.move_dis
        
        if control_State.left and (char.x > 0):
            char.x -= self.move_dis
            dx = - self.move_dis

        self.Bullets.onControl(control_State.space, [char.x + char.asset.get_width()/2, char.y] )
        if control_State.space :
            self.controlBullet.execute(self.sounds)
            self.character.add_bullet()


        for enemy in self.Enemies.enemes:
            if self.Bullets.controlColitionPerEnemy(enemy[0]) :
                self.Enemies.enemyHited(enemy)
        
        if self.Bullets.controlColitionPerEnemy(self.HealthTableObject) :
            self.helthBars.pop()
            self.move_dis *= 0.8
        
        for enemy in self.Enemies.droping_enemies:
            if enemy[0].collition(self.character) :
                self.helthBars.pop()
                if( len(self.helthBars) != 0 ):
                    self.helthBars.pop()
                self.move_dis *= 0.8
                enemy = self.Enemies.droping_enemies.pop()
                self.Enemies.dead_droping_enemies.append(enemy)
                self.collide_explor = [ True, (self.character.position()[0] , self.character.position()[1]) ]

        self.Enemies.cleanUpEnemies()
        
        if len(self.Enemies.enemes) == 0 and len(self.Enemies.dead_enemies) == 0:
            print( self.character.get_score() )
            game_State.set_end_game()
            
        # self.helthBars.pop()
        self.Enemies.moveEnemies(self.character.x, -1*dx, win.dim[0], self.character.position())
        
        if len( self.helthBars ) == 0 :
            game_State.set_end_game()

    def onEvent(self):
        self.character.add_time()

    def onDraw(self):
        win.screen.blit( self.assets.background,(0,0) )
        win.screen.blit( self.character.asset, self.character.position() )

        self.Enemies.onDraw()
        win.screen.blit(self.healthTable, self.helthPos)
        for bar in self.helthBars : 
            win.screen.blit( bar.asset, bar.position())
        self.Bullets.onDraw()
        if self.collide_explor[0] and self.ex_c < 8 :
            if self.ex_c % 2 :
                win.screen.blit( self.assets.bullet_expl, (self.collide_explor[1][0]-2, self.collide_explor[1][1] ) )
            else :
                win.screen.blit( self.assets.bullet_expl, (self.collide_explor[1][0]+2, self.collide_explor[1][1] ) )
            self.ex_c += 1
            self.controlColition.execute(self.sounds)

        elif self.collide_explor[0] and self.ex_c >= 8 :
            self.collide_explor[0] = False
            self.ex_c = 0
