# -*- coding: UTF-8 -*-
#!/usr/bin/python3
from olympe.messages.camera import (
    set_camera_mode,
    set_photo_mode,
    take_photo,
    photo_progress,
)
from olympe.messages import gimbal
from olympe.messages.ardrone3.Piloting import TakeOff, Landing
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
from olympe.messages.move import extended_move_by
import olympe
import cv2
import os
import re
import csv
import requests
import shutil
import tempfile
import xml.etree.ElementTree as ET
import time

# Drone IP
ANAFI_IP = "192.168.42.1"
# Drone web server URL
ANAFI_URL = "http://{}/".format(ANAFI_IP)
# Drone media web API URL
ANAFI_MEDIA_API_URL = ANAFI_URL + "api/v1/media/medias/"
XMP_TAGS_OF_INTEREST = (
    "CameraRollDegree",
    "CameraPitchDegree",
    "CameraYawDegree",
    "CaptureTsUs",
    # NOTE: GPS metadata is only present if the drone has a GPS fix
    # (i.e. they won't be present indoor)
    "GPSLatitude",
    "GPSLongitude",
    "GPSAltitude",
)


def takeoff(drone):
    drone(
        TakeOff()
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()


def land(drone):
    drone(Landing()).wait().success()


def setup_photo_burst_mode(drone):
    drone(set_camera_mode(cam_id=0, value="photo")).wait()
    # For the file_format: jpeg is the only available option
    # dng is not supported in burst mode
    drone(
        set_photo_mode(
            cam_id=0,
            mode="single",
            format="rectilinear",
            file_format="jpeg",
            burst="burst_4_over_1s",
            bracketing="preset_1ev",
            capture_interval=0.0,
        )
    ).wait()


def take_photo_burst(drone):
    # take a photo burst and get the associated media_id
    photo_saved = drone(photo_progress(result="photo_saved", _policy="wait"))
    drone(take_photo(cam_id=0)).wait()
    photo_saved.wait()
    media_id = photo_saved.received_events().last().args["media_id"]

    return media_id

def save_photo(i):
    media_id = take_photo_burst(drone)
    # Save photo to local storage
    print("*******************************************************************************************************")
    print("photo_" + str(i)+".jpg")
    print("SAVING PICTURE")
    print("*******************************************************************************************************")
    media_info_response = requests.get(ANAFI_MEDIA_API_URL + media_id)
    media_info_response.raise_for_status()
    for resource in media_info_response.json()["resources"]:
        image_response = requests.get(ANAFI_URL + resource["url"])
        open("./keras-yolo3/photo/photo_"+str(i)+".jpg", 'wb').write(image_response.content)



def image_check_upperside(i):
    # ????????????????????????
    img = cv2.imread("./keras-yolo3/photo/photo_" + str(i)+".jpg", cv2.IMREAD_COLOR)

    # ???????????????????????????
    height, width, channels = img.shape[:3]
    print("width: " + str(width))
    print("height: " + str(height))

    # ???????????????????????????
    boxFromX = 0  # ???????????????????????? X??????
    boxFromY = 0  # ???????????????????????? Y??????
    boxToX = 4608  # ???????????????????????? X??????
    boxToY = 864  # ???????????????????????? Y??????
    # y:y+h, x:x+w??????????????????
    imgBox = img[boxFromY: boxToY, boxFromX: boxToX]

    # RGB??????????????????
    # flatten??????????????????mean??????????????????
    b = imgBox.T[0].flatten().mean()
    g = imgBox.T[1].flatten().mean()
    r = imgBox.T[2].flatten().mean()

    # RGB??????????????????
    print("***********************************************BGR********************************************************")
    print("photo_" + str(i)+".jpg")
    print("B: %.2f" % (b))
    print("G: %.2f" % (g))
    print("R: %.2f" % (r))
    print("***********************************************BGR********************************************************")

    return b, g, r


def image_check_rightside(i):
    # ????????????????????????
    img = cv2.imread("./keras-yolo3/photo/photo_" + str(i)+".jpg", cv2.IMREAD_COLOR)

    # ???????????????????????????
    height, width, channels = img.shape[:3]
    print("width: " + str(width))
    print("height: " + str(height))

    # ???????????????????????????
    boxFromX = 3456  # ???????????????????????? X??????
    boxFromY = 0  # ???????????????????????? Y??????
    boxToX = 4608  # ???????????????????????? X??????
    boxToY = 3456  # ???????????????????????? Y??????
    # y:y+h, x:x+w??????????????????
    imgBox = img[boxFromY: boxToY, boxFromX: boxToX]

    # RGB??????????????????
    # flatten??????????????????mean??????????????????
    b = imgBox.T[0].flatten().mean()
    g = imgBox.T[1].flatten().mean()
    r = imgBox.T[2].flatten().mean()

    # RGB??????????????????
    print("***********************************************BGR********************************************************")
    print("photo_" + str(i)+".jpg")
    print("B: %.2f" % (b))
    print("G: %.2f" % (g))
    print("R: %.2f" % (r))
    print("***********************************************BGR********************************************************")

    return b, g, r

p_number = 3
def move_cycle(drone):
    global p_number
    altitude = 0
    for i in range(10):
        print("*******************************************************************************************************")
        print("??????")
        print("*******************************************************************************************************")
        drone(
            extended_move_by(0, 0, -0.8, 0, 0.7, 0.7, 0.7)
            >> FlyingStateChanged(state="hovering", _timeout=5)
        ).wait().success()

        altitude = altitude + 1
        take_photo_burst(drone)
        save_photo(p_number)
        
         # ???????????????
        b, g, r = image_check_upperside(p_number)
        b_o,g_o,r_o = image_check_upperside(p_number-1)
        b_r, g_r, r_r = image_check_rightside(p_number)


       # if (r - r_o > 30) and (100 > b_r or 100 > g_r or 100 > r_r):
        #    print("*******************************************************************************************************")
         #   print("???????????????")
          #  print("*******************************************************************************************************")
           # land(drone)
            #drone.disconnect()
            #break
        
        #???
        if r_o - r > 35 or b - b_o > 35:
            print("*******************************************************************************************************")
            print("????????????")
            print("*******************************************************************************************************")
            drone(
                extended_move_by(0, 0.8, 0, 0, 0.7, 0.7, 0.7)
                >> FlyingStateChanged(state="hovering", _timeout=5)
            ).wait().success()
            take_photo_burst(drone)
            save_photo(p_number+1)
            p_number = p_number + 1
            break
        """
        #??????
        if b - b_o > 35:
            print("*******************************************************************************************************")
            print("????????????")
            print("*******************************************************************************************************")
            drone(
                extended_move_by(0, 0.8, 0, 0, 0.7, 0.7, 0.7)
                >> FlyingStateChanged(state="hovering", _timeout=5)
            ).wait().success()
            take_photo_burst(drone)
            save_photo(p_number+1)
            p_number = p_number + 1
            break
        """

        p_number = p_number + 1
       
 


    for i in range(altitude):
        print("*******************************************************************************************************")
        print("??????")
        print("*******************************************************************************************************")
        drone(
            extended_move_by(0, 0, 0.8, 0, 0.7, 0.7, 0.7)
            >> FlyingStateChanged(state="hovering", _timeout=5)
        ).wait().success()
        take_photo_burst(drone)
        save_photo(p_number)
        p_number = p_number + 1

    drone(
        extended_move_by(0, 0.8, 0, 0, 0.7, 0.7, 0.7)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()
    take_photo_burst(drone)
    save_photo(p_number)
    print("*******************************************************************************************************")
    print("1???????????????")
    print("*******************************************************************************************************")

    return altitude,p_number
        
def move(drone):
    for i in range(7):
        move_cycle(drone)
        altitude,p_number = move_cycle(drone)
        # ???????????????
        b_r, g_r, r_r = image_check_rightside(p_number)
        p_number = p_number + 1
        if 100 > b_r or 100 > g_r or 100 > r_r:
            print("*******************************************************************************************************")
            print("???????????????")
            print("*******************************************************************************************************")
            for i in range(altitude):
                drone(
                    extended_move_by(0, 0, -0.8, 0, 0.7, 0.7, 0.7)
                    >> FlyingStateChanged(state="hovering", _timeout=5)
                ).wait().success()
                take_photo_burst(drone)
                save_photo(p_number)
                p_number = p_number + 1
                
            break

def set_gimbal(drone):
    drone(gimbal.set_target(
        gimbal_id=0,
        control_mode="position",
        yaw_frame_of_reference="none",   # None instead of absolute
        yaw=0.0,
        pitch_frame_of_reference="absolute",
        pitch=-90.0,
        roll_frame_of_reference="none",     # None instead of absolute
        roll=0.0,
    )).wait()


def main(drone):
    setup_photo_burst_mode(drone)
    take_photo_burst(drone)
    save_photo(1)
    time.sleep(3)
    takeoff(drone)
    take_photo_burst(drone)
    save_photo(2)
    time.sleep(3)
    move(drone)
    land(drone)
    drone.disconnect()


if __name__ == "__main__":
    drone = olympe.Drone("192.168.42.1")
    drone.connect()
    main(drone)
