# shot-tracker
shot-tracker is a project which measures the angle of a basketball as it approaches the basket in real time using imaging technology.

This project has been tested on Windows 10 and Ubuntu 18.04.

![Image of Software](/demo/report.png)

# Installation
The software is written in Python 2.7 and is most likely compatible with any Python 2.x version although it is untested with may versions. See https://wiki.python.org/moin/BeginnersGuide/Download for installation instructions.

### Other Dependencies
1. OpenCV Python: tested on version 3.4.x.
  - For Windows see https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.htmlfor install instructions. Installing from the prebuilt binaries should be sufficient.
  2. For Ubuntu, simply use

```$ sudo apt-get install python-opencv```

  3. If you're using another Linux distribution you're probably fully capable of figuring this out.
2. Kivy, see https://kivy.org/doc/stable/installation/installation.html for installation instructions.
3. Numpy, in case you didn't install Numpy with OpenCV, see https://scipy.org/install.html for instructions.
4. Playsound, install via pip

  ```$ pip install playsound```
  
5. The opencv contrib modules can be installed via pip

  ```$ pip install opencv-contrib-python```

# Usage
Run home.py to start the software. The user can either measure shot live from a webcam or from a previoiusly taken video. The user may click set input to determine the source of the video or which webcam to use.

### Calibration
The system uses the color differences of the ball verses the background to track the shot. Thus results will vary depending on the color of the ball relative to the background.
1. Click *Calibrate* to start the Calibration.
2. If you're tracking shots live, make sure the camera is in place, perpendicular to the line of the shot and halfway between the shooter and the basket.
3. Click on the top of the rim from the perspective of the camera, and then click *next*.
4. Have the shooter take a few shots to calibrate the system. When the ball is in the air, pause the video and click on the ball several times. Repeat this step and continue to adjust the settings until the software tracks the ball fairly reliably and then click *next*.
5. You can name the calibration and save it for future use. The calibration will be saved as a .json file in color-calibrations/files.
6. The false positives screen applies the filter based on the calibration to the In the case that the filter does not filter out all the objects to satisfaction, click on any points which show up which are not the ball and then click *next*.

### Opening a Calibration
1. To open a calibration, click *Open Previous Calibration* on the home screen. Then click on the name of the calibration.
2. After this refer to steps 2 and 6 of the **Calibration** section of this document to continue.


### Tracking
1. At this point, the software will begin to track shots. You can click on the screen to remove false positives from the filter at any time.
2. When finished, click *done* to view the report.

### Report
1. The raw data from each shot is measured and the software attempts to remove outlier points. After this, a parabolic curve is fit to the data from each shot and the results are displayed over an image of the shooter.
2. Several statistics are shown to the left which reflect the accuracy and consistency of the shooter.
3. The optimum angle for a shooter is 45 degrees. But, if the camera is set up at an off angle this reading will not be the correct angle. To avoid this, the shooter should stay in one place and the camera should be set up as described in step 2 of the **Calibration** section of this document.
4. If the software seems to have made a mistake with the tracking of a shot, that shot may be removed from the report by clicking *Edit Results*.
5. Click **Save Data** to save the results as a .csv file. This format can be easily opened using Microsoft Excel or LibreOffice Calc. The raw data saved contains the coefficients of two separate models fitting the data.
  1. The first model returns the y coordinate as a function of the x coordinate.
  2. The second model returns the y coordinate as a function of time.
