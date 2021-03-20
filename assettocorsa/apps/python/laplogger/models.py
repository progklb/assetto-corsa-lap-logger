class Vehicle:
	"""Represents a vehicle"""
	
	def __init__(self, name):
		self.name = name

class Track:
	"""Represents a track"""

	def __init__(self, name, layout):
		self.name = name
		self.layout = layout

class Lap:
	"""Represents a single lap around a track"""

	def __init__(self):
		self.time = 0
		self.splits = []
		self.invalidated = False

	# time = 0
	# splits = []
	# invalidated = False

class Session:
	"""Represents a single track session, consisting of multiple laps."""

	startTime = ""
	endTime = ""
	laps = []



class Log:

	def __init__(self):
		self.vehicle = {}
		self.track = {}
		self.session = []