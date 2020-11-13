import sys
import cv2
import numpy as np
class Unknown_algorythm_error(Exception):
    def __init__(self):
        pass
class No_image_passed_error(Exception):
    def __int__ (self):
        pass
class Corner_detector():
    def __init__(self, image, detectortype="Harris", corners=[]):
        self.corners = corners
        self.image = image
        self.detectortype = detectortype
    def update(self, image=None):
        gray = np.float32(cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY))
        if self.detectortype == "Harris":
            self.corners = cv2.cornerHarris(gray, 3, 3, 0, 1)
        elif self.detectortype == "Shi-Tomasi":
            self.corners = cv2.goodFeaturesToTrack(gray, 3, 3, 0, 1)
        else:
            raise Unknown_algoryth_error
        return self.corners
    def updateanddisplay(self):
        dst = self.update(image=self.image)
        self.image[dst>0.01*dst.max()] = [0, 0, 255]
        return self.image





