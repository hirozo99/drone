#マーカーIDと、動画を重ねて表示する
import time
from threading import Thread
import concurrent.futures
import cv2
from cv2 import aruco
import numpy as np

# parrot
import olympe
import os
from olympe.messages.ardrone3.Piloting import TakeOff, Landing
from olympe.messages.ardrone3.PilotingState import AltitudeChanged
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
from olympe.messages.move import extended_move_by


DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")

RTSP_URL ='rtsp://192.168.42.1/live'
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS']='rtsp_transport;udp'


### --- aruco設定 --- ###
dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()
cap = cv2.VideoCapture(RTSP_URL)

# 動画ファイル保存用の設定
fps = int(cap.get(cv2.CAP_PROP_FPS))                    # カメラのFPSを取得
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))              # カメラの横幅を取得
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))             # カメラの縦幅を取得
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')        # 動画保存時のfourcc設定（mp4用）
video = cv2.VideoWriter('test1.mp4', fourcc, fps, (w, h))  # 動画の仕様（ファイル名、fourcc, FPS, サイズ）

def test_takeoff(drone):
    print("--------------------test_takeoff--------------------")
    assert drone(TakeOff()).wait().success()
    time.sleep(3)


def test_landing(drone):
    print("--------------------test_landing--------------------")
    drone(Landing()).wait().success()
    drone.disconnect()

def test_move(drone):
    print("--------------------test_move--------------------")
    drone(
        extended_move_by(0, 0, -2.0, 0, 0.7, 0.7, 0.7)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()

def aruco_landing(drone):
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dict_aruco, parameters=parameters)
        frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
        cv2.imshow('frame', frame_markers)
        video.write(frame)  # 保存
        list_ids = list(np.ravel(ids))
        list_ids.sort()
        print(list_ids)
        time.sleep(0.5)
        test_takeoff(drone)
        if list_ids[0] == 0:
            print("***************landing***************")
            test_landing(drone)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def main():
    # executor = concurrent.futures.ProcessPoolExecutor(max_workers=2)
    # thread_1 = Thread(target=test_video)
    # thread_2 = Thread(target=drone_moving, args=(drone))
    try:
        drone = olympe.Drone(DRONE_IP)
        drone.connect()
        # test_move(drone)
        aruco_landing(drone)
        # thread_1.start()
        # thread_2.start()
        # executor.submit(test_video())
        # executor.submit(drone_moving(drone))
    except KeyboardInterrupt:
        test_landing(drone)

if __name__ == "__main__":
    main()
