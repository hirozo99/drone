### マーカーの座標を抽出する
import cv2
from cv2 import aruco
import numpy as np
import time
import os

class MarkSearch :

    ### --- aruco設定 --- ###
    RTSP_URL = 'rtsp://192.168.42.1/live'
    os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'
    dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters_create()

    def __init__(self, RTSP_URL):
        self.cap = cv2.VideoCapture(RTSP_URL)

    def get_mark_coordinate(self, num_id):
        """
        静止画を取得し、所望のマークの座標を取得する
        """
        ret, frame = self.cap.read()
        gray = self.cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dict_aruco, parameters=parameters)

        frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
        cv2.imshow('frame', frame_markers)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyWindow('frame')
            self.cap.release()
        ### num_id のマーカーが検出された場合 ###
        if num_id in np.ravel(ids) :
            index = np.where(ids == num_id)[0][0] #num_id が格納されているindexを抽出
            cornerUL = corners[index][0][0]
            cornerUR = corners[index][0][1]
            cornerBR = corners[index][0][2]
            cornerBL = corners[index][0][3]

            center = [ (cornerUL[0]+cornerBR[0])/2 , (cornerUL[1]+cornerBR[1])/2 ]

            print('左上 : {}'.format(cornerUL))
            print('右上 : {}'.format(cornerUR))
            print('右下 : {}'.format(cornerBR))
            print('左下 : {}'.format(cornerBL))
            print('中心 : {}'.format(center))

            print(corners[index])

            return center

        return None


if __name__ == "__main__" :

    import cv2
    from cv2 import aruco
    import numpy as np
    import time

    ### --- aruco設定 --- ###
    dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters_create()

    ### --- parameter --- ###
    cameraID = 0
    cam0_mark_search = MarkSearch(cameraID)

    markID = 0

    try:
        while True:
            print(' ----- get_mark_coordinate ----- ')
            print(cam0_mark_search.get_mark_coordinate(markID))
            time.sleep(0.5)
    except KeyboardInterrupt:
        cam0_mark_search.cap.release()