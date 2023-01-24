#マーカーIDと、動画を重ねて表示する
import cv2
from cv2 import aruco
import numpy as np
import time

# parrot
import olympe
import os
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveBy
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
from olympe.messages.move import extended_move_by

# 変数の指定
DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")
H = 2
F = 1

RTSP_URL ='rtsp://192.168.42.1/live'
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS']='rtsp_transport;udp'


### --- aruco設定 --- ###
dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()

cap = cv2.VideoCapture(RTSP_URL)

def test_takeoff(drone):
    print("--------------------test_takeoff--------------------")
    assert drone(TakeOff()).wait().success()
    time.sleep(3)

def test_move(drone, H):
    print("--------------------test_move--------------------")
    drone(
        extended_move_by(0, 0, -H, 0, 0.7, 0.7, 0.7)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()

def forward(drone, F):
    print("***************forward***************")
    drone(
        extended_move_by(F, 0, 0, 0, 0.3, 0.3, 0.3)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()

def test_landing(drone):
    print("--------------------test_landing--------------------")
    assert drone(Landing()).wait().success()
    drone.disconnect()

def aruco_landing(drone):
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dict_aruco, parameters=parameters)
        # frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
        # cv2.imshow('frame', frame_markers)
        list_ids = list(np.ravel(ids))
        list_ids.sort()
        print(list_ids)
        time.sleep(1.5)
        if list_ids[0] == 0:
            print("***************landing***************")
            test_landing(drone)
            break

def main():
    try:
        drone = olympe.Drone(DRONE_IP)
        drone.connect()
        test_takeoff(drone)
        test_move(drone, 2)
        # forward(drone, 0.2)
        aruco_landing(drone)
    except KeyboardInterrupt:
        test_landing(drone)

if __name__ == "__main__":
    main()
