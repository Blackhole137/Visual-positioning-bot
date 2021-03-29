import sys
import cv2
import numpy as np
import features as corn
import camera as cali
#videoname = input("enter input")
videoname = "camera10001-0200.mkv"
try:
	videoname = int(videoname)
	cap = cv2.VideoCapture(videoname)
except:
	cap = cv2.VideoCapture(videoname)
videoname2 = "camera 20000-0200.mkv"
try:
	videoname = int(videoname)
	cap2 = cv2.VideoCapture(videoname)
except:
	cap2 = cv2.VideoCapture(videoname)
if cap.isOpened()and cap2.isOpened():
    ret1, image1 = cap.read()
    ret2, image2 = cap2.read()
    ret = [ret1, ret2]
    image = [np.float32(cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)), np.float32(cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY))]
    cali1 = cali.Calibrator()
    corn1 = corn.Corner_detector(image)
while cap.isOpened() and cap2.isOpened():
    ret[0], image[0] = cap.read()
    ret[1], image[1] = cap2.read()
    if ret:
        backupimg = image
        for i, img in enumerate(image):
            if cali1.calibrated:
                backupimg[i] = corn1.image = cali1.undistort(np.float32(cv2.cvtColor(image[i], cv2.COLOR_BGR2GRAY)), cali1.mtx, cali1.dist)
            else:
                backupimg[i] = corn1.image = np.float32(cv2.cvtColor(image[i], cv2.COLOR_BGR2GRAY))
            cv2.imshow("camera "+str(i), corn1.updateanddisplay())
        image = backupimg
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
