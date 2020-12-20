from picamera import PiCamera
from time import sleep
import cv2
import time
import numpy as np
from FindLargestContour import largest_contour
import math

def empty(a):
    pass

ROI_start = (50,25)
ROI_end = (250,200)

counter = 0
possible_directions = [0,0,0,0]
final_direction = 0
confirm = 0
longest = 0