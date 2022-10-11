import cv2

aruco = cv2.aruco
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

def arGenerator():
  for i in range(50):
    fileName = "{}.png".format(i)
    generator = aruco.drawMarker(dictionary, i, 50)
    cv2.imwrite(fileName, generator)

arGenerator()