from variables import *
from FindLargestContour import *

##### Read image########
camera = PiCamera()
path = '/home/pi/Desktop/image.jpg'
###take a picture#######################
camera.start_preview(fullscreen=False,window=(100,200,1000,1000))
sleep(5)
camera.capture(path, use_video_port = False)
camera.stop_preview()

img = cv2.imread(path)
##HSV isolate hand
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#only do 255 - if hsv background is black
mask = 255 - cv2.inRange(hsv, (23,0,0),(179,255,255))
cropped_mask = mask[ROI_start[1]:ROI_end[1], ROI_start[0]:ROI_end[0]]
cropped_img = img[ROI_start[1]:ROI_end[1], ROI_start[0]:ROI_end[0]]

###############################FIND THE CONTOURS, HAND, and HULL################
contours, hierarchy = cv2.findContours(cropped_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
if(len(contours) > 0):
    possible_hand = largest_contour(contours)
    cv2.drawContours(cropped_mask, possible_hand, -1, (0 , 255, 100),3)
    cv2.drawContours(cropped_img, possible_hand, -1, (0 , 255, 100),3)
    if(detect_Hand(possible_hand, ROI_start, ROI_end)):
        cv2.putText(img, "HAND DETECTED", (300,100),  cv2.FONT_HERSHEY_SIMPLEX, 1, (100,255,100), 4)
        hull = cv2.convexHull(possible_hand, returnPoints=False)
        center = find_center(possible_hand)
        defects = cv2.convexityDefects(possible_hand, hull)
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(possible_hand[s][0])
            end = tuple(possible_hand[e][0])
            far = tuple(possible_hand[f][0])
            cv2.line(img, start,end, [0,255,0], 2)
            cv2.circle(img, far, 5, [0,0,255],-1)
        #far_point = farthest_point(defefcts, possible_hand, center)
        #print(far_point)
        cv2.circle(cropped_img, center, 3, (0,0,255), -1)
        cv2.drawContours(cropped_img, [hull], -1, (0,255,255), 2)    
########################DISPLAY FRAME######################################

#cv2.imshow('frame', mask)
img = cv2.rectangle(img, ROI_start, ROI_end, (255,0,0), 8)
cv2.imshow('img',img)
cv2.imshow('Crop image',cropped_img)
cv2.imshow('Crop mask', cropped_mask)
cv2.waitKey(0)
cv2.destroyAllWindows() 