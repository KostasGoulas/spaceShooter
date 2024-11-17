from gameWindow import *

def is_point_inside_box( point, box_point, box_width, box_heigth ):
    return (point[0] >= box_point[0] and point[0] <= box_point[0]+box_width) and (point[1] >= box_point[1] and point[1] <= box_point[1]+box_heigth)

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
        self.update(0,-self.speed)


        

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
        self.enemys  = []
        self.init_bullet_pos_y =  self.character.y - char.get_height()

    def onControl(self):
        char = self.character
        if self.right_pressed and (char.x < (self.size[0]-char.asset.get_width())):
            char.x += self.move_dis
        
        if self.left_pressed and (char.x > 0):
            char.x -= self.move_dis

        if self.space_pressed :
            self.bullets.append( Bullet(self.assets.bullet, self.character.x + self.character.asset.get_width()/2, self.init_bullet_pos_y, 2 ) )
        
        for bullet in self.bullets:
            bullet.move_forword()
        
        pop_bullet = False
        for bullet in self.bullets:
            if bullet.y < 0:
                pop_bullet = True
        if pop_bullet :
            self.bullets.pop(0)
            print("delete buulet")
                

        
    
    def onDraw(self):
        super().onDraw()
        self.screen.blit( self.assets.background,(0,0) )
        self.screen.blit( self.character.asset, (self.character.x, self.character.y))
        for bullet in self.bullets:
            self.screen.blit( bullet.asset, bullet.position() )