from kivy.uix.screenmanager import Screen

import mod.Global as Global
class SetInputScreen(Screen):
    def setInputWebCam(self):
        self.manager.current = "selectCam"
