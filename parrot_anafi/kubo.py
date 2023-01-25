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

RTSP_URL ='rtsp://192.168.42.1/live'
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS']='rtsp_transport;udp'


### --- aruco設定 --- ###
dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()
cap = cv2.VideoCapture(RTSP_URL)

# 変数の指定
DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")

# 動画ファイル保存用の設定
fps = int(cap.get(cv2.CAP_PROP_FPS))                    # カメラのFPSを取得
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))              # カメラの横幅を取得
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))             # カメラの縦幅を取得
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')        # 動画保存時のfourcc設定（mp4用）
video = cv2.VideoWriter('video.mp4', fourcc, fps, (w, h))  # 動画の仕様（ファイル名、fourcc, FPS, サイズ）


def test_takeoff(drone):
    time.sleep(2)
    print("--------------------test_takeoff--------------------")
    assert drone(TakeOff()).wait().success()
    time.sleep(3)

def test_move(drone, F, H):
    print("--------------------test_move--------------------")
    assert drone(
        extended_move_by(F, 0, -H, 0, 0.7, 0.7, 0.7)
    ).wait().success()

def main():
    a = 0
    b = 0
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    time.sleep(1)
    test_takeoff(drone)
    time.sleep(1)
    # test_move(drone, 0, 0)
    # time.sleep(1)

    try:
        while True:
            time.sleep(1)
            ret, frame = cap.read()
            time.sleep(1)
            # gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            # corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dict_aruco, parameters=parameters)
            # frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
            if ret == True:
                a += 1
                print(a)
                cv2.imshow('frame', frame) #frame_markers
            else:
                b += 1
                print(str(b) + "+++++++++++")
            # # video.write(frame)
            # print(corners)
            # list_ids = list(np.ravel(ids))
            # list_ids.sort()
            # print(list_ids)
            #
            # if list_ids[0] == 0:
            #     print("着陸体制に入ります！！")
            #     if list_ids[-1] == 4 and len(list_ids) == 5:
            #         print("--------------------------着陸--------------------------")
            #         break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyWindow('frame')
        cap.release()
    except KeyboardInterrupt:
        cv2.destroyWindow('frame')
        cap.release()


# def main():
#     aruco()

if __name__ == "__main__":
    main()