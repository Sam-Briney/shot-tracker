from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.graphics.instructions import Canvas
from kivy.graphics import Rectangle, Color
from kivy.graphics.texture import Texture

import cv2
import numpy as np

import mod.Global as Global

import mod.camera as cam
import mod.find as find

# loop through moments in getColor to find all false positives

class FalsePosScreen(Screen):

    def findSpots(self):
        self.capture = cv2.VideoCapture(Global.video)

        okay, self.calImage = self.capture.read()
        self.h, self.w, channels = self.calImage.shape

        self.fps = 30
        self.loop = Clock.schedule_interval(self.update, 1.0 / self.fps)

        self.falsePos = []

    def update(self, *texture):
        okay, self.image = self.capture.read()
        
        if okay:
            disp = find.filter(self.image, Global.lower_bound, Global.upper_bound)
            cv2.line(disp, (-10, Global.hoopY), (self.w + 10, Global.hoopY), (0, 255, 0))

            for fp in self.falsePos:
                cv2.rectangle(self.image, (fp[0] - Global.deadPointRad, fp[1] - Global.deadPointRad), (fp[0] + Global.deadPointRad, fp[1] + Global.deadPointRad), (0, 255, 0), 10)
                cv2.rectangle(disp, (fp[0] - Global.deadPointRad, fp[1] - Global.deadPointRad), (fp[0] + Global.deadPointRad, fp[1] + Global.deadPointRad), (0, 255, 0), 10)

            coord = find.search(self.image[0:Global.hoopY, 0:self.w], Global.lower_bound, Global.upper_bound)
            if not coord == (-1, -1):
                cv2.circle(disp, coord, 5, (255, 0, 0), 5)
            self.ids.img.texture = cam.capToTexture(disp)

    def deadSpot(self, *args):
        absX = args[0].last_touch.px
        absY = args[0].last_touch.py

        totalWidth = args[0].width
        totalHeight = args[0].height

        imageSize = args[0].get_norm_image_size()

        trueImgX = (totalWidth - imageSize[0]) / 2
        trueImgY = (totalHeight - imageSize[1]) / 2

        # if inside displayed image
        if absX > trueImgX and absX < trueImgX + imageSize[0] and absY > trueImgY and absY < trueImgY + imageSize[1]:
            rawHeight, rawWidth, channels = self.image.shape
            transX = (absX - trueImgX) #* rawWidth / imageSize[0]ent
            transY = (absY - trueImgY) #* rawHeight / imageSize[1]ent
            transY = imageSize[1] - transY

            normX = int(transX * rawWidth / imageSize[0])
            normY = int(transY * rawHeight / imageSize[1])

            if normY < Global.hoopY:
                self.falsePos.append((normX, normY))

    def done(self):
        Global.deadPoints = self.falsePos
        self.capture.release();

        self.manager.current = "trackShots"

    def cancel(self):
        self.falsePos = []
        self.manager.current = "menu"
