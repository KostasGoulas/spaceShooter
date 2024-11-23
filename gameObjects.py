import pygame
from algos import *

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
