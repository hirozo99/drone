import olympe
import os
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveTo
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged, moveToChanged
import olympe.enums.move as mode
if __name__ == "__main__":
        DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")
        drone = olympe.Drone(DRONE_IP)
        drone.connect()
        drone(TakeOff() >> FlyingStateChanged(state="hovering", _timeout=5)).wait().success()
        drone(
                moveTo(35.709750, 139.522989, 5.0, mode.orientation_mode.to_target, 0.0) >> moveToChanged(latitude=35.709750, longitutde=139.522989, altitude=5.0, orientation_mode=mode.orientation_mode.to_target, status='DONE', _policy='wait') >> FlyingStateChanged(state="hovering", _timeout=5)
        ).wait().success()
        drone(Landing()).wait().success()
        drone.disconnect()