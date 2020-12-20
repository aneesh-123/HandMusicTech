from picamera import PiCamera
from time import sleep
import cv2
import time
import numpy as np

def empty(a):
    pass
##### Image Caputre with Camera########
camera = PiCamera()

###Trackbar initialization ###############
path = '/home/pi/Desktop/image.jpg'
cv2.namedWindow("trackbars")
cv2.resizeWindow("trackbars", 640, 240)
cv2.createTrackbar("Hue Min", "trackbars",0,179,empty)
cv2.createTrackbar("Hue Max", "trackbars",179,179,empty)
cv2.createTrackbar("Sat Min", "trackbars",0,255,empty)
cv2.createTrackbar("Sat Max", "trackbars",255,255,empty)
cv2.createTrackbar("Value Min", "trackbars",0,255,empty)
cv2.createTrackbar("Value Max", "trackbars",255,255,empty)




###take a picture#######################
camera.start_preview(fullscreen=False,window=(100,200,1000,1000))
sleep(10)
camera.capture(path, use_video_port = False)
camera.stop_preview()

img = cv2.imread(path)
img = cv2.resize(img, (960,540))

##HSV Trackbar
while True:
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue Min", "trackbars")
    h_max = cv2.getTrackbarPos("Hue Max", "trackbars")
    s_min = cv2.getTrackbarPos("Sat Min", "trackbars")
    s_max = cv2.getTrackbarPos("Sat Max", "trackbars")
    v_min = cv2.getTrackbarPos("Value Min", "trackbars")
    v_max = cv2.getTrackbarPos("Value Max", "trackbars")
    print(h_min, h_max, s_min, s_max, v_min, v_max)
    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imgHSV, lower, upper)

#     # Display image

    img = cv2.resize(img, (760,440))
    imgHSV = cv2.resize(imgHSV, (760,440))
    mask = cv2.resize(mask, (760,440))
    mask = cv2.rectangle(mask, (50,25), (300,275), (255,0,0), 8)
    cv2.imshow('Mask', mask)
    cv2.imshow('yo', img)
    cv2.imshow('HSV', imgHSV)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
print("H_min",h_min,
      "H_max", h_max, "\nSat min", s_min, "Sat_Max", s_max, "\nVal_min", v_min, "val_max", v_max)