import cv2
from cv2 import aruco
import os

RTSP_URL ='rtsp://192.168.42.1/live'
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS']='rtsp_transport;udp'
dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()

# OpenCVのarucoモジュールを読み込み
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)

# カメラからの画像を取得
cap = cv2.VideoCapture(RTSP_URL)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # マーカー検出
    corners, ids, _ = cv2.aruco.detectMarkers(frame, dictionary)

    if ids is not None:
        # 検出したマーカーの座標を出力
        for i in range(len(ids)):
            print(corners[i][0])

    # 画面に検出したマーカーを描画
    cv2.aruco.drawDetectedMarkers(frame, corners, ids)
    cv2.imshow("Aruco Marker", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
