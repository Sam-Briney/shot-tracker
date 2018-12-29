import time
import numpy as  np
from playsound import playsound

from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.graphics.instructions import Canvas
from kivy.graphics import Rectangle, Color
from kivy.graphics.texture import Texture

import cv2

import mod.find as find
import mod.camera as cam
import mod.calibrate as calibrate
import mod.paint as paint
import mod.calc as calc

import mod.Global as Global

class TrackShotsScreen(Screen):
    def trackShots(self, *arg):
        self.audio = True
        if self.ids.audio.state == "normal":
            self.audio = False

        self.curve = [0,0,-10]

        self.capture = cv2.VideoCapture(Global.video)

        Global.fps = self.capture.get(cv2.CAP_PROP_FPS)

        Global.mapped = False
        Global.shots = []
        Global.shotsFiltered = []

        okay, image = self.capture.read()
        if okay:
            self.h, self.w, channels = image.shape

        Global.videoH = self.h

        self.loop = Clock.schedule_interval(self.update, 1.0 / 40)

        #distance to switch shots (normalized and squared so the root does not have to be taken)
        self.shot_distance = (100 * self.w / 1080)**2

        scaleToWin = (self.width/self.w, self.height/self.h)

        self.shot = []

        self.tracking = False

        #approx size of bball
        self.radius = 15

        self.basketOn = 1 #1=left

        if Global.hoopX > self.w / 2:
            self.basketOn = -1 #-1=right

        Global.basketOn = self.basketOn
        # print self.basketOn

        self.newShotThreshold = Global.hoopX + (200 * self.w / 1280) * self.basketOn

        self.displayAngleThreshold = 0.75 #seconds

        self.last_midPoint = (-1, -1)

        self.wait_for_angle = True

        # MIL, BOOSTING, KCF, TLD, MEDIANFLOW or GOTURN
        #self.algorithm = "MEDIANFLOW"
        self.tracker = cv2.TrackerMedianFlow_create()

        self.last3 = []

        self.reportImage = False

        self.frame = 0

        self.time = 0


    def update(self, texture):
        self.ids.numShots.text = "Shots: " + str(len(Global.shots))

        okay, self.image = self.capture.read()

        self.useMid = False

        midPoint = False
        if okay:
            self.frame += 1

            for fp in Global.deadPoints:
                cv2.rectangle(self.image, (fp[0] - Global.deadPointRad, fp[1] - Global.deadPointRad), (fp[0] + Global.deadPointRad, fp[1] + Global.deadPointRad), (0, 0, 0), 10)
            if self.tracking:
                #look for point using tracker
                ok, bbox = self.tracker.update(self.image)

                #reset tracker point
                trackerPoint = (-1, -1)

                #look for point using color calibration
                point = find.search(self.image[0:Global.hoopY, 0:self.w], Global.lower_bound, Global.upper_bound)

                if ok:
                    #find midpoint of tracker box
                    p1 = (int(bbox[0]), int(bbox[1]))
                    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                    midPoint = (int((p1[0] + p2[0])/2), int((p1[1] + p2[1])/2))

                    #create range for color calibration point
                    pf1 = (int(point[0] - self.radius), int(point[1] - self.radius))
                    pf2 = (int(point[0] + self.radius), int(point[1] + self.radius))
                    pfDiameter = self.radius * 2

                    #if conflict between two points
                    if not point == (-1, -1) and (point[0] < p1[0] or point[0] > p2[0] or point[1] < p1[1] or point[1] > p2[1]):
                        #if tracker stuck or less than 3 points reset tracker and use color point
                        if len(self.last3) < 3 or midPoint == self.last_midPoint:
                            cv2.rectangle(self.image, pf1, pf2, (255,0,0))
                            del self.tracker
                            self.tracker = cv2.TrackerMedianFlow_create()
                            self.tracker.init(self.image, (pf1[0], pf1[1], pfDiameter, pfDiameter))
                            midPoint = (-1, -1)
                            self.useMid = False
                        else:
                            #check distance between last two points
                            dist01sq = (self.last3[0][0] - self.last3[1][0])**2 + (self.last3[0][1] - self.last3[1][1])**2
                            dist12sq = (self.last3[1][0] - self.last3[2][0])**2 + (self.last3[1][1] - self.last3[2][1])**2
                            #if distance "small enough" use a line to project the next point
                            if dist01sq < 30**2:
                                # line: y = m(x-h) + k
                                # y = (self.last3[0][1] - self.last3[1][1])/(self.last3[0][0] - self.last3[1][0]) * (point[0] - self.last3[0][0]) + self.last3[0][1]
                                try:
                                    yP = (self.last3[0][1] - self.last3[1][1])/(self.last3[0][0] - self.last3[1][0]) * (point[0] - self.last3[1][0]) + self.last3[1][1]
                                    yMid = (self.last3[0][1] - self.last3[1][1])/(self.last3[0][0] - self.last3[1][0]) * (midPoint[0] - self.last3[1][0]) + self.last3[1][1]

                                    distYP = abs(yP - point[1])
                                    distYMid = abs(yMid - midPoint[1])

                                    #if projection is close to tracker point use the tracker instead of the color
                                    if distYMid < distYP:
                                        self.useMid = True
                                except:
                                    self.useMid = self.useMid

                    #store midpoint to check for sticking points
                    self.last_midPoint = midPoint
            else:
                #else not trakcing yet: initialize tracker using color point
                point = find.search(self.image[0:Global.hoopY, 0:self.w], Global.lower_bound, Global.upper_bound)
                if not point == (-1, -1):
                    self.tracking = True
                    self.tracker.init(self.image, (int(point[0] - self.radius), self.radius * 2, int(point[1] - self.radius), self.radius * 2))
                    if not self.reportImage:
                        Global.reportImage = self.image.copy()
                        self.reportImage = True

            #if there is a point, log it
            if (not point == (-1, -1) and not self.useMid) or midPoint:
                if point == (-1, -1):
                    point = midPoint
                if point[1] < Global.hoopY:
                    try:
                        if not (point == self.last3[2]):
                            self.time = videoTime(self.capture)
                    except:
                        self.time = videoTime(self.capture)

                    #draw circle on the ball, and append point or midPoint to self.shot
                    cv2.circle(self.image, point, 7, (0,0,255), 7)
                    self.shot.append([point, self.time])
                    self.last3.insert(0, point)
                    if len(self.last3) > 3:
                        self.last3.pop()

            items = len(self.shot) - 1

            #if more than one point
            if items > 1:
                #if starting from the shooter when previous point was at basket, initialize new shot
                if (self.shot[items - 1][0][0] < self.newShotThreshold and self.shot[items][0][0] > self.newShotThreshold and self.basketOn == 1) or (self.shot[items - 1][0][0] > self.newShotThreshold and self.shot[items][0][0] < self.newShotThreshold and self.basketOn == -1):
                    toAdd = self.shot[items][0]
                    self.frame = 0
                    self.shot = [[toAdd, self.time]]

                    self.wait_for_angle = True
                #if going backwards delete point
                elif self.shot[items - 1][0] * self.basketOn < self.shot[items][0] * self.basketOn:
                    self.shot.pop()
                    self.last3.pop()

                #if shot initialized and passed cuttoff time - save shot to Global
                if self.wait_for_angle and self.time > 0 and (videoTime(self.capture) > self.time + self.displayAngleThreshold):
                    #reset time to avoid double logging shots
                    self.time = 0

                    try:
                        #fit parabola and calculate angle
                        z = calc.curveFit(self.shot, "x")
                        theta = int(round(calc.angle(z)))
                        print "theta = " + str(theta)
                        self.ids.lastAngle.text = "Last Angle = " + str(theta) + " degrees"

                        #play sound
                        if self.audio == True:
                            if theta > 60:
                                playsound("audio/ABOVE.wav", False)
                            elif theta < 35:
                                playsound("audio/BELOW.wav", False)
                            else:
                                playsound("audio/numbers/" + str(theta) + ".wav", False)

                        z[0] = z[0] * -1
                        z[1] = z[1] * -1
                        z[2] = z[2] * -1 + Global.hoopY
                        self.curve = z
                        Global.shots.append(self.shot)
                        self.wait_for_angle = False
                    except:
                        #if having trouble curve fitting, discard shot and start over
                        print "error trackshots.py ln 201"
                        self.shot = []
                        self.last3 = []


            #draw green line of raw data
            for i in range(1, len(self.shot) - 1):
                cv2.line(self.image, self.shot[i-1][0], self.shot[i][0], (0, 255, 0))

            try:
                if len(self.shot) > 1:
                    x0 = (-1 * self.curve[1] - ((self.curve[1] ** 2) - 4 * self.curve[0] * (self.curve[2] - Global.hoopY))**(0.5)) / (2 * self.curve[0])
                    x1 = (-1 * self.curve[1] + ((self.curve[1] ** 2) - 4 * self.curve[0] * (self.curve[2] - Global.hoopY))**(0.5)) / (2 * self.curve[0])
                    xlin = np.linspace(x0, x1, num=100)
                    for i in range(1, 100):
                        #draw blue line of curve fit
                        cv2.line(self.image, (int(xlin[i-1]), int(self.curve[0] * xlin[i-1] ** 2 + self.curve[1] * xlin[i-1] + self.curve[2])), (int(xlin[i]), int(self.curve[0] * xlin[i] ** 2 + self.curve[1] * xlin[i] + self.curve[2])), (255, 0, 0))
                else:
                    #if no shot, replace curve with a line outside visible area
                    self.curve = [0,0,-10]
            except:
                pass

        else:
            self.manager.current = "menu"

        if okay:
            #show grid of basketheight
            height, width, channels = self.image.shape
            cv2.line(self.image, (-10, Global.hoopY), (width + 10, Global.hoopY), (0, 255, 0))
            cv2.line(self.image, (self.newShotThreshold, -10), (self.newShotThreshold, height+10), (0, 255, 0))
            self.ids.img.texture = cam.capToTexture(self.image)

    #add false positives on the fly
    def remPoint(self, *args):
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
                Global.deadPoints.append((normX, normY))

    def smooth(self, y):
        rft = np.fft.rfft(y)
        rft[5:] = 0
        y_smooth = np.fft.irfft(rft)
        return y_smooth

    def deleteLast(self):
        self.shot = []

    def submit(self):
        Clock.unschedule(self.loop)
        self.capture.release()
        Global.openedCalibration = False
        self.manager.current = "report"

    def dist2(self, p1, p2):
        return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

    def falsePos(self, point):
        for fp in Global.deadPoints:
            if self.dist2(point, fp) < 5**2:
                return True
        return False

    def toggleAudio(self, widget, value):
        if value[1] == 'down':
            self.audio = True
        else:
            self.audio = False

#get actual frame time from video capture
def videoTime(capture):
    return capture.get(cv2.CAP_PROP_POS_MSEC) / 1000
