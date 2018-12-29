from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.togglebutton import ToggleButton

import mod.Global as Global

import mod.calc as calc
import mod.paint as paint
import mod.camera as cam

class EditResultsScreen(Screen):

    def editResults(self, *arg):

        self.shots = Global.shotsFiltered

        if Global.mapped == False:
            self.map = []
            for shot in self.shots:
                self.map.append(1)
        else:
            self.map = Global.map

        self.ids.tableAngles.clear_widgets()

        self.ids.tableAngles.rows = len(self.shots)

        for i in range(0, len(self.shots)):
            st = "down"
            if Global.mapped:
                if self.map[i] == 0:
                    st = "normal"

            shot = self.shots[i]
            theta = round(calc.angle(shot[0]))
            tog = ToggleButton(text=str(theta), state=st, group=str(i), height=40, size_hint_y=None)
            tog.bind(state=self.toggleShot)

            self.ids.tableAngles.add_widget(tog)

        self.refreshImage()

    def toggleShot(self, widget, value):
        index = int(float(widget.group))
        self.map[index] = 1
        if value == "normal":
            self.map[index] = 0

        self.refreshImage()

    def refreshImage(self):
        # generate image
        try:
            self.image = Global.reportImage.copy()
        except:
            pass

        dispShots = []

        for i in range(0, len(self.shots)):
            shot = self.shots[i]

            if self.map[i] == 1:
                dispShots.append(shot)

        self.image = paint.shotsImage(dispShots, self.image)

        try:
            self.ids.img.texture = cam.capToTexture(self.image)
        except:
            pass

    def done(self):
        Global.mapped = True
        Global.map = self.map
        self.manager.current = "report"

    def cancel(self):
        self.manager.current = "report"
