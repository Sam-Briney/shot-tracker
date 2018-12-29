from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics.instructions import Canvas
from kivy.graphics import Rectangle, Color
from kivy.graphics.texture import Texture
from kivy.clock import Clock

import cv2
import numpy as np

import mod.camera as cam
import mod.calibrate as calibrate
import mod.find as find
import mod.paint as paint
import mod.getColor as getColor

import mod.Global as Global

class CalibrateColorFromFileScreen(Screen):

    def selectVideo(self):
        def setColor(self, sm, *arg):
            self.capture = cv2.VideoCapture(0)

            self.loop = Clock.schedule_interval(self.update, 1.0 / 15)

            self.tryAgain = False

        def update(self, texture):
            okay, self.image = self.capture.read()
            if okay:
                self.texture = cam.capToTexture(self.image)
                self.canvas.clear()
                with self.canvas:
                    Rectangle(texture=self.texture, pos=self.pos, size=self.size)
                    paint.message(self, "Please click on the basketball", 10, 50, 200)
                    if self.tryAgain:
                        paint.message(self, "Try clicking a more uniform area", 10,110, 200)

        def selectColor(self, *args):
            sx, sy = args[1][1].spos

            threshold = getColor.get(self.image, sx, sy, 13, True)

            if threshold == False:
                self.tryAgain = True
            else:
                self.tryAgain = False
                Clock.unschedule(self.loop)
                self.capture.release()

                Global.lower_bound = np.array(threshold[0])
                Global.upper_bound = np.array(threshold[1])

                calibrate.saveCal(self.image, threshold[0], threshold[1])

                self.manager.current = "locateBasket"
