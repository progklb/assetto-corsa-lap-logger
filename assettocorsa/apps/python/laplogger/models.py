class Vehicle(object):
	'''Represents a vehicle'''
	
	def __init__(self, name):
		self.name = name

class Track(object):
	''''Represents a track'''

	def __init__(self, name, layout):
		self.name = name
		self.layout = layout

class Lap(object):
	'''Represents a single lap around a track'''

	def __init__(self):
		self.lapNo = 0
		self.time = 0
		self.splits = []
		self.invalidated = False

		# TODO Add a vehicle configuration object

class Session(object):
	'''Represents a single track session, consisting of multiple laps.'''

	def __init__(self, startTime):
		self.startTime = startTime
		self.endTime = None
		self.laps = []

	def addLap(self, lap):
		self.laps.append(lap)

class Log(object):
	'''Represents a full log for a vehicle-track combination, and can consist of multiple game sessions.'''

	def __init__(self, vehicle, track):
		self.vehicle = vehicle
		self.track = track
		self.sessions = []

	def getFileName(self):
		'''Genereates and returns a file name based on the current data. Requires that track and vehicle are set.'''
		return "{}-{}-{}.acl".format(self.vehicle.name, self.track.name, self.track.layout or "default")

	def addSession(self, session):
		'''Adds a session to this log instance. Session should be fully assigned before adding.'''
		self.sessions.append(session)