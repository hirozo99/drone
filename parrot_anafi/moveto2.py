# -*- coding: UTF-8 -*-
# !/usr/bin/python3

import olympe
import os
import time
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing, moveTo

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
    assert drone(moveTo(drone, 139.522988, 35.70979750, 3.0)).wait().success()
    assert drone(Landing()).wait().success()
    drone.disconnect()

