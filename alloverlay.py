import sys
import cv2
import time
import numpy as np
import features as corn
import camera as cali
cv2.ocl.setUseOpenCL(False)
#videoname = input("enter input")
videoname = "camera10001-0200.mkv"
cv2.setUseOptimized(True)
fps = 0
BLACK = (0,0,0)
def frameshower(image):
    global fps, BLACK
    return cv2.putText(image, str(fps), (0,100), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, BLACK, 2)
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
    cali1 = cali.Calibrator(camera_data={"pixelsize":None, "matrixsize":None, "baseline":1, "lens_distance":None})
    corn1 = corn.Corner_detector(image)
    matc1 = corn.Feature_matcher()
while cap.isOpened() and cap2.isOpened():
    framestart_time = time.time()
    ret[0], image[0] = cap.read()
    ret[1], image[1] = cap2.read()
    tomatch = [[[], []], [[], []]]
    if ret:
        backupimg = image
        for i, img in enumerate(image):
            if cali1.calibrated:
                backupimg[i] = corn1.image = cali1.undistort(np.float32(cv2.cvtColor(image[i], cv2.COLOR_BGR2GRAY)), cali1.mtx, cali1.dist)
            else:
                backupimg[i] = corn1.image = np.float32(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
            keypointsanddescriptors=corn1.updateanddisplay()
            tomatch[0][i] = keypointsanddescriptors[0]
            tomatch[1][i] = keypointsanddescriptors[1]
            cv2.imshow("camera "+str(i), cv2.drawKeypoints(img, keypointsanddescriptors[1], None, color=(0,255,0)))
        image = backupimg
        print(ret, image)
        matches = matc1.match(np.uint8(tomatch[0]))[:100]
        cv2.imshow("matches1", frameshower(cv2.drawMatches(np.uint8(image[0]),tomatch[1][0],np.uint8(image[1]),tomatch[1][1],matches,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)))
        cv2.imshow("matches2", frameshower(cv2.drawMatches(np.uint8(image[1]),tomatch[1][0],np.uint8(image[0]),tomatch[1][1],matches,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)))
        #cv2.imshow("test", image)
        point_positions = []
        #for m in matches:
         #   locs = [tomatch[0][m.queryIdx], tomatch[0][m.trainIdx]]
          #  point_positions.append(cali1.calculate_point_relative_position(locs))
        key = cv2.waitKey(1)
        if key == ord("c"):
            cali1.calibrate(cali1.image)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break
        framestop_time = time.time()
        frame_duration = framestop_time-framestart_time
        fps = 1/frame_duration
    else:
        print("capture not reading")
        break
cap.release()
