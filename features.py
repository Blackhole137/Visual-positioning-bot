import sys
import cv2
import numpy as np
cv2.ocl.setUseOpenCL(False)
class Unknown_algorythm_error(Exception):
    def __init__(self):
        pass
class No_image_passed_error(Exception):
    def __int__ (self):
        pass
class Corner_detector():
    def __init__(self, image, detectortype="ORB", corners=[]):
        self.corners = corners
        self.image = image
        self.detectortype = detectortype
    def update(self, image=None):
        if self.detectortype == "Harris":
            self.corners = cv2.cornerHarris(image, 3, 3, 0, 1)
        elif self.detectortype == "Shi-Tomasi":
            self.corners = cv2.goodFeaturesToTrack(image, 3, 3, 0, 1)
        elif self.detectortype == "ORB":
            orb = cv2.ORB_create()
            kp, self.corners = orb.detectAndCompute(image.astype(np.uint8),None)
        elif self.detectortype == "SURF":
            minHessian = 400
            detector = cv2.features2d_SURF(hessianThreshold=minHessian)
            keypoints1, descriptors1 = detector.detectAndCompute(img1, None)
            keypoints2, descriptors2 = detector.detectAndCompute(img2, None)
        else:
            raise Unknown_algoryth_error
        return self.corners, kp
    def updateanddisplay(self):
        dst = self.update(image=self.image)
        #if self.detectortype in ("ORB", "SURF"):
          #  self.image = cv2.drawKeypoints(self.image)
        #else:
         #   self.image[dst>0.01*dst.max()] = 0
        #self.image[dst>0.01*dst.max()] = 0
        #return self.image
        return dst
class Feature_matcher():
    def __init__(self, matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)):
        self.matcher = matcher
