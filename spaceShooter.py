from gameWindow import *

def is_point_inside_box( point, box_point, box_width, box_heigth ):
    return (point[0] >= box_point[0] and point[0] <= box_point[0]+box_width) and (point[1] >= box_point[1] and point[1] <= box_point[1]+box_heigth)

class GameAssets :
    def __init__(self):
        self.simple_char = self.loadImageAsset("Missile_03.png");
        self.move_right  = self.loadImageAsset("Missile_03.png");
        self.move_left   = self.loadImageAsset("Missile_03.png")
        self.background  = self.loadImageAsset("small-bubbles-foam.jpg")
        self.bullet      = self.loadImageAsset("Rocket_Effect_01.png")
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
        p3 = [obj.x+obj.asset.get_width(), obj.y+obj.asset.get_height()]
        p4 = [obj.x                      , obj.y+obj.asset.get_height()]
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
    def __init__(self, asset, x, y, speed):
        super().__init__(asset, x, y)
        self.speed = speed
    def move_forword( self ):
        self.update(0,self.speed)


        

class SpaceShooter(Game):
    def __init__(self, dim, title):
        super().__init__(dim, title)
        self.assets  = GameAssets()
        self.char = self.assets.move_left # in this version left right and char is the same
        self.char = pygame.transform.scale(self.char, ( self.char.get_width()/4, self.char.get_height()/4) )
        self.assets.background = pygame.transform.scale( self.assets.background, self.size ) # this is to fit the background to the window 
        self.char_x  = (self.size[0]/2) - self.char.get_width()/2
        self.char_y  = self.size[1] - self.size[1]/20 - self.char.get_height()
        self.move_dis = self.char.get_width()/4 
        print( self.assets.move_left )

    def onControl(self):
        if self.right_pressed and (self.char_x < (self.size[0]-self.char.get_width())):
            self.char_x += self.move_dis
        
        if self.left_pressed and (self.char_x > 0):
            self.char_x -= self.move_dis
        
    
    def onDraw(self):
        super().onDraw()
        self.screen.blit( self.assets.background,(0,0) )
        self.screen.blit( self.char, (self.char_x, self.char_y))