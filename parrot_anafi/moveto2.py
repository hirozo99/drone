# -*- coding: UTF-8 -*-
# !/usr/bin/python3

import olympe
import os, csv, time, tempfile
from olympe.messages.ardrone3.GPSSettingsState import GPSFixStateChanged, HomeChanged
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing, moveTo
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
import olympe.enums.move as mode

DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")

"""def moveto(drone, latitude, longitude, altitude, orientation_mode, heading):
    drone(moveTo(
    latitude,
    longitude,
    altitude,
    orientation_mode,
    heading
)).wait()"""

if __name__ == "__main__":
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    assert drone(TakeOff()).wait().success()
    time.sleep(10)
    assert drone(
        moveTo(drone, 35.70979750, 139.522988, 3.0)
        >> moveToChanged(status=status.DONE, _timeout=10)
    ).wait().success()
    assert drone(Landing()).wait().success()
    drone.disconnect()

