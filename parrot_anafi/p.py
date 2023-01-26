# parrot
import olympe
import os
import time
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveBy
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
from olympe.messages.move import extended_move_by

# 変数の指定
DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")

def test_takeoff(drone):
    print("--------------------test_takeoff--------------------")
    assert drone(TakeOff()).wait().success()
    time.sleep(5)

def test_move(drone, F, H):
    print("--------------------test_move--------------------")
    drone(
        extended_move_by(F, 0, -H, 0, 0.7, 0.7, 0.7)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()
    time.sleep(5)

def test_landing(drone):
    print("--------------------test_landing--------------------")
    drone(Landing()).wait().success()
    drone.disconnect()

def go(distance):
    os.system("python3 go.py -m {}".format(distance))

def height(z):
    os.system("python3 height.py -m {}".format(z))

def main():
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    test_takeoff(drone)
    time.sleep(1)
    height(1)
    time.sleep(1)
    go(1)
    time.sleep(1)
    test_landing(drone)

if __name__ == "__main__":
    main()