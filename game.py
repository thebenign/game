
import sys, pygame, math, random
from pygame.locals import *
from pygame import font
import load_graphics

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Cray Game")

timer = pygame.time.Clock()
TIME = 1000/60

FPS_TIMER = USEREVENT + 1
pygame.time.set_timer(FPS_TIMER, 1000)

tile = load_graphics.load(screen)

fontlocation = pygame.font.match_font('TimesNewRoman')
main_font = font.SysFont(fontlocation,32,False,False)


class Hero():
	""" 
		A class to act as the playable character.

		Initializes with the standard cartesian coords and
		a sprite.

	"""

	def __init__(self):
		self.x, self.y = random.random()*800, random.random()*600
		self.dx, self.dy = 0, 0 # Delta x and y. this is the character's movement over time.
		self.img = tile[math.ceil(random.random()*5)]


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

		self.size = width, height = 800, 600
		self.black = 0, 0, 0
		self.clock = pygame.time.Clock()
		
		self.text = main_font.render("Hello World",0,(255,255,255))

		self.time = 0
		self.dt = 0

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
			self.obj.append(Hero())
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

				if obj.x > 800:			# Super stupid screen wrapping.
					obj.x = -32
				if obj.x < -32:
					obj.x = 800
				if obj.y > 600:
					obj.y = -32
				if obj.y < -32:
					obj.y = 600
			
			self.text = main_font.render(str(len(self.obj)),0,(255,255,255))
			self.handleGameKeys()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == USEREVENT+1:
					pygame.display.set_caption("FPS: "+str(math.floor(self.clock.get_fps())))

	def display(self):
		"""
			This blits visible objects to the Surface,
			then flips the Surface to the window, making
			a complete frame draw.

		"""
		screen.fill(self.black)

		for obj in self.obj:
			screen.blit(obj.img, (math.floor(obj.x), math.floor(obj.y)))

		screen.blit(self.text,(0,0))
		pygame.display.flip()


game = GameRunner()

while 1:
	#game.handleKeys(guy)
	game.update()
	game.display()