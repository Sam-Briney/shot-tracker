from kivy.uix.screenmanager import Screen
import mod.Global as Global

import numpy as np

import json
from random import randint
import os
import os.path
import cv2

class SaveCalScreen(Screen):
    def list(self):
        files = os.listdir("color-calibrations/files")
        self.ids.list.item_strings = files

    def save(self):
        lb = Global.lower_bound.tolist()
        ub = Global.upper_bound.tolist()

        data = {"lower_bound": lb, "upper_bound": ub}

        f = open("color-calibrations/files/" + self.ids.fName.text + ".json", "w")
        f.write(json.dumps(data))
        f.close()

        self.manager.current = "falsePos"


    def cancel(self):
        self.manager.current = "falsePos"
