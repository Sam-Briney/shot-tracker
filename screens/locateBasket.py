from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.graphics.instructions import Canvas
from kivy.graphics import Rectangle, Color
from kivy.graphics.texture import Texture

import cv2

import mod.camera as cam
import mod.calibrate as calibrate

import mod.Global as Global

class LocateBasketScreen(Screen):
    def locateBasket(self, *arg):

        self.capture = cv2.VideoCapture(Global.video)

        okay, self.calImage = self.capture.read()
        self.h, self.w, channels = self.calImage.shape

        self.fps = 30
        self.loop = Clock.schedule_interval(self.update, 1.0 / self.fps)

        self.normY = -1
        self.normX = -1

    def update(self, texture):
        okay, self.image = self.capture.read()

        if okay:
            disp = self.image
            if not self.normY == -1:
                cv2.line(disp, (-10, self.normY), (self.w + 10, self.normY), (0, 255, 0))
                cv2.line(disp, (self.normX, -10), (self.normX, self.h + 10), (0, 255, 0))

            self.ids.img.texture = cam.capToTexture(disp)

    def selectBasket(self, *args):

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

            self.normX = int(transX * rawWidth / imageSize[0])
            self.normY = int(transY * rawHeight / imageSize[1])

    def cancel(self):
        Clock.unschedule(self.loop)

        self.capture.release()

        self.manager.current = "menu"

    def done(self):
        Global.hoopX = self.normX
        Global.hoopY = self.normY

        Clock.unschedule(self.loop)

        self.capture.release()

        if Global.openedCalibration:
            self.manager.current = "falsePos"
        else:
            self.manager.current = "setColor"

    pass
