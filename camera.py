import sys
import cv2
#import glob
import numpy as np
class Missing_calibration_data_error(Exception):
    def __init__():
        pass
class Calibrator():
    def __init__(self, image, camera_data={"pixelsize":None, "matrixsize":None, "baseline":None, "lens_distance":None}, criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001), calibrated = False):
        self.criteria = criteria
        self.objpoints = []
        self.imgpoints = []
        self.objp = np.zeros((6*7,3), np.float32)
        self.objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
        self.image = image
        self.mtx = None
        self.dist = None
        self.calibrated = calibrated
        self.pixelsize = camera_data["pixelsize"]
        self.matrixsize = camera_data["matrixsize"]
        self.baseline = camera_data["baseline"]
        self.lens_distance = camera_data["lens_distance"]
    def calibrate(self, image):
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (7,6),None)
        if ret == True:
            self.objpoints.append(self.objp)
            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),self.criteria)
            self.imgpoints.append(corners2)
            h,  w = image.shape[:2]
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
            self.mtx = mtx
            self.dist = dist
            self.calibrated = True
            return mtx, dist
    def undistort(self, image, mtx, dist):
        if dist == None or mtx == None or image == None:
            raise Missing_calibration_data_error
            h,  w = image.shape[:2]
        newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
        dst = cv2.undistort(image, mtx, dist, None, newcameramtx)
        x,y,w,h = roi
        dst = dst[y:y+h, x:x+w]
        return image
    def calculate_point_relative_position(self, point_location2d):
        angle = self.baseline/(point_location2d[left][x]-point_location2d[right][x])
        x = angle * (point_location2d[left][x]-self.matrixsize[0]/2)
        y = angle * (point_location2d[left][y]-self.matrixsize[1]/2)
        z = self.lens_distance * (1-angle/self.pixelsize)

