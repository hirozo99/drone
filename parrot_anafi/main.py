"""離陸した後、マーカーIDを取得するプログラム"""
import olympe
import os
import time
import cv2
from cv2 import aruco
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveTo
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged,MoveToChanged
from olympe.enums.ardrone3.Piloting import MoveTo_Orientation_mode


from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing

DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")
RTSP_URL ='rtsp://192.168.42.1/live'
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS']='rtsp_transport;udp'

### --- aruco設定 --- ###
dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()

cap = cv2.VideoCapture(RTSP_URL)
def takeoff(drone):
    drone(
        TakeOff()
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()

def moveto(drone):
    drone(
        moveTo(35.709750, 139.523334,3.0,MoveTo_Orientation_mode.TO_TARGET,0.0)
        >> MoveToChanged(status = "DONE", _timeout=10)
    ).wait().success()

def landing(drone):
    drone(Landing()).wait().success()

def get_id():
    try:
        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

            corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dict_aruco, parameters=parameters)

            frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
            cv2.imshow('frame', frame_markers)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyWindow('frame')
        cap.release()
    except KeyboardInterrupt:
        cv2.destroyWindow('frame')
        cap.release()

def main(drone):
    drone.connect()
    takeoff(drone)
    moveto(drone)
    get_id()
    landing(drone)
    drone.disconnect()


if __name__ == "__main__":
    drone = olympe.Drone(DRONE_IP)
    main(drone)

