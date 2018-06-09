import cv2
import subprocess as sp
import numpy as np
from threading import Thread
import os
from setup import setupCamera

PIHOST = "192.168.0.111"
sshCommand = "ssh -t "

class Cam:
    def __init__(self , port , size):
        self.port = port
        self.w , self.h = size
        self.img = np.array((640, 480, 3), np.uint8)
        print(" IN :: Camera Module. Started Threading for updateFrame")

        print("Inside updateFrame")
        NETCAT_BIN = "netcat"
        ncCommand = [NETCAT_BIN,
                '-l','-p',str(self.port)] 
        nPipe = sp.Popen(ncCommand, stdout = sp.PIPE , bufsize = 10**8)
        print("Created sp pipe")
        FFMPEG_BIN = "ffmpeg"
        fCommand = [ FFMPEG_BIN,
                '-i', 'pipe:0',             # fifo is the named pipe
                '-loglevel' , 'quiet',
                '-pix_fmt', 'bgr24',      # opencv requires bgr24 pixel format.
                '-vcodec', 'rawvideo',
                '-an','-sn',              # we want to disable audio processing (there is no audio)
                '-f', 'image2pipe', '-']
        self.fPipe = sp.Popen(fCommand, stdin = nPipe.stdout , stdout = sp.PIPE, stderr=None, bufsize=11**8)
        setupCamera()

    def getFrame(self):
        if self.updateFrame() is not None:
            return self.updateFrame()

    def updateFrame(self):
        raw_image = self.fPipe.stdout.read(self.h * self.w * 3)
        image = np.fromstring(raw_image,dtype = 'uint8')
        image = image.reshape((self.h,self.w,3))
        self.fPipe.stdout.flush()
        if image is not None:
            self.img = image
            return image