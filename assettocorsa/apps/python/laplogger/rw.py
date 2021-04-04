import os
import json

import ac

from logger import acLog
from models import Vehicle
from models import Track
from models import Lap
from models import Session
from models import Log

# -----------------------------------------
# Constants
# -----------------------------------------

# Because the script is run from the context of the main .exe we need to provide a relative path to this script.
LOG_DIR = "apps/python/laplogger/logs"


# -----------------------------------------
# Variables
# -----------------------------------------

# The name of the file that we are writing to for the current session.
logFilename = None


# -----------------------------------------
# Logging
# -----------------------------------------

def setLog(log):
	'''Opens the car/track log file. If no file exists, one will be created.'''
	
	global logFilename
	logFilename = log.getFileName()

	if not os.path.exists(LOG_DIR):
		os.mkdir(LOG_DIR)

	shouldInit = not os.path.exists(getLogPath())
		
	if shouldInit:
		initLog(log)


def initLog(log):
	'''Initialises the log file with important information for this log.'''

	with open(getLogPath(), 'a+') as f:
		jsonDump = dump(log)
		f.write(jsonDump)


def writeLap(lapData):
	'''Writes a new log entry to the log using the current state information.'''

	#TODO Write a single lap entry. Include laps details and config.

	#with open(getLogPath(), 'a+') as f:
	#	f.write("{}\n".format(lapData))


def writeSession(sessionData):
	'''Writes the provided session to the current log file.'''

	# TODO Write session header. Include start time and config.

	#with open(getLogPath(), 'a+') as f:
	#	jsonDump = dump(sessionData)
	#	f.write(jsonDump)

	
def getLogPath():
	'''Returns the full log file path.'''
	global LOG_DIR
	global logFilename
	return "{}/{}".format(LOG_DIR, logFilename)


def dump(obj, sort=True):
	'''Converts the provided string to a JSON string representation'''
	return json.dumps(obj, sort_keys=sort, indent=4, default=lambda x: x.__dict__)