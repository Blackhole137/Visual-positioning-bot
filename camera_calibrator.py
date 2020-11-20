import sys
import cv2
#import glob
import numpy as np
class Calibrator():
	def __init__(self, image, criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)):
		self.criteria = criteria
		self.objpoints = []
		self.imgpoints = []
		self.objp = np.zeros((6*7,3), np.float32)
		self.objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
		self.image = image
		self.mtx = None
		self.dist = None
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
			return mtx, dist
	def undistort(self, image, mtx, dist):		
		h,  w = image.shape[:2]
		newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
		dst = cv2.undistort(image, mtx, dist, None, newcameramtx)
		x,y,w,h = roi
		dst = dst[y:y+h, x:x+w]
		return image