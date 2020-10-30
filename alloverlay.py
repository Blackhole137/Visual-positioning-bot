import sys
import cv2
import numpy as np
import corner_detector as corn
videoname = input("enter input")
try:
	videoname = int(videoname)
	cap = cv2.VideoCapture(0)
except:
	cap = cv2.VideoCapture(videoname)
while cap.isOpened():
    ret, image = cap.read()
    if ret == True:
        corn1 = corn.Corner_detector(image)
        dst = corn.update()
        #dst = cv2.dilate(dst, None)
        image[dst>0.01*dst.max()] = [0, 0, 255] 
        cv2.imshow("image", image)
        cv2.waitKey(1)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break
    else:
        break
cap.release()
