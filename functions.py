from constants import *
import cv2
import dlib
from cameraModule import *
from setup import setupCamera
from pynput.mouse import Button, Controller
import numpy as np
from imutils import face_utils
from threading import Thread
import math
import time

beginTime = time.time()
dblTime   = time.time()
prevCursor = [0, 0]
class ImageProcessor:
    def __init__(self):
        print("--- Creating the image processor => ImageProcessor.__init__ ---")
        # Setup the face cascade, camera and predictor.
        # Also block the stream until image is not read
        print(" Setting up camera receiving server.")
        self.cam = Cam(PI_PORT, (IMAGE_WIDTH, IMAGE_HEIGHT))
        print(" Setting up PI to pipe data.")
        Thread(target=setupCamera()).start()
        self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.predictor = dlib.shape_predictor("landmarks.dat")
        print(" Please wait while the camera warms up...")
        self.readFrames()

    def readFrames(self):
        # This function returns the facial features, as a tuple to another function
        # for further processing. The function plots the tuples and makes the required mouse/
        # keyboard movements as requirement.
        while True:
            key = cv2.waitKey(1)
            if key & 0xff == 27:
                break
            f = self.cam.getFrame()
            f = cv2.flip(f, 1)
            gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
            cv2.equalizeHist(gray, gray)
            toGuess = cv2.resize(f, (160, 120))
            faces = self.face_cascade.detectMultiScale(toGuess)
            mul = 4
            for (x, y, w, h) in faces:
                top = y*mul
                left = x*mul
                right = int(x+w) * mul
                bottom = int(y+h) * mul
                rect = dlib.rectangle(left, top, right, bottom)
                shape = self.predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)
                for (name, (i, j)) in (list(face_utils.FACIAL_LANDMARKS_IDXS.items())):
                    for (x, y) in shape[i:j]:
                        cv2.circle(f, (x, y), 1, (255, 0, 0), -1)
                    if name == 'nose':
                        noseTopPosition = shape[i:j][0]
                        noseBottomPosition = shape[i:j][3]
                        noseLeftPixel = shape[i:j][4]
                        noseRightPixel = shape[i:j][8]

                    elif name == 'left_eye':
                        leftEye = shape[i:j][0]
                    
                    elif name == 'right_eye':
                        rightEye = shape[i:j][3]
                toReturn = (left, top, w, h, leftEye, rightEye, noseTopPosition, noseBottomPosition, noseLeftPixel, noseRightPixel)
                if MODE != "CONFIG":
                    processor = ProcessUI(f, toReturn)
                cv2.imshow("Image", f)
                break   #Currently work on only one face. :)
                
class ProcessUI:
    def __init__(self, image, faceCoordinates):
        (left, top, w, h, leftEye, rightEye, noseTopPosition, noseBottomPosition, noseLeftPixel, noseRightPixel) = faceCoordinates

        cv2.circle(image, (left, top), 3, (0, 255, 0), 4)
        for (x,y) in faceCoordinates[4:]:
            cv2.circle(image, (x,y), 2, (255, 0,  0), 3)
        cv2.imshow("Image 2", image)
        mouse = Controller()
        # This function gets the facial coordinates, and the input image, and makes the necessary calculations.
        distanceLeft = np.array(noseTopPosition - leftEye)
        unitLeft = distanceLeft
        distanceRight = np.array(noseTopPosition - rightEye)
        unitRight = distanceRight
        distanceLeft = np.sum(distanceLeft ** 2, axis = 0)
        distanceRight = np.sum(distanceRight ** 2, axis = 0)
        unitLeft = unitLeft / distanceLeft ** 0.5
        unitRight = unitRight / distanceRight ** 0.5
        angle = np.dot(unitLeft, unitRight)
        angle = math.degrees(math.acos(angle))
        angle = ( angle // 2 ) * 10
        topBottom = np.array(noseTopPosition - noseBottomPosition)
        topBottom = (np.sum(topBottom ** 2, axis = 0)) ** 0.5
        # Face top/bottom tracking using angle.

        faceRatio = topBottom / h
        val = (distanceLeft - distanceRight)
        global prevCursor, beginTime, dblTime
        x, y = mouse.position
        if (x,y)==prevCursor:
            if (time.time() - beginTime) > 2:
                mouse.press(Button.left)
                mouse.release(Button.left)
                print("Click event occured")
                beginTime = time.time()

            if(time.time() - dblTime) > 4:
                mouse.click(Button.left, 2)
                print("Double click event occured")
                dblTime = time.time()
        else:
            beginTime = time.time()
            dblTime = time.time()
            prevCursor=mouse.position

        print(mouse.position)

        if abs(val) > 300:
            if distanceLeft > distanceRight: #Facing right
                x = x + 7
            else:
                x = x - 7  # Facing left
        
        if angle not in range(760, 840):
            if angle <= 760:
                y = y - 4
            else:
                y = y + 4

        mouse.position = x, y
class faceConstants:
    def __init__(self):
        pass