import cv2
import sys
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
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
if True:
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[7]

    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        if tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()
    video = cv2.VideoCapture(0)
    if not video.isOpened():
        print ("Could not open video")
        sys.exit()
    ok, frame = video.read()
    if not ok:
        print ('Cannot read video file')
        sys.exit()
    bbox = cv2.selectROI(frame, False)
    ok = tracker.init(frame, bbox)
    while True:
        ok, frame = video.read()
        if not ok:
            break
        timer = cv2.getTickCount()
        ok, bbox = tracker.update(frame)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        corn = Corner_detector(frame)
        dst = corn.update()
        frame[dst>0.01*dst.max()] = [0, 0, 255] 
        if ok:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else :
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
        cv2.imshow("Tracking", frame)
        k = cv2.waitKey(1) & 0xff
        if k == 27 :
            break
