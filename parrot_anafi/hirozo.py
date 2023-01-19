import olympe
import os
import time
from olympe.messages.ardrone3.Piloting import TakeOff, Landing
from olympe.messages.ardrone3.Piloting import moveBy

# 変数の指定
DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")
H = 5

def takeoff():
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    assert drone(TakeOff()).wait().success()
    time.sleep(5)

def gain_altitude():
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    drone(moveBy(0, 0, -H, 0)).wait().success()
    time.sleep(5)

def landing():
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    assert drone(Landing()).wait().success()
    drone.disconnect()

def main():
    takeoff()
    try:
        gain_altitude()
        landing()
    except KeyboardInterrupt:
        landing()

if __name__ == "__main__":
    main()
