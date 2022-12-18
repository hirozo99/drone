#マーカーIDと、動画を重ねて表示する
import cv2
from cv2 import aruco
import numpy as np

import olympe
import os
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveTo
from olympe.messages.ardrone3.PilotingState import AltitudeAboveGroundChanged
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged, moveToChanged
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

def change_altitude(alt):
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    drone(AltitudeAboveGroundChanged(altitude=alt, _policy='check_wait', _float_tol=(1e-07, 1e-09))).wait().success()

def test_moveto():
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    """法政大学小金井キャンパスの中庭、白い四角タイルの角"""
    drone(moveTo(35.709748, 139.523333, 8.0, mode.orientation_mode.to_target, 0.0)).wait().success()

def test_landing():
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    assert drone(Landing()).wait().success()
    drone.disconnect()

def aruco_landing():
    try:
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
                print("着陸体制に入ります！！")
                change_altitude(3.0)
                if list_ids[-1] == 4 and len(list_ids) == 5:
                    print("--------------------------着陸--------------------------")
                    test_landing()
                    break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                test_landing()
                break
        cv2.destroyWindow('frame')
        cap.release()
        test_landing()
    except KeyboardInterrupt:
        cv2.destroyWindow('frame')
        cap.release()
        test_landing()
def main():
    test_takeoff()
    change_altitude(8.0)
    test_moveto()
    aruco_landing()

if __name__ == "__main__":
    main()