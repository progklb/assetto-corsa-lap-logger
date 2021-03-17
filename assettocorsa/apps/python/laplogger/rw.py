import os

# -----------------------------------------
# Constants
# -----------------------------------------

# Because the script is run from the context of the main .exe we need to point to provide a relative path to this script.
LOG_DIR = "apps/python/laplogger/logs"


# -----------------------------------------
# Variables
# -----------------------------------------

logFile = None


# -----------------------------------------
# Logging
# -----------------------------------------

def openLog(carNameLine, trackNameLine, trackConfigLine):
	'''Opens the car/track log file. If no file exists, one will be created.'''
	
	# Create a log name based on the curent vehicle-track combination
	LOG_NAME = "{}-{}-{}.acl".format(carNameLine, trackNameLine, trackConfigLine or "default")

	# TODO If no track configration is available, write "default"
	# TODO Condider creating a spacer between log entries from different sessions.

	if not os.path.exists(LOG_DIR):
		os.mkdir(LOG_DIR)

	shouldInit = not os.path.exists("{}/{}".format(LOG_DIR, LOG_NAME))
		
	global logFile
	logFile = open("{}/{}".format(LOG_DIR, LOG_NAME), "a+")

	if shouldInit:
		initLog(carNameLine, trackNameLine, trackConfigLine or "default")


# TODO This should accept a Car and Track object.
def initLog(carNameLine, trackNameLine, trackConfigLine):
	'''Initialises the log file with important information regarding this log.'''
	logFile.write("car: {}\ntrack: {}\nlayout: {}\n\n".format(carNameLine, trackNameLine, trackConfigLine))


def writeLogEntry(lapData):
	'''Writes a new log entry to the log using the current state information.'''
	global logFile
	logFile.write("{}\n".format(lapData))


def closeLog():
	global logFile
	logFile.close()