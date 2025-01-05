
class controlState:
    def __init__(self) :
        self.right      = False
        self.left       = False
        self.space      = False
        self.mouse_down = False
        self.mouse_pos  = (0,0)
    def reset(self):
        self.right = False
        self.left  = False
        self.space = False
        self.mouse_down = False

    def set_right(self):
        self.right = True
    def set_left(self):
        self.left = True
    def set_space(self):
        self.space = True

class gameSate:
    def __init__(self) :
        self.start_screen = True
        self.level_1      = False
        self.level_2      = False
        self.end_game     = False
        self.exit         = False
    
    def set_start_game(self):
        self.start_screen = False
        self.level_1      = True
        self.level_2      = False
        self.end_game     = False
        self.exit         = False
    
    def set_level2(self):
        self.start_screen = False
        self.level_1      = False
        self.level_2      = True
        self.end_game     = False
        self.exit         = False


    def set_end_game(self):
        self.start_screen = False
        self.level_1      = False
        self.level_2      = False
        self.end_game     = True
        self.exit         = False

    def set_exit(self):
        self.start_screen = False
        self.level_1      = False
        self.level_2      = False
        self.end_game     = False
        self.exit         = True
    
    def set_start(self):
        print( "START" )
        self.start_screen = True
        self.level_1      = False
        self.level_2      = False
        self.end_game     = False
        self.exit         = False