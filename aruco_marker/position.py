import numpy as np
import cv2
from cv2 import aruco
import os

DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")

RTSP_URL ='rtsp://192.168.42.1/live'
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS']='rtsp_transport;udp'

def main():
    cap = cv2.VideoCapture(RTSP_URL)
    marker_length = 0.060
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

    camera_matrix = np.load("mtx.npy")
    distortion_coeff = np.load("dist.npy")
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dict_aruco, parameters=parameters)

    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

    while True:
        ret, img = cap.read()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(img, dictionary)
        aruco.drawDetectedMarkers(img, corners, ids, (0, 255, 255))

        if len(corners) > 0:
            for i, corner in enumerate(corners):
                rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corner, marker_length, camera_matrix, distortion_coeff)

                tvec = np.squeeze(tvec)
                rvec = np.squeeze(rvec)
                rvec_matrix = cv2.Rodrigues(rvec)
                rvec_matrix = rvec_matrix[0]
                transpose_tvec = tvec[np.newaxis, :].T
                proj_matrix = np.hstack((rvec_matrix, transpose_tvec))
                euler_angle = cv2.decomposeProjectionMatrix(proj_matrix)[6]

                print("x : " + str(tvec[0]))
                print("y : " + str(tvec[1]))
                print("z : " + str(tvec[2]))
                print("roll : " + str(euler_angle[0]))
                print("pitch: " + str(euler_angle[1]))
                print("yaw  : " + str(euler_angle[2]))

                draw_pole_length = marker_length / 2
                aruco.drawAxis(img, camera_matrix, distortion_coeff, rvec, tvec, draw_pole_length)

        cv2.imshow('drawDetectedMarkers', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()