#マーカーIDと、動画を重ねて表示する
import cv2
from cv2 import aruco
import numpy as np
import time

# parrot
import olympe
import os
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveBy

# 変数の指定
DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")
H = 7

RTSP_URL ='rtsp://192.168.42.1/live'
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS']='rtsp_transport;udp'


### --- aruco設定 --- ###
dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()

cap = cv2.VideoCapture(RTSP_URL)

def test_takeoff():
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    print("--------------------test_takeoff--------------------")
    assert drone(TakeOff()).wait().success()

def gain_altitude():
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    print("***************gain_altitude***************")
    drone(moveBy(0, 0, -H, 0)).wait().success()
    time.sleep(5)

def test_landing():
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    print("--------------------test_landing--------------------")
    assert drone(Landing()).wait().success()
    drone.disconnect()

def aruco_landing():
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dict_aruco, parameters=parameters)
        frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
        cv2.imshow('frame', frame_markers)
        list_ids = list(np.ravel(ids))
        list_ids.sort()
        print(list_ids)
        if list_ids[0] == 0:
            print("***************landing***************")
            test_landing()
            break

def main():
    try:
        test_takeoff()
        gain_altitude()
        aruco_landing()
    except KeyboardInterrupt:
        test_landing()

if __name__ == "__main__":
    main()
