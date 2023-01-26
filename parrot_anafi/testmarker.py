#マーカーIDと、動画を重ねて表示する
import time
import cv2
from cv2 import aruco
import os
import numpy as np

# parrot
import olympe
import os
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveBy
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
from olympe.messages.move import extended_move_by

# 変数の指定
DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")

RTSP_URL ='rtsp://192.168.42.1/live'
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS']='rtsp_transport;udp'

### --- aruco設定 --- ###
dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()
cap = cv2.VideoCapture(RTSP_URL)

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
    assert drone(Landing()).wait().success()
    drone.disconnect()

def video_recognize():
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    test_takeoff(drone)
    test_move(drone, 0, 1)
    time.sleep(1)
    while True:
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dict_aruco, parameters=parameters)
            # frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
            # cv2.imshow('frame', frame_markers)
            # video.write(frame)
        list_ids = list(np.ravel(ids))
        list_ids.sort()
        print(list_ids)

        if list_ids[0] == 0:
            index = np.where(ids == 0)[0][0]  # num_id が格納されているindexを抽出
            cornerUL = corners[index][0][0]
            cornerUR = corners[index][0][1]
            cornerBR = corners[index][0][2]
            cornerBL = corners[index][0][3]

            center = [(cornerUL[0] + cornerBR[0]) / 2, (cornerUL[1] + cornerBR[1]) / 2]

            print('左上 : {}'.format(cornerUL))
            print('右上 : {}'.format(cornerUR))
            print('右下 : {}'.format(cornerBR))
            print('左下 : {}'.format(cornerBL))
            print('中心 : {}'.format(center))
            time.sleep(1)
            # print("着陸体制に入ります！！")
            if list_ids[-1] == 4 and len(list_ids) == 5:
                print("--------------------------着陸--------------------------")
                break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def main():
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    try:
        video_recognize()
    except KeyboardInterrupt:
        test_landing(drone)


if __name__ == "__main__":
    main()