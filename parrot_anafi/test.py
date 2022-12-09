# import olympe
# import time
# from olympe.messages.ardrone3.Piloting import TakeOff, Landing
import cv2
from cv2 import aruco
import os
import numpy as np
import time

###anafiの設定
cameraID = 'rtsp://192.168.42.1/live'
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'

class MarkSearch:
    ### --- aruco設定 --- ###
    dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters_create()

    def __init__(self, cameraID):
        self.cap = cv2.VideoCapture(cameraID)

    def get_markID(self):
        """
        静止画を取得し、arucoマークのidリストを取得する
        """
        ret, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dict_aruco, parameters=parameters)

        frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
        cv2.imshow('frame', frame_markers)
        list_ids = np.ravel(ids)
        return list_ids

if __name__ == "__main__":
    import cv2
    from cv2 import aruco
    import numpy as np
    import time

    ### --- aruco設定 --- ###
    dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters_create()

    ### --- parameter --- ###
    ###anafiの設定
    cameraID = 'rtsp://192.168.42.1/live'
    os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'
    cam0_mark_search = MarkSearch(cameraID)


    try:
        while True:
            print(' ----- get_markID ----- ')
            print(cam0_mark_search.get_markID())
            print('idを検出中')
            if cam0_mark_search.get_markID()[0] == 0:
                print("着陸体制に入ります。")
                time.sleep(3)
                break
            time.sleep(1)
    except KeyboardInterrupt:
        cam0_mark_search.cap.release()