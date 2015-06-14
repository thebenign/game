
import sys, pygame, math, random
from pygame.locals import *
from pygame import font
import load_graphics
import json
from pprint import pprint as pprint

WINDOW_W = 1280
WINDOW_H = 720

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Cray Game")

timer = pygame.time.Clock()
TIME = 1000/60

FPS_TIMER = USEREVENT + 1
pygame.time.set_timer(FPS_TIMER, 1000)

tile = load_graphics.load(screen)

fontlocation = pygame.font.match_font('TimesNewRoman')
main_font = font.SysFont(fontlocation,32,False,False)

mob_img = load_graphics.load_mobs(screen, "")

class Mob():
    """ 
        This class is the base for all "mobile" entities in the game.

        Initializes with the standard cartesian coords and
        a sprite.

    """

    def __init__(self):
        self.x, self.y = random.random()*800, random.random()*600
        self.dx, self.dy = 0, 0 # Delta x and y. this is the character's movement over time.
        self.friction = .2

    def doFriction(self):
        try:
            dx_norm = self.dx / abs(self.dx)
        except ZeroDivisionError:
            dx_norm = 0
        try:
            dy_norm = self.dy / abs(self.dy)
        except:
            dy_norm = 0


        if self.dx != 0:
            self.dx = self.dx - dx_norm * self.friction
        if self.dy != 0:
            self.dy = self.dy - dy_norm * self.friction



class Hero(Mob):

    def __init__(self, sprite, x = 0, y = 0):
        Mob.__init__(self)
        self.x = x or self.x
        self.y = y or self.y
        self.img = sprite


class Camera():
    """
        This class represents your view of the world. Takes an animate game object and follows it around,
        showing only what's within the camera's view port.

    """

    def __init__(self, mob = None):
        """
            Arguments:
                mob: a "mobile" object with coordinates that can be followed.

        """
        self.target = mob
        self.x = 0
        self.y = 0
        self.r = 0      # angle in radians
        self.s = 0      # speed in pixels per step

        self.scale = 1
    
    def follow(self, mob):
        """ Change the mob """
        self.target = mob

    def update(self):

        speed = math.hypot(self.x - self.target.x, self.y - self.target.y)
        angle = math.atan2(self.x - self.target.x, self.y - self.target.y)

        #self.x = self.x + math.cos(angle)*speed
        #self.y = self.y + math.sin(angle)*speed

        self.x = self.target.x - WINDOW_W / 2
        self.y = self.target.y - WINDOW_H / 2

        if self.x < 0 :
            self.x = 0
        if self.y < 0:
            self.y = 0

    def start(self):
        self.move = True

    def stop(self):
        self.move = False


class GameRunner():
    """
        A class to run the majority of top level game logic, i.e.
        graphics updating, keyboard handling, etc.

        Additionally, most of the other classes/objects will be instantiated
        as a child of GameRunner, hopefully to the effect of succint reference passing.
        I'll figure that part out eventually.

    """
    def __init__(self):

        self.obj = []
        self.obj.append(Hero(mob_img["candle1"], 128, 128))

        camera.follow(self.obj[0])

        self.size = width, height = 800, 600
        self.black = 0, 0, 0
        self.clock = pygame.time.Clock()
        
        self.text = main_font.render("Hello World",0,(255,255,255))

        self.time = 0
        self.dt = 0

        self.blend = 0
        self.maps = []
        

    def handleKeys(self,obj):
        """
            This moves the things. Arrow keys move the objects around.
            Enter/Return: stop motion of all objects


            Uses pygame's key handling function to directly increment
            the delta coordinates of obj

            Parameters:
                obj: an object which has cartesian coordinates

        """
        key = pygame.key.get_pressed()
        if key[K_DOWN]:
            obj.dy = obj.dy + .5
        if key[K_UP]:
            obj.dy = obj.dy - .5
        if key[K_LEFT]:
            obj.dx = obj.dx - .5
        if key[K_RIGHT]:
            obj.dx = obj.dx + .5
        if key[K_RETURN]:
            obj.dx, obj.dy = 0, 0

    def handleGameKeys(self):
        """
            Handles window and top level keyboard events.

            
            Space: add objects

            Backspace: destroy objects

            Escape: quit the program

        """
        key = pygame.key.get_pressed()
        if key[K_SPACE]:
            self.obj.append(Hero(mob_img["candle"]))
        if key[K_BACKSPACE]:
            if len(self.obj) > 0:
                _ = self.obj.pop()

        if key[K_ESCAPE]:
            exit()

    def update(self):
        """
            This is the main game loop.

            Nearly all physics, logic, and control is handled here.
            As well as the timestep code which keeps the game physics and logic
            running at a fixed rate.

            This function is called once per game step, as frequently as possible.

        """
        #pygame.event.pump()
        self.dt = self.dt + self.clock.tick() # increment the delta time by the time (in milliseconds) since the last game step
        
        
        if self.dt > TIME:               # if the delta time is greater than a predetermined TIME (1/60 sec)
            self.dt = self.dt - TIME     # decrement the dt by TIME, leaving the rollover time. This ensures a smooth timestep.
                                         # and continue with a step of game logic
            for obj in self.obj:

                self.handleKeys(obj)
                obj.x = obj.x + obj.dx
                obj.y = obj.y + obj.dy
                obj.doFriction()

                '''
                if obj.x > 800:         # Super stupid screen wrapping.
                    obj.x = -32
                if obj.x < -32:
                    obj.x = 800
                if obj.y > 600:
                    obj.y = -32
                if obj.y < -32:
                    obj.y = 600
                '''

            camera.update()


            self.text = main_font.render(str(len(self.obj)),0,(255,255,255))
            self.handleGameKeys()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == USEREVENT+1:
                    pygame.display.set_caption("FPS: "+str(math.floor(self.clock.get_fps())))
                    print(camera.x, camera.y)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_t:
                        self.blend = (self.blend + 1)%2

    def display(self):
        """
            This blits visible objects to the Surface,
            then flips the Surface to the window, making
            a complete frame draw.

        """
        cam_x = camera.x
        cam_y = camera.y

        screen.fill(self.black)

        for obj in self.obj:
            screen.blit(obj.img, (obj.x-(obj.x%1) - cam_x, obj.y-(obj.y%1) - cam_y), special_flags = self.blend)

        screen.blit(self.text,(0,0))
        pygame.display.flip()
        
    def LoadMap(self):
        x = ['''list of files''']
        
        for m in x:
            self.maps.append(Map.LoadJSON(m))
            

class Map():
    def __init__(self, map_data={}, layer_data=[], tile_data=[]):
        self.map_data = map_data
        self.layer_data = layer_data
        self.tile_data = tile_data
        
    @classmethod
    def LoadJSON(cls, file_name):
        map_data, layer_data, tile_data = {},{},{}

        map_dict = json.load(open(file_name))

        for key, val in map_dict.items():
            if key == "layers":
                layer_data[key] = val
            elif key == "tilesets":
                tile_data[key] = val
                load_graphics.load_tiles(tile_data)
            else:
                map_data[key] = val

        return cls(map_data, layer_data, tile_data)


map1 = Map.LoadJSON("map/map.json")
camera = Camera()
game = GameRunner()

while 1:
    game.update()
    game.display()
