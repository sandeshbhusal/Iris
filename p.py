# This is simple face-based tracking method. :) 
# Eliminate Iris to get more reliable data. :)

from pynput.mouse import Button, Controller
import requests
from module import *
import cv2
import dlib
import numpy as np
from imutils import face_utils
import math
import time

def sendKey(eyelAngle, eyerAngle, noseAngle):
    pass

mouse = Controller()
host = '192.168.0.101'
source = cv2.VideoCapture(0)
# detector = dlib.get_frontal_face_detector()
#Plug in the cv2 face detector module we made to detect face.
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
predictor = dlib.shape_predictor("landmarks.dat")
kernel = np.ones((2,2),np.uint8)
mul = 4
noseTopPosition = 0
rightEye, leftEye = np.zeros((1, 2)), np.zeros((1, 2))
faceCenter = [0, 0]
# c = Cam(5000, (640, 480))
begin = time.time()
frames_read = 0

# while c.getFrame() is None:
#     pass

while True:  
    '''  
    resp = requests.get("http://{}:8080/shot.jpg".format(host))
    jpg = resp.content
    f = cv2.imdecode(np.fromstring(jpg,dtype = np.uint8) , cv2.IMREAD_COLOR)
    '''
    ret, f = source.read()
    # f = c.getFrame()
    f = cv2.flip(f, 1)
    gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    cv2.equalizeHist(gray, gray)
    # rects = detector(gray, 1)
    # Use opencv's module to get faces, and extract rect from it. :)
    toGuess = cv2.resize(f, (160, 120))
    faces = face_cascade.detectMultiScale(toGuess)
    for (x, y, w, h) in faces:
        top = y*mul
        left = x*mul
        right = int(x+w) * mul
        bottom = int(y+h) * mul
        rect = dlib.rectangle(left, top, right, bottom)
        pt1 = (left, top)
        pt2 = (right, bottom)
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        #Pre process nose to give 'bottom' and 'top' keystrokes to the keyboard.
        # CALCULATE ROI FOR LEFT AND RIGHT EYES:
        for (name, (i, j)) in (list(face_utils.FACIAL_LANDMARKS_IDXS.items())):
            for(x, y) in shape[i:j]:
                faceCenter[0] = faceCenter[0] + x
                faceCenter[1] = faceCenter[1] + y
                cv2.circle(f, (x, y), 1, (255, 255, 255), -1)
            if name == 'nose':
                # Do something to get nose top.
                noseTopPosition = shape[i:j][0]
                noseBottomPosition = shape[i:j][3]
                noseLeftPixel = shape[i:j][4]
                noseRightPixel = shape[i:j][8]
                cv2.circle(f, tuple(noseTopPosition), 3, (255, 0, 0), 2)
                cv2.circle(f, tuple(noseBottomPosition), 3, (255, 0, 0), 2)
                cv2.line(f, tuple(noseTopPosition), tuple(noseBottomPosition), (0, 255, 0), 2)
                cv2.line(f, tuple(noseBottomPosition), tuple(noseLeftPixel), (0, 255, 2), 2)   
                cv2.line(f, tuple(noseBottomPosition), tuple(noseRightPixel), (0, 255, 2), 2)   
                
                angleLine = rightEye - leftEye
                cv2.line(f, tuple(noseTopPosition), tuple(rightEye), (255, 0, 0), 2)
                cv2.line(f, tuple(noseTopPosition), tuple(leftEye), (255, 0, 0), 2)
                angle = angleLine[1] / angleLine[0]
                print(math.degrees(math.atanh(angle)))
                distanceLeft = np.array(noseTopPosition - leftEye)
                distanceRight = np.array(noseTopPosition - rightEye)
                distanceLeft = np.sum(distanceLeft ** 2, axis = 0)
                distanceRight = np.sum(distanceRight ** 2, axis = 0)
                topBottom = np.array(noseTopPosition - noseBottomPosition)
                topBottom = np.sum(topBottom ** 2, axis = 0)
                val = (distanceLeft - distanceRight)
                x, y = mouse.position
                if abs(val) > 300:
                    if distanceLeft > distanceRight:
                        x = x + 30
                        print("Right", end=" ")
                    else:
                        x = x - 30
                        print("Left", end = " ")
                else:   
                    print("center", end = "")
                mouse.position = (x, y)
                print("Right", end=" ")
                # Calculate pointing direction based on the scaled face and nose length
                faceCenter[0] = faceCenter[0] // 68
                faceCenter[1] = faceCenter[1] // 68
                cv2.circle(f, tuple(faceCenter), 3, (255, 0, 0), 3)
                continue
            elif name == 'left_eye':
                # Do something to get left eye beginning:
                leftEye = shape[i:j][0]
                cv2.circle(f, tuple(leftEye), 3, (0, 255, 0), 2)
            elif name == 'right_eye':
                # Do something to get right eye beginning:
                rightEye = shape[i:j][3]
                cv2.circle(f, tuple(rightEye), 3, (0, 0, 255), 2)
    cv2.imshow("IMAGE", f)
    frames_read = frames_read + 1
    key = cv2.waitKey(1)
    if key & 0xFF == 27:
        break
end = time.time()

print(frames_read, " frames read in ", (end-begin), " seconds ")
print("Average FPS: ", (frames_read)/(end-begin))