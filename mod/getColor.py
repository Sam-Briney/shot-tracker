import cv2
import numpy as np

import mod.find as find

h = []
s = []
v = []

samples = 0

sensitivity = 0.3

def hpmAdjust(std):
    global sensitivity
    return round(10 * sensitivity**(2/3) * std**(1.0/7))

def spmAdjust(std):
    global sensitivity
    return round(50 * sensitivity * std**(1.0/7))

def vpmAdjust(std):
    global sensitivity
    return round(50 * sensitivity * std**(1.0/7))

def resetSamples():
    global h, s, v, samples, sensitivity
    h = []
    s = []
    v = []

    samples = 0

    sensitivity = 0.3

def addSample(image, x, y, radius):
    global h, s, v, samples

    selection = cv2.cvtColor(image[y-radius:y+radius, x-radius:x+radius], cv2.COLOR_BGR2HSV)

    r2 = radius**2

    xCount = 0
    for row in selection:
        xCount += 1
        yCount = 0
        for hsv in row:
            yCount += 1
            samples += 1
            # circular region
            if (xCount - radius)**2 + (yCount - radius)**2 < radius**2:
                h.append(hsv[0])
                s.append(hsv[1])
                v.append(hsv[2])

    std = [round(np.std(h), 1), round(np.std(s), 1), round(np.std(v), 1)]
    median = [np.median(h), np.median(s), np.median(v)]

    return[median, std]

def get(sampleImages):
    global h, s, v, samples

    std = [np.std(h), np.std(s), np.std(v)]

    median = [np.median(h), np.median(s), np.median(v)]

    hpm = hpmAdjust(std[0])
    spm = spmAdjust(std[1])
    vpm = vpmAdjust(std[2])

    lower = [median[0] - hpm, median[1] - spm, median[2] - vpm]
    upper = [median[0] + hpm, median[1] + spm, median[2] + vpm]

    for i in range(len(lower)):
        if lower[i] < 0:
            lower[i] = 0

    if upper[0] > 179:
        upper[0] = 179

    if upper[1] > 255:
        upper[1] = 255

    if upper[2] > 255:
        upper[2] = 255


    return [lower, upper]
