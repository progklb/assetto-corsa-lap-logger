import ac
import acsys
import sys

import os

import rw

# -----------------------------------------
# Constants
# -----------------------------------------

# The name of the custom HUD window displayed when this app is active.
APP_NAME = "Lap Logger"


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
	updateState()
	refreshUI()

def acShutdown():
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

	# TODO Update UI according to latest mockups.


# -----------------------------------------
# Logging
# -----------------------------------------

def openLog():
	'''Opens a log file for the current session.'''
	rw.openLog(ac.getCarName(0), ac.getTrackName(0), ac.getTrackConfiguration(0))

def writeLogEntry():
	'''Writes a new log entry to the log file.'''
	lapData = {
		"lap" : lapCount,
		"time" : ac.getCarState(0, acsys.CS.LastLap),
		"invalidated" : lastLapInvalidated,
		"splits" : ac.getLastSplits(0)
	}

	rw.writeLogEntry(lapData)

def closeLog():
	'''Releases the current log file.'''
	rw.closeLog()

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
