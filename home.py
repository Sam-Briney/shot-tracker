import os
#make sure WebCam light turns off
os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0"

import cv2
import numpy as np

import mod.find as find
import mod.camera as cam
import mod.calibrate as calibrate

import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics.instructions import Canvas
from kivy.graphics import Rectangle, Color
from kivy.graphics.texture import Texture
from kivy.clock import Clock

from mod.cls import IconButton


from screens.saveCal import SaveCalScreen
from screens.setColor import SetColorScreen
from screens.locateBasket import LocateBasketScreen
from screens.trackShots import TrackShotsScreen
from screens.openCalibration import OpenCalibrationScreen
from screens.calibrateColorFromFile import CalibrateColorFromFileScreen
from screens.selectVideo import SelectVideoScreen
from screens.selectCam import SelectCamScreen
from screens.setInput import SetInputScreen
from screens.falsePos import FalsePosScreen
from screens.report import ReportScreen
from screens.saveData import SaveDataScreen
from screens.editResults import EditResultsScreen
#from kivy.graphics.instructions.InstructionGroup import InstructionGroup

# Inherit Kivy's App class which represents the window
# for our widgets
# HelloKivy inherits all the fields and methods
# from Kivy

class MenuScreen(Screen):
    pass

class ShotCounterApp(App):
    # This returns the content we want in the window
    def build(self):
        pass


shotCounter = ShotCounterApp()
shotCounter.run()
