import olympe
import os
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveTo
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged, MoveToChanged
from olympe.enums.ardrone3.Piloting import MoveTo_Orientation_mode

DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")


def takeoff(drone):
    drone(
        TakeOff()
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()


def moveto(drone):
    drone(
        moveTo(35.70979750, 139.522988, 3.0, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> MoveToChanged(status="DONE", _timeout=10)
    ).wait().success()


def landing(drone):
    drone(Landing()).wait().success()


def main(drone):
    drone.connect()
    takeoff(drone)
    moveto(drone)
    landing(drone)
    drone.disconnect()


if __name__ == "__main__":
    drone = olympe.Drone(DRONE_IP)
    main(drone)
