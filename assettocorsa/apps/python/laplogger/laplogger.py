import sys
import ac
import acsys

import os

# -----------------------------------------
# Constants
# -----------------------------------------

# The name of the custom HUD window displayed when this app is active.
APP_NAME = "Lap Logger"
# Because the script is run from the context of the main .exe we need to point to provide a relative path to this script.
LOG_DIR = "apps/python/laplogger/logs"


# -----------------------------------------
# Variables
# -----------------------------------------

active = False

appWindow = None
logFile = None

lblLapCount = None
lblBestLap = None
lblLastLap = None
lblCurrentTime = None

lapCount = 0
bestLap = 0
lastLap = 0

lastLapInvalidated = False

# -----------------------------------------
# Asseto Corsa Events
# -----------------------------------------

def acMain(ac_version):

	log("Starting {}".format(APP_NAME))

	global appWindow
	appWindow = ac.newApp(APP_NAME)
	ac.setSize(appWindow, 400, 200)

	# TODO Get this working
	#ac.addOnAppActivatedListener(appWindow, onAppActivated)
	#ac.addOnAppDismissedListener(appWindow, onAppDismissed)

	global lblLapCount
	lblLapCount = ac.addLabel(appWindow, "")
	ac.setPosition(lblLapCount, 3, 30)

	global lblBestLap
	lblBestLap = ac.addLabel(appWindow, "")
	ac.setPosition(lblBestLap, 3, 60)

	global lblLastLap
	lblLastLap = ac.addLabel(appWindow, "")
	ac.setPosition(lblLastLap, 3, 90)

	global lblCurrentTime
	lblCurrentTime = ac.addLabel(appWindow, "")
	ac.setPosition(lblCurrentTime, 3, 120)

	openLog()

	return APP_NAME


def acUpdate(deltaT):
	
	# if (not active):
		# return
	
	updateState()
	refreshUI()

def acShutdown():
	# TODO Save lap logs
	closeLog()


# -----------------------------------------
# Helper Functions
# -----------------------------------------

def log(message, level = "INFO"):
	'''Logs a message to the py_log with the (optional) specified level tag.'''
	ac.log("laplogger [{}]: {}".format(level, message))

def getFormattedLapTime(lapTime):
	'''Returns a lap time string formatted for display.'''

	if (not lapTime > 0):
		return "--:--:--"

	minutes = int(lapTime/1000/60)
	seconds = int((lapTime/1000)%60)
	millis = lapTime - (int((lapTime/1000))*1000)

	return "{}:{:02d}:{:03d}".format(minutes, seconds, millis)

def updateState():
	'''Updates the state of all variables required for logging.'''

	global lastLapInvalidated

	# Not working
	if ac.getCarState(0, acsys.CS.LapInvalidated) != 0:
		lastLapInvalidated = True

	global lapCount
	currentLap = ac.getCarState(0, acsys.CS.LapCount)
	if (lapCount < currentLap):
		lapCount = currentLap
		writeLogEntry()

		lastLapInvalidated = False


def refreshUI():
	'''Updates the state of the UI to reflect the latest data.'''

	global lblLapCount, lapCount
	ac.setText(lblLapCount, "Laps: {}".format(lapCount))

	global lblBestLap, bestLap
	bestLap = ac.getCarState(0, acsys.CS.BestLap)
	ac.setText(lblBestLap, "Best: {}".format(getFormattedLapTime(bestLap)))

	global lblLastLap, lastLap
	lastLap = ac.getCarState(0, acsys.CS.LastLap)
	ac.setText(lblLastLap, "Last: {}".format(getFormattedLapTime(lastLap)))

	global lblCurrentTime
	ac.setText(lblCurrentTime, "Time: {}".format(getFormattedLapTime(ac.getCarState(0, acsys.CS.LapTime))))

	# TODO
	# Personal best
	# Graph


# -----------------------------------------
# Logging
# -----------------------------------------

def openLog():
	
	# Create a log name based on the curent vehicle-track combination
	LOG_NAME = "{}-{}-{}.acl".format(ac.getCarName(0), ac.getTrackName(0), ac.getTrackConfiguration(0))

	# TODO If no track configration is available, write "default"
	# TODO Condider creating a spacer between log entries from different sessions.

	if not os.path.exists(LOG_DIR):
		os.mkdir(LOG_DIR)

	shouldInit = not os.path.exists("{}/{}".format(LOG_DIR, LOG_NAME))
		
	global logFile
	logFile = open("{}/{}".format(LOG_DIR, LOG_NAME), "a+")

	if shouldInit:
		initLog()

def initLog():
	'''Initialises the log file with important information regarding this log.'''
	carNameLine =		"car: {}".format(ac.getCarName(0))
	trackNameLine =		"track: {}".format(ac.getTrackName(0))
	trackConfigLine =	"config: {}".format(ac.getTrackConfiguration(0))

	logFile.write("{}\n{}\n{}\n\n".format(carNameLine, trackNameLine, trackConfigLine))

def writeLogEntry():
	'''Writes a new log entry to the log using the current state information.'''
	global logFile

	lapData = {
		"lap" : lapCount,
		"time" : ac.getCarState(0, acsys.CS.LastLap),
		"invalidated" : lastLapInvalidated,
		"splits" : ac.getLastSplits(0)
	}

	logFile.write("{}\n".format(lapData))

def closeLog():
	global logFile
	logFile.close()

# -----------------------------------------
# Event Handlers
# -----------------------------------------

def onAppDismissed():
	ac.console("LapLogger Dismissed")
	active = False
	log("Dismissed")

def onAppActivated():
	ac.console("LapLogger Activated")
	active = True
	log("Activated")
