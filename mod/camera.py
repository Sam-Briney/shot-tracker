import cv2
import numpy as np
from kivy.graphics.texture import Texture

def capToTexture(frame, fmt='bgr'):
    buf1 = cv2.flip(frame, 0)
    buf = buf1.tostring()
    image_texture = Texture.create(
        size=(frame.shape[1], frame.shape[0]), colorfmt=fmt)
    image_texture.blit_buffer(buf, colorfmt=fmt, bufferfmt='ubyte')
    return image_texture
