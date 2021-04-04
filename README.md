# Assetto Corsa Lap Logger

A lap-logging app for [Assetto Corsa](https://www.assettocorsa.net/home-ac).

When active the app will record lap times for the current track-vehicle combination, allowing you to analyse your improvement over time in a particular vehicle on a particular track.

---

## Features

> (Theoretical. Many of these are goals for the future.)

Features of in-game app:

- Recording of track-vehicle combination lap times.
- Recording of additional information (track conditions, vehicle setup) for in-depth analysis.
- Displaying previous laps for immediate comparison in-game.

Features of viewer app:

- Viewer app for graphing lap times.
- Ability to compare different setups and conditions.
- Ability to compare different vehicles on the same track.
- Live update via database web hooks, allows user to display the app on a separate screen and view up-to-date information.
- Possible mobile companion app that mimics to the desktop app.

## App

### Usage / Notes

The app displays a custom in-game HUD when active.

For each track-vehicle combination, a log file will be generated at the location `assettocorsa/apps/python/laplogger/logs` and session information will be written to this log. Logs assume the naming format of `vehicle_name - track_name - track_layout`.

The header of the file identifies the session configuration, while the bulk of the file is dedicated to recording lap details. For example:

Filename: `bmw_z4_gt3 - ks_nurburgring - layout_gp_b`

// TODO Change to YAML to support appending to file.
```json
{
    "track": {
        "layout": "indy", 
        "name": "ks_brands_hatch"
    }, 
    "vehicle": {
        "name": "ks_nissan_gtr_gt3"
    },
    "sessions": [
        {
			"laps": [
				{"time": 135776, "invalidated": false, "lap": 1, "splits": [47536, 46472, 41768]},
				{"time": 125238, "invalidated": false, "lap": 2, "splits": [39054, 44658, 41526]}
			],
			"config": {
			}
		}
    ]
}
```

```yaml
---
track:
  layout: indy
  name: ks_brands_hatch

vehicle:
  name: ks_nissan_gtr_gt3

sessions:

- session:
    date: "2021-01-02T12:34"
    config: {}
    laps:
    - {"time": 135776, "invalidated": false, "lap": 1, "splits": [47536, 46472, 41768]}
    - {"time": 125238, "invalidated": false, "lap": 2, "splits": [39054, 44658, 41526]}
  

- session:
    date: "2021-01-02T12:34"
    config: {}
    laps:
    - {"time": 135776, "invalidated": false, "lap": 1, "splits": [47536, 46472, 41768]}
    - {"time": 125238, "invalidated": false, "lap": 2, "splits": [39054, 44658, 41526]}
```

> TODO: This log can then be visualised as a graph in order to inspect lap splits/times.

> NOTE: It should be possible to look up the correct name/details of a vehicle by reading assettocorsa/content/cars/{vehiclename}/ui/ui_car.json.

### Logging

By default, console logs are located at `C:\Users\<Username>\My Documents\Assetto Corsa\logs`

There are two kinds of AC log commands available:

- `ac.log` which logs to `py_log.txt`. This persists after the session is ended.
- `ac.console` which logs to `log.txt` and is available via the console (Home key) in game. This persists only while running.

> TODO: Replace with an image containing only the Lap Logger app.

![Image](/Documentation/20190518203937-HUD.jpg)

## Installation

In order to install:

- **Manual**
  - Merge the folder `assettocorsa` with the `assettocorsa` game folder (i.e. Assetto Corsa installation directory).

- **Automated**
  - Update the `deploy.py` script to point to your Assetto Corsa installation directory.
  - Via terminal, execute the `python ./deploy.py`

- After launching the game, ensure that the app is enabled in the settings menu.

Troubleshooting:

- Inspect the logs should any issue occur (see **Logging** section)

## Credit

Thanks to [**assettocorsamods**](https://assettocorsamods.net) for:

- The link to **Giovanni Romagnoli's** [AC Python API documentation](https://assettocorsamods.net/threads/doc-python-doc.59/).
- A fantastic [onboarding tutorial](https://assettocorsamods.net/threads/getting-started-with-ac-app-developing.716/) to modding in AC.
