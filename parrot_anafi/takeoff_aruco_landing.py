#マーカーIDと、動画を重ねて表示する
import cv2
from cv2 import aruco
import numpy as np

# parrot
import olympe
import os
from olympe.messages.ardrone3.Piloting import TakeOff, Landing
from olympe.messages.ardrone3.PilotingState import AltitudeChanged


DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")

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
        cv2.imshow('display', frame_markers)
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
        aruco_landing()
    except KeyboardInterrupt:
        test_landing()

if __name__ == "__main__":
    main()
