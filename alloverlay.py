import sys
import cv2
import numpy as np
import corner_detector as corn
#videoname = input("enter input")
videoname = 0
try:
	videoname = int(videoname)
	cap = cv2.VideoCapture(videoname)
except:
	cap = cv2.VideoCapture(videoname)
if cap.isOpened():
    ret, image = cap.read()
    corn1 = corn.Corner_detector(image)
while cap.isOpened():
    ret, image = cap.read()
    if ret:
        corn1.image = image 
        cv2.imshow("image", corn1.updateanddisplay())
        print(ret, image)
        #cv2.imshow("test", image)
        cv2.waitKey(1)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break
    else:
        print("capture not reading")
        break
cap.release()
