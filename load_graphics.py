#load graphics
from pygame import image as image
from pygame import Surface as surface

def load(screen):	
	tile = []

	for i in range(1, 7):
		raw_tile = image.load("block"+str(i)+".png")
		tile.append(raw_tile.convert(screen))

	return tile
