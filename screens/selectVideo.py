from kivy.uix.screenmanager import Screen
import mod.Global as Global

class SelectVideoScreen(Screen):

    def load(self, path, filename):
        Global.video = filename[0]
        self.manager.current = "menu"

    def cancel(self):
        self.manager.current = "menu"
