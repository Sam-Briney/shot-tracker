from kivy.uix.label import Label
from kivy.graphics.instructions import Canvas
from kivy.graphics import Rectangle, Color

import mod.Global as Global

import cv2
import numpy as np

def message(s, message, xPos, yPos, width):
    Color(0, 0, 0, 0.25)
    Rectangle(pos=(0, s.height-yPos), size=(220, 50))
    label = Label(text=message, halign="left", valign="middle", pos=(xPos, s.height-yPos), size=(width, 50))

def shotsImage(shots, image):
    for shot in shots:
        a = shot[0][0]
        b = shot[0][1]
        c = shot[0][2]

        #avoid imaginary numbers
        if (b**2 - 4 * a * c) >= 0:
            x01 = (-1 * b - (b**2 - 4 * a * c)**(0.5))/(2 * a)
            x02 = (-1 * b + (b**2 - 4 * a * c)**(0.5))/(2 * a)

            xlin = np.linspace(x01, x02, 100)

            points = []

            try:
                for x in xlin:
                    y = Global.hoopY - (a * x**2 + b * x + c)
                    points.append((int(x), int(y)))

                for i in range(1, len(xlin) - 1):
                    cv2.line(image, points[i-1], points[i], (0, 255, 0))
            except:
                pass

    return image
