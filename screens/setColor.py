from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics.instructions import Canvas
from kivy.graphics import Rectangle, Color
from kivy.graphics.texture import Texture
from kivy.clock import Clock

import numpy as np
import cv2

import mod.camera as cam
import mod.calibrate as calibrate
import mod.find as find
import mod.paint as paint
import mod.getColor as getColor

import mod.Global as Global


class SetColorScreen(Screen):
    def updateInputs(self):
        self.ids.radius.text = str(self.radius)
        self.ids.std.text = str(self.std[0]) + ", " + str(self.std[1]) + ", " + str(self.std[2])


    def setColor(self):
        self.capture = cv2.VideoCapture(Global.video)

        okay, self.calImage = self.capture.read()
        self.h, self.w, channels = self.calImage.shape

        self.fps = 30
        self.loop = Clock.schedule_interval(self.update, 1.0 / self.fps)

        self.h = 15
        self.s = 150
        self.v = 175

        self.radius = 5

        self.std = [3,50,25]

        self.updateInputs()

        self.playing = True

        self.sampleImages = []

        self.filter = False

        self.bounds = [np.array(Global.lower_bound), np.array(Global.upper_bound)]

        getColor.resetSamples()


    def update(self, *texture):
        okay, self.image = self.capture.read()
        if not getColor.sensitivity == self.ids.sensitivity.value_normalized:
            getColor.sensitivity = self.ids.sensitivity.value_normalized
            bounds = getColor.get(self.sampleImages)
            self.bounds = [np.array(bounds[0]), np.array(bounds[1])]

        if okay:
            coord = find.search(self.image[0:Global.hoopY, 0:self.w], self.bounds[0], self.bounds[1])

            if self.filter:
                self.image = find.filter(self.image, self.bounds[0], self.bounds[1])

            if not coord == (-1, -1):
                disp = self.image.copy()
                cv2.circle(disp, coord, 7, (0, 0, 255), 5)
                self.ids.img.texture = cam.capToTexture(disp)
            else:
                self.ids.img.texture = cam.capToTexture(self.image)
            try:
                self.radius = int(self.ids.radius.text)
            except:
                pass

    def selectColor(self, *args):

        absX = args[0].last_touch.px
        absY = args[0].last_touch.py

        totalWidth = args[0].width
        totalHeight = args[0].height

        imageSize = args[0].get_norm_image_size()

        trueImgX = (totalWidth - imageSize[0]) / 2
        trueImgY = (totalHeight - imageSize[1]) / 2

        self.radius = int(self.ids.radius.text)

        # if inside displayed image + radius
        if absX > trueImgX + self.radius and absX < trueImgX + imageSize[0] - self.radius and absY > trueImgY + self.radius and absY < trueImgY + imageSize[1] - self.radius:
            rawHeight, rawWidth, channels = self.image.shape
            transX = (absX - trueImgX) #* rawWidth / imageSize[0]ent
            transY = (absY - trueImgY) #* rawHeight / imageSize[1]ent
            transY = imageSize[1] - transY

            normX = int(transX * rawWidth / imageSize[0])
            normY = int(transY * rawHeight / imageSize[1])

            normRadius = int(float(self.radius) * rawWidth/640)

            if normY - normRadius < Global.hoopY:
                blur = cv2.GaussianBlur(self.image, (5,5),0)

                sample = getColor.addSample(self.image, normX, normY, normRadius)

                self.ids.samples.text = str(getColor.samples)

                self.median = sample[0]
                self.std = sample[1]

                self.h = self.median[0]
                self.s = self.median[1]
                self.v = self.median[2]

                self.sampleImages.append([cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)[0:Global.hoopY, 0:rawWidth], normX, normY])

                self.calImage = self.image.copy()

                cv2.circle(self.calImage, (normX, normY), normRadius, (0, 255, 0))
                self.ids.img.texture = cam.capToTexture(self.calImage)
                if self.playing:
                    self.playPause()

                self.updateInputs()

                bounds = getColor.get(self.sampleImages)
                self.bounds = [np.array(bounds[0]), np.array(bounds[1])]


    def cancel(self):
        Clock.unschedule(self.loop)
        self.capture.release()
        self.manager.current = "menu"

    def toggleFilter(self):
        if self.filter:
            self.filter = False
        else:
            self.filter = True

    def playPause(self):
        if self.playing:
            Clock.unschedule(self.loop)
            self.playing = False
            if Global.video == 0:
                self.capture.release()
        else:
            self.loop = Clock.schedule_interval(self.update, 1.0 / self.fps)
            self.playing = True
            if Global.video == 0:
                self.capture = cv2.VideoCapture(Global.video)

    def save(self):
        Clock.unschedule(self.loop)
        self.capture.release()

        bounds = getColor.get(self.sampleImages)

        Global.lower_bound = np.array(bounds[0])
        Global.upper_bound = np.array(bounds[1])

        self.manager.current = "saveCal"
