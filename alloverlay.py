import sys
import cv2
import numpy as np
import features as corn
import camera as cali
#videoname = input("enter input")
videoname = 0
try:
	videoname = int(videoname)
	cap = cv2.VideoCapture(videoname)
except:
	cap = cv2.VideoCapture(videoname)
if cap.isOpened():
    ret, image = cap.read()
    image = np.float32(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    corn1 = corn.Corner_detector(image)
    cali1 = cali.Calibrator(image)
while cap.isOpened():
    ret, image = cap.read()
    if ret:
        image = np.float32(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
        corn1.image = image
        cali1.image = image 
        cv2.imshow("image", corn1.updateanddisplay())
        print(ret, image)
        #cv2.imshow("test", image)
        key = cv2.waitKey(1)
        if key == ord("c"):
            cali1.calibrate(cali1.image)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break
    else:
        print("capture not reading")
        break
cap.release()
