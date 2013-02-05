
import itertools
import sys

ESC = chr(0x1B)
RESET = "0"

COLOURS_NAMED = dict(list(zip(
		['black', 'red', 'green', 'yellow', 'blue', 'magneta', 'cyan', 'white'],
		[str(x) for x in range(30, 38)]
		)))

COLOURS_MID = [
	colours for name, colours in list(COLOURS_NAMED.items())
	if name not in ('black', 'white')
]

class AnsiColourException(Exception):
	pass

class ColourMap(object):
	def __init__(self, colours=COLOURS_MID):
		self.map = {};
		self._colourIter = itertools.cycle(colors)

	def colourFor(self, string):
		if string not in self._cmap:
			self._cmap[string] = next(self._colourIter)
		return self._cmap[string]

class AnsiCmd(object):
	def __init__(self, forceAnsi):
		self.forceAnsi = forceAnsi

	def cmdReset(self):
		if sys.stdout.isatty() or self.forceAnsi:
			return ESC + "[0m"
		else:
			return ""

	def cmdColour(self, colour):
		if sys.stdout.isatty() or self.forceAnsi:
			return ESC + "[" + colour + "m"
		else:
			return ""

	def cmdColourNamed(self, colour):
		try:
			return self.cmdColour(COLOURS_NAMED[colours])
		except KeyError:
			raise AnsiColourException('Unknown colour %s' %(colour))

	def cmdBold(self):
		if sys.stdout.isatty() or self.forceAnsi:
			return ESC + "[1m"
		else:
			return ""

	def cmdUnderline(self):
		if sys.stdout.isatty() or self.forceAnsi:
			return ESC + "[4m"
		else:
			return ""

def cmdReset():
	return AnsiCmd(False).cmdReset()

def cmdColour(colour):
	return AnsiCmd(False).cmdColour(colour)

def cmdColourNamed(colour):
	return AnsiCmd(False).cmdColourNamed(colour)

