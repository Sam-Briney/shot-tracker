from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image

import cv2

import mod.Global as Global
import mod.camera as cam
class SelectCamScreen(Screen):
    def callBack(self, instance):
        cam_index = int(instance.text[-1:])

        Global.video = cam_index
        self.manager.current = "menu"

    def listCameras(self):
        continue_checking = True
        cams = []
        images = []


        i = 0
        while continue_checking:
            self.capture = cv2.VideoCapture(i)
            okay, img = self.capture.read()

            if okay:
                cams.append(i)
                images.append(cam.capToTexture(img))
            else:
                continue_checking = False

            self.capture.release()

            i += 1

        layout = GridLayout(cols=1, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        for i in range(0, len(cams)):
            img = Image(texture=images[i])
            but = Button(text="Camera " + str(cams[i]), on_press=self.callBack)

            bLayout = BoxLayout(orientation="horizontal", size_hint_y=None, height=200)

            bLayout.add_widget(but)
            bLayout.add_widget(img)

            layout.add_widget(bLayout)

        self.ids.sv.clear_widgets()
        self.ids.sv.add_widget(layout)

    def cancel(self):
        self.manager.current = "menu"
