#load graphics
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
