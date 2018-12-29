from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
import json
import os

import numpy as np

import mod.Global as Global

class OpenCalibrationScreen(Screen):

    def callBack(self, instance):
        f = open("color-calibrations/files/" + instance.text, "r")
        data = json.loads(f.read())
        f.close()

        Global.lower_bound = np.array(data['lower_bound'])
        Global.upper_bound = np.array(data['upper_bound'])
        Global.openedCalibration = True

        self.manager.current = "locateBasket"

    def listCalibrations(self, *arg):
        files = os.listdir("color-calibrations/files")

        layout = GridLayout(cols=1, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        for f in files:
            layout.add_widget(Button(text=f, size_hint_y=None, height=30, on_press=self.callBack))

        self.ids.sv.clear_widgets()
        self.ids.sv.add_widget(layout)
