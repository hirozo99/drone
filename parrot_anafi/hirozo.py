import cv2
from cv2 import aruco
import numpy as np
import os

import olympe
import time
from olympe.messages.ardrone3.Piloting import TakeOff, Landing
from olympe.messages.ardrone3.Piloting import moveBy

# 変数の指定
DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")
H = 6

# aruco設定
RTSP_URL ='rtsp://192.168.42.1/live'
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS']='rtsp_transport;udp'
dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()
cap = cv2.VideoCapture(RTSP_URL)

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

def aruco_landing():
    while True:
        frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dict_aruco, parameters=parameters)
        # frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
        # cv2.imshow('frame', frame_markers)
        list_ids = list(np.ravel(ids))
        list_ids.sort()
        print(list_ids)
        if list_ids[0] == 0:
            print("着陸体制に入ります！！")
            landing()
            # if list_ids[-1] == 4 and len(list_ids) == 5:
            #     print("--------------------------着陸--------------------------")
            #     break

def main():
    try:
        takeoff()
        gain_altitude()
        aruco_landing()
    except KeyboardInterrupt:
        landing()

if __name__ == "__main__":
    main()