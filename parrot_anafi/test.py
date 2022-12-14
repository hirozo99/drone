#マーカーIDと、動画を重ねて表示する
import cv2
from cv2 import aruco
import numpy as np

import olympe
import os
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveTo
from olympe.messages.ardrone3.PilotingState import AltitudeChanged
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged, moveToChanged,
import olympe.enums.move as mode

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
    assert drone(TakeOff()).wait().success()

def change_altitude():
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    drone(AltitudeChanged(altitude=3.0, _policy='check_wait', _float_tol=(1e-07, 1e-09))).wait().success()

def test_moveto():
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    """法政大学小金井キャンパスの中庭、白い四角タイルの角"""
    drone(moveTo(35.709751, 139.523337, 3.0, mode.orientation_mode.to_target, 0.0)).wait().success()

def test_landing():
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    assert drone(Landing()).wait().success()
    drone.disconnect()

def aruco_landing():
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dict_aruco, parameters=parameters)

        list_ids = np.ravel(ids)
        print(list_ids)
        if list_ids[0] == 0:
            print("着陸体制に入ります！！")
            test_landing()
            break

def main():
    test_takeoff()
    change_altitude()
    test_moveto()
    aruco_landing()

if __name__ == "__main__":
    main()