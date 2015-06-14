#load graphics
import os, inspect
from pygame import image as image
from pygame import Surface as surface

def load(screen):
	"""
		Loads the graphics for the game into a list,
		then converts the graphics from png to something more
		appropriate for blitting.

		Perameters:
			screen: a pygame Surface object for Surface.convert to use

		Returns:
			list

	"""
	tile = []

	for i in range(1, 7):
		raw_tile = image.load("block"+str(i)+".png")
		tile.append(raw_tile.convert(screen))

	return tile

def load_mobs(screen, dir):
	path = os.path.dirname(os.path.abspath(__file__))+"/graphics"
	files = os.listdir(path)
	mob_graphics = {}
	print (files)

	for f in files:
		asset = image.load("graphics/"+f).convert_alpha(screen)
		name, _ = os.path.splitext(f)
		mob_graphics[name] = asset

	return mob_graphics

def load_tiles(tiles_dict):
	"""
		Loads tiles from the tiles dictionary extracted from
		a map JSON.
	"""
	tile = []

	#for 
	return tile