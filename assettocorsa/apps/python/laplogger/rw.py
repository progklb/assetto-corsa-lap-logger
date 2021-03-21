import os
import json

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

logFile = None


# -----------------------------------------
# Logging
# -----------------------------------------

def openLog(log):
	'''Opens the car/track log file. If no file exists, one will be created.'''
	
	LOG_NAME = log.getFileName()

	if not os.path.exists(LOG_DIR):
		os.mkdir(LOG_DIR)

	shouldInit = not os.path.exists("{}/{}".format(LOG_DIR, LOG_NAME))
		
	global logFile
	logFile = open("{}/{}".format(LOG_DIR, LOG_NAME), "a+")

	if shouldInit:
		initLog(log)


def initLog(log):
	'''Initialises the log file with important information for this log.'''

	jsonDump = json.dumps(log, sort_keys=True, indent=4, default=lambda x: x.__dict__)
	logFile.write(jsonDump)


def writeLogEntry(lapData):
	'''Writes a new log entry to the log using the current state information.'''
	global logFile
	logFile.write("{}\n".format(lapData))


def closeLog():
	global logFile
	logFile.close()