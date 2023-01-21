#マーカーIDと、動画を重ねて表示する
import cv2
from cv2 import aruco
import os
import numpy as np

RTSP_URL ='rtsp://192.168.42.1/live'
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS']='rtsp_transport;udp'


### --- aruco設定 --- ###
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(dictionary, parameters)
cap = cv2.VideoCapture(RTSP_URL)
frame = cv2.imread(...)

try:
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dictionary, parameters=parameters)
        markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(frame)
        frame_markers = aruco.drawDetectedMarkers(frame.copy(), markerCorners, markerIds)
        cv2.imshow('frame', frame_markers)
        list_ids = list(np.ravel(markerIds))
        list_ids.sort()
        print(list_ids)
        if list_ids[0] == 0:
            print("着陸体制に入ります！！")
            if list_ids[-1] == 4 and len(list_ids) == 5:
                print("--------------------------着陸--------------------------")
                break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyWindow('frame')
    cap.release()
except KeyboardInterrupt:
    cv2.destroyWindow('frame')
    cap.release()