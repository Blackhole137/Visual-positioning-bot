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
videoname2 = 0
try:
	videoname = int(videoname)
	cap2 = cv2.VideoCapture(videoname)
except:
	cap2 = cv2.VideoCapture(videoname)
if cap.isOpened()and cap2.isOpened():
    ret = []
    image = []
    corns = []
    calis = []
    for j in range(2):
        ret1, image1 = cap.read()
        ret.append(ret1)
        image.append(np.float32(cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)))
        corns.append(corn.Corner_detector(image))
        calis.append(cali.Calibrator(image))
while cap.isOpened():
    ret[0], image[0] = cap.read()
    ret[1], image[1] = cap2.read()
    if ret:
        backupimg = image
        for i, img in enumerate(image):
            backupimg[i] = np.float32(cv2.cvtColor(image[i], cv2.COLOR_BGR2GRAY))
        image = backupimg
        backupcorns = corns
        for i, c in enumerate(corns):
            backupcorns[i].image = image[i]
            calis[i].image = image[i]
            cv2.imshow("image {}".format(i), backupcorns[i].updateanddisplay())
        corns = backupcorns
        print(ret, image)
        #cv2.imshow("test", image)
        key = cv2.waitKey(1)
        if key == ord("c"):
            cali1.calibrate(cali1.image)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break
    else:
        print("capture not reading")
