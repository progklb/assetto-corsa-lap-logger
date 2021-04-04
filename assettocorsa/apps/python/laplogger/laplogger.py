import ac
import acsys
import sys

import os

import rw
from logger import acLog
from models import Vehicle
from models import Track
from models import Lap
from models import Session
from models import Log

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

lblLapCount = None
lblBestLap = None
lblLastLap = None
lblCurrentTime = None

lapCount = 0
bestLap = 0
lastLap = 0

lastLapInvalidated = False

session = None


# -----------------------------------------
# Asseto Corsa Events
# -----------------------------------------

def acMain(ac_version):

	acLog("Starting {}".format(APP_NAME))

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

	setLog()

	return APP_NAME

def acUpdate(deltaT):
	updateState()
	refreshUI()

def acShutdown():
	closeLog()


# -----------------------------------------
# Helper Functions
# -----------------------------------------

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
		recordLap()

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

def setLog():
	'''Opens a log file for the current session.'''

	vehicle = Vehicle(ac.getCarName(0))
	track = Track(ac.getTrackName(0), ac.getTrackConfiguration(0))
	log = Log(vehicle, track)

	rw.setLog(log)

	from datetime import datetime

	global session
	session = Session(datetime.now)

	#TODO Populate session data. Write to file.

def recordLap():
	'''Writes a new log entry to the log file.'''

	global lastLapInvalidated

	lapData = Lap()
	lapData.lapNo = lapCount
	lapData.time = ac.getCarState(0, acsys.CS.LastLap)
	lapData.split = ac.getLastSplits(0)
	lapData.invalidated = lastLapInvalidated

	#TODO Populate lap data. Write to file.

	rw.writeLap('!')

	acLog('Lap completed')

def closeLog():
	#TODO Finalise session entry.
	pass

# -----------------------------------------
# Event Handlers
# -----------------------------------------

def onAppDismissed():
	ac.console("LapLogger Dismissed")
	active = False
	acLog("Dismissed")

def onAppActivated():
	ac.console("LapLogger Activated")
	active = True
	acLog("Activated")
