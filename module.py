import cv2
import subprocess as sp
import numpy as np
from threading import Thread
import os

PIHOST = "192.168.0.104"

sshCommand = "ssh -t "


class Cam:
    def __init__(self , port , size):
        self.port = port
        self.w , self.h = size
        self.img = None
        Thread(target = self.updateFrame).start()
    
    def getFrame(self):
        return self.img

    def updateFrame(self):
       NETCAT_BIN = "netcat"
       ncCommand = [NETCAT_BIN,
               '-l','-p',str(self.port)] 
       nPipe = sp.Popen(ncCommand, stdout = sp.PIPE , bufsize = 10**8)
       
       FFMPEG_BIN = "ffmpeg"
       fCommand = [ FFMPEG_BIN,
               '-i', 'pipe:0',             # fifo is the named pipe
               '-loglevel' , 'quiet',
               '-pix_fmt', 'bgr24',      # opencv requires bgr24 pixel format.
               '-vcodec', 'rawvideo',
               '-an','-sn',              # we want to disable audio processing (there is no audio)
               '-f', 'image2pipe', '-']
       fPipe = sp.Popen(fCommand, stdin = nPipe.stdout , stdout = sp.PIPE, stderr=None, bufsize=11**8)
       while True:
           raw_image = fPipe.stdout.read(self.h * self.w * 3)
           image = np.fromstring(raw_image,dtype = 'uint8')
           image = image.reshape((self.h,self.w,3))
           if image is not None:
               self.img = image
           fPipe.stdout.flush()
