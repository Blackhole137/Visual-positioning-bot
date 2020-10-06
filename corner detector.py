import sys
import cv2
import numpy as np
class Corner_detector():
    def __init__(self, image, corners=[]):
        self.corners = corners
        self.image = image
    def update(self, image=None):
        if image != None:
            self.image = image
        gray = np.float32(cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY))
        self.corners = cv2.cornerHarris(gray, 3, 3, 0, 1)
        return self.corners
videoname = input("enter input")
try:
	videoname = int(videoname)
	cap = cv2.VideoCapture(0)
except:
	cap = cv2.VideoCapture(videoname)
while cap.isOpened():
    ret, image = cap.read()
    if ret == True:
        corn = Corner_detector(image)
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


