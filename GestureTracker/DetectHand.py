from variables import *
from FindLargestContour import *

#############################RECORD A VIDEO##################
vid = cv2.VideoCapture(0)

while(True):
    ret, img = vid.read() 
    ##HSV isolate hand
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #only do 255 - if hsv background is black
    mask = 255 - cv2.inRange(hsv, (33,0,0),(179,255,255))
    cropped_mask = mask[ROI_start[1]:ROI_end[1], ROI_start[0]:ROI_end[0]]
    cropped_img = img[ROI_start[1]:ROI_end[1], ROI_start[0]:ROI_end[0]]
    
###############################FIND THE CONTOURS, HAND, and HULL################
    contours, hierarchy = cv2.findContours(cropped_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if(len(contours) > 0):
        counter = counter + 1
        possible_hand = largest_contour(contours)
        cv2.drawContours(cropped_mask, possible_hand, -1, (0 , 255, 100),3)
        cv2.drawContours(cropped_img, possible_hand, -1, (0 , 255, 100),3)
        if(detect_Hand(possible_hand, ROI_start, ROI_end)):
            cv2.putText(img, "HAND DETECTED", (300,100),  cv2.FONT_HERSHEY_SIMPLEX, 1, (100,255,100), 4)
            hull = cv2.convexHull(possible_hand, returnPoints=False)
            center = find_center(possible_hand)
            defects = cv2.convexityDefects(possible_hand, hull)
            
            longest = 0
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                far = tuple(possible_hand[f][0])
                length = distance_points(center, far)
                if(length > longest):
                    longest = length
                    farthest_point = far
            cv2.circle(cropped_img, center, 3, (0,0,255), -1)
            cv2.line(cropped_img, center, farthest_point, (0,255,255), 4)
            direction = determine_direction(center, farthest_point)
            
            if(counter > 100):
                final_direction = direction_determiner(possible_directions)
                confirm = 0
                while(counter < 150):
                    ret, img = vid.read()
                    cv2.rectangle(img, (250,0), (650,250), (0,0,0), -1)
                    cv2.putText(img, "Keep hand in box", (300,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 3)
                    cv2.putText(img, "To Confirm hand", (300,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 3)
                    cv2.putText(img, "direction is", (300,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 3)
                    cv2.putText(img, final_direction, (300,200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0),4)
                    ##HSV isolate hand
                    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                    #only do 255 - if hsv background is black
                    mask = 255 - cv2.inRange(hsv, (35,0,0),(179,255,255))
                    cropped_mask = mask[ROI_start[1]:ROI_end[1], ROI_start[0]:ROI_end[0]]
                    cropped_img = img[ROI_start[1]:ROI_end[1], ROI_start[0]:ROI_end[0]]
              
                    contours, hierarchy = cv2.findContours(cropped_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    if(len(contours) > 0):
                        possible_hand = largest_contour(contours)
                        if(detect_Hand(possible_hand, ROI_start, ROI_end)):
                            confirm = confirm + 1
                    counter = counter + 1
                    
                    img = cv2.rectangle(img, ROI_start, ROI_end, (255,0,0), 8)
                    cv2.imshow('img',img)
                    cv2.waitKey(1)
                print("Counter ", counter)
                print("confirm ", confirm)
                if(confirm > 40):
                    print("CONFIRMED")
                    print(message_determine(final_direction))
                    cv2.rectangle(img, (250,200), (650,400), (0,0,0), -1)
                    cv2.putText(img, message_determine(final_direction), (250,300), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3)
                    for i in range(300):
                        cv2.imshow('img',img)
                        cv2.waitKey(1)
                else:
                    print("cvonfirm ", confirm)
                    print("CANCELED COMMAND")
                counter = 0
                possible_directions = [0,0,0,0]
            else:
                cv2.putText(img, "CHECKING", (300,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                possible_directions = direction_tabulator(direction, possible_directions)
        else:
            final_direction = 0
            counter = 0
            possible_directions = [0,0,0,0]
        
########################DISPLAY FRAME######################################
    
    #cv2.imshow('frame', mask)
    img = cv2.rectangle(img, ROI_start, ROI_end, (255,0,0), 8)
    cv2.imshow('img',img)
    cv2.imshow('Crop image',cropped_img)
    cv2.imshow('Crop mask', cropped_mask)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

vid.release() 
cv2.destroyAllWindows()