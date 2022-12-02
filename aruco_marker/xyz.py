import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import moviepy.editor as mpy
from tqdm import tqdm
from cv2 import aruco
from mpl_toolkits.mplot3d import axes3d, Axes3D

DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")
RTSP_URL ='rtsp://192.168.42.1/live'
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS']='rtsp_transport;udp'

### --- aruco設定 --- ###
dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()


cap = cv2.VideoCapture(RTSP_URL)

def npy_to_gif(npy, filename):
    clip = mpy.ImageSequenceClip(list(npy), fps=10)
    clip.write_gif(filename)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dict_aruco, parameters=parameters)

    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
    cv2.imshow('frame', frame_markers)
    marker_length = 0.07  # [m] ### 注意！
    mtx = np.load(cap)
    dist = np.load(cap)

    XYZ = []
    RPY = []
    V_x = []
    V_y = []
    V_z = []

    for frame in cap[:500:25]:  # 全部処理すると重いので…
        frame = frame[..., ::-1]  # BGR2RGB
        corners, ids, _ = cv2.aruco.detectMarkers(frame)

        if len(corners) == 0:
            continue

        rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners, marker_length, mtx, dist)

        R = cv2.Rodrigues(rvec)[0]  # 回転ベクトル -> 回転行列
        R_T = R.T
        T = tvec[0].T

        xyz = np.dot(R_T, - T).squeeze()
        XYZ.append(xyz)

        rpy = np.deg2rad(cv2.RQDecomp3x3(R_T)[0])
        RPY.append(rpy)

        V_x.append(np.dot(R_T, np.array([1, 0, 0])))
        V_y.append(np.dot(R_T, np.array([0, 1, 0])))
        V_z.append(np.dot(R_T, np.array([0, 0, 1])))

        # ---- 描画
        cv2.aruco.drawDetectedMarkers(frame, corners, ids, (0, 255, 255))
        cv2.aruco.drawAxis(frame, mtx, dist, rvec, tvec, marker_length / 2)
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
        # ----

    cv2.destroyAllWindows()


    def plot_all_frames(elev=90, azim=270):
        frames = []

        for t in tqdm(range(len(XYZ))):
            fig = plt.figure(figsize=(4, 3))
            ax = Axes3D(fig)
            ax.view_init(elev=elev, azim=azim)
            ax.set_xlim(-2, 2);
            ax.set_ylim(-2, 2);
            ax.set_zlim(-2, 2)
            ax.set_xlabel("x");
            ax.set_ylabel("y");
            ax.set_zlabel("z")

            x, y, z = XYZ[t]
            ux, vx, wx = V_x[t]
            uy, vy, wy = V_y[t]
            uz, vz, wz = V_z[t]

            # draw marker
            ax.scatter(0, 0, 0, color="k")
            ax.quiver(0, 0, 0, 1, 0, 0, length=1, color="r")
            ax.quiver(0, 0, 0, 0, 1, 0, length=1, color="g")
            ax.quiver(0, 0, 0, 0, 0, 1, length=1, color="b")
            ax.plot([-1, 1, 1, -1, -1], [-1, -1, 1, 1, -1], [0, 0, 0, 0, 0], color="k", linestyle=":")

            # draw camera
            ax.quiver(x, y, z, ux, vx, wx, length=0.5, color="r")
            ax.quiver(x, y, z, uy, vy, wy, length=0.5, color="g")
            ax.quiver(x, y, z, uz, vz, wz, length=0.5, color="b")

            # save for animation
            fig.canvas.draw()
            frames.append(np.array(fig.canvas.renderer.buffer_rgba()))
            plt.close()

        return frames
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyWindow('frame')
cap.release()








