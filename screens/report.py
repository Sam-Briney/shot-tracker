from kivy.uix.screenmanager import Screen

import cv2
import numpy as np
import mod.camera as cam
import mod.calc as calc

import mod.Global as Global
import mod.paint as paint

class ReportScreen(Screen):

    def generate(self):

        if len(Global.shots) < 1:
            self.manager.current = 'menu'

        self.shots = []
        self.angles = []
        self.maxHeights = []
        Global.shotFits = []

        shots_filtered_raw = calc.filterRaw(Global.shots)

        for shot in shots_filtered_raw:
            try:
                self.shots.append([calc.curveFit(shot, "x"), calc.curveFit(shot, "t")])
            except:
                pass

        self.shots = calc.filterShots(self.shots, shots_filtered_raw)

        Global.shotsFiltered = self.shots

        if Global.mapped:
            dispShots = []

            for i in range(0, len(self.shots)):
                shot = self.shots[i]
                if Global.map[i] == 1:
                    dispShots.append(shot)

            self.shots = dispShots

        self.ids.shotsTaken.text = str(len(self.shots)) + "/" + str(len(Global.shots))

        for shot in self.shots:
            theta = calc.angle(shot[0])
            self.angles.append(theta)
            maxHeight = calc.maxHeight(shot[0])
            self.maxHeights.append(maxHeight)

        std = np.std(self.angles)
        average = np.mean(self.angles)
        median = np.median(self.angles)


        self.ids.stdAngle.text = str(round(std, 2))
        self.ids.averageAngle.text = str(round(average, 2))
        self.ids.medianAngle.text = str(round(median, 2))

        # generate image
        try:
            self.image = Global.reportImage.copy()
        except:
            pass

        self.image = paint.shotsImage(self.shots, self.image)

        pixelToFeetList = []

        for shot in self.shots:
            a = shot[1][0]
            pixelToFeetList.append(abs(32.2 / (2 * a)))

        pixelToFeet = np.median(pixelToFeetList)

        Global.pixelToFeet = pixelToFeet

        endXs = []
        for shot in self.shots:
            a = shot[0][0]
            b = shot[0][1]
            c = shot[0][2]

            #avoid imaginary numbers
            if (b**2 - 4 * a * c) >= 0:
                x01 = (-1 * b - (b**2 - 4 * a * c)**(0.5))/(2 * a)
                x02 = (-1 * b + (b**2 - 4 * a * c)**(0.5))/(2 * a)
                x0 = 0

                # on left
                if Global.basketOn == 1:
                    if x01 < x02:
                        x0 = x01
                    else:
                        x0 = x02
                else:
                    if x01 < x02:
                        x0 = x02
                    else:
                        x0 = x01

                endXs.append(x0)


        distStd = np.std(endXs)

        distStdIn = distStd * pixelToFeet * 12

        self.ids.distStd.text = str(round(distStdIn, 2)) + " In"

        # Dx = v0 t + 1/2 a t^2
        # V^2 = v0^2 + 2 a Dx
        try:
            self.ids.traceImage.texture = cam.capToTexture(self.image)
        except:
            pass

        Global.shotFits = self.shots
        Global.angles = self.angles

        Global.stdAngle = std
        Global.averageAngle = average
        Global.medianAngle = median

        Global.averageMaxHeight = np.mean(self.maxHeights)
        Global.stdMaxHeight = np.std(self.maxHeights)
        Global.medianMaxHeight = np.median(self.maxHeights)

        Global.maxHeights = self.maxHeights
