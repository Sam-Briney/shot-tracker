from kivy.uix.screenmanager import Screen

import mod.Global as Global

import numpy as np

import os

class SaveDataScreen(Screen):
    def save(self, path, fname):

        self.shotFits = []

        self.combo = []

        self.data = []

        for shot in Global.shotFits:
            self.shotFits.append(np.array([shot[0].tolist(), shot[1].tolist()]).flatten().tolist())

        for i in range(len(self.shotFits)):
            self.combo.append([self.shotFits[i], Global.angles[i], Global.maxHeights[i] * Global.pixelToFeet])

        for elem in self.combo:
            self.data.append([elem[0][0], elem[0][1], elem[0][2], elem[0][3], elem[0][4], elem[0][5], elem[1], elem[2]])

        self.strFile = "Model:,Ax^2+Bx+C,,Model:,At^2+Bt+c,,,\ny (pixels) v. x (pixels),,,y (pixels) v. t (seconds),,,,\nA,B,C,A,B,C,Angle (Degrees),Max Height (Ft.)"

        for data in self.data:
            self.strFile = self.strFile + "\n"
            for elem in data:
                self.strFile = self.strFile + str('{:.20f}'.format(elem)) + ","
            self.strFile = self.strFile[:-1]

        self.strFile = self.strFile + "\n,,,,,,,\nAngle Mean:," + str(Global.averageAngle) + ",Angle Median:," + str(Global.medianAngle) + ",Angle St. Dev.:," + str(Global.stdAngle) + ",,"
        self.strFile = self.strFile + "\n1 foot =," + str(1 / Global.pixelToFeet) + " pixels,,,,,,"

        try:
            f = open(path + "/" + fname + ".csv", "w")

            f.write(self.strFile)

            f.close()
            self.manager.current = "report"
        except:
            self.manager.current = "report"
            pass
