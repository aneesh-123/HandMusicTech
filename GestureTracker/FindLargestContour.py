from variables import *
import math

def largest_contour(contours):
    large = list()
    max = 0
    i = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if(area > max):
            max = area
            large.append(contours[i])
        i = i + 1
    #print("first large ",cv2.contourArea(large[len(large) - 1]))
    return large[len(large) - 1]

def detect_Hand(possible_hand, ROI_start, ROI_end):
    area = cv2.contourArea(possible_hand)
    ROI_Area = (ROI_end[0] - ROI_start[0]) * (ROI_end[1] - ROI_start[1])
    ratio = area / ROI_Area
    if(ratio > 0.03):
        return True
    else:
        return False
    
def find_center(contour):
    M = cv2.moments(contour)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    center = (cX, cY)
    return center

def distance_points(center, defect):
    return math.sqrt(((center[0] - defect[0]) **2) + ((center[1] - defect[1]) ** 2))

def determine_direction(center, defect):
    x = defect[0] - center[0]
    y = center[1] - defect[1]
    angle = abs(math.degrees(math.atan(y / x)))
    if(x < 0 and y > 0):
        angle = angle + 90
    if(x < 0 and y < 0):
        angle = angle + 180
    if(x > 0 and y < 0):
        angle = angle + 270
    
    if((angle >= 290 and angle <= 360) or (angle <= 45 and angle >= 0)):
        direction = "East"
    elif(angle >= 45 and angle <= 95):
        direction = "North"
    elif(angle > 95 and angle <= 205):
        direction = "West"
    else:
        direction = "South"
    print("angle ", angle, "direction ", direction) 
    return direction

def direction_tabulator(direction, data):
    if(direction == "North"):
        data[0] = data[0] + 1
    if(direction == "East"):
        data[1] = data[1] + 1
    if(direction == "South"):
        data[2] = data[2] + 1
    if(direction == "West"):
        data[3] = data[3] + 1
    return data

def direction_determiner(data):
    max_value = max(data)
    if(data[0] == max_value):
        return "North"
    if(data[1] == max_value):
        return "East"
    if(data[2] == max_value):
        return "South"
    if(data[3] == max_value):
        return "West"
    
def message_determine(final_direction):
    if(final_direction == "North"):
        message = "Like Song!"
    if(final_direction == "East"):
        message = "Skip Song"
    if(final_direction == "South"):
        message = "Dislike Song"
    if(final_direction == "West"):
        message = "Replay Song"
    return message
    
'''##### Read image########
camera = PiCamera()
path = '/home/pi/Desktop/image.jpg'
###take a picture#######################
camera.start_preview(fullscreen=False,window=(100,200,1000,1000))
sleep(5)
camera.capture(path, use_video_port = False)
camera.stop_preview()

img = cv2.imread(path)
img = cv2.resize(img, (960,540))
ROI_start = (50,25)
ROI_end = (250,200)
##HSV isolate hand
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = 255 - cv2.inRange(hsv, (15,0,0),(133,255,255))
cropped_mask = mask[ROI_start[1]:ROI_end[1], ROI_start[0]:ROI_end[0]]
cropped_img = img[ROI_start[1]:ROI_end[1], ROI_start[0]:ROI_end[0]]

###############################FIND THE CONTOURS################
contours, hierarchy = cv2.findContours(cropped_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
if(len(contours) > 0):
    cv2.drawContours(cropped_mask, largest_contour(contours), -1, (0 , 255, 100),3)
    cv2.drawContours(cropped_img, largest_contour(contours), -1, (0 , 255, 100),3)
    
########################DISPLAY FRAME######################################

#cv2.imshow('frame', mask)
img = cv2.rectangle(img, ROI_start, ROI_end, (255,0,0), 8)
cv2.imshow('img',img)
cv2.imshow('Crop image',cropped_img)
cv2.imshow('Crop mask', cropped_mask)
cv2.waitKey(0)
cv2.destroyAllWindows() 
'''
