import cv2
import numpy as np

def filter(image, lower_bound, upper_bound):
    blur = cv2.GaussianBlur(image, (5,5),0)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    height, width, channels = hsv.shape

    # threshhold for basketball in general
    #lower_bound = np.array([12, 95, 150])
    #upper_bound = np.array([17, 200, 200])

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    # # Blur the mask
    bmask = cv2.GaussianBlur(mask, (5,5),0)

    output = cv2.bitwise_and(image, image, mask = bmask)

    return output

def search(image, lower_bound, upper_bound):

    '''Accepts BGR image as Numpy array
       Returns: (x,y) coordinates of centroid if found
                (-1,-1) if no centroid was found
                None if user hit ESC
    '''

    # Blur the image to reduce noise
    blur = cv2.GaussianBlur(image, (5,5),0)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    height, width, channels = hsv.shape

    # threshhold for basketball in general
    #lower_bound = np.array([12, 95, 150])
    #upper_bound = np.array([17, 200, 200])

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    # Blur the mask
    bmask = cv2.GaussianBlur(mask, (5,5),0)

    # Take the moments to get the centroid
    moments = cv2.moments(bmask)
    m00 = moments['m00']
    centroid_x, centroid_y = None, None
    if m00 != 0:
        centroid_x = int(moments['m10']/m00)
        centroid_y = int(moments['m01']/m00)

    # Assume no centroid
    ctr = (-1,-1)

    # Use centroid if it exists
    if centroid_x != None and centroid_y != None:

        ctr = (centroid_x, centroid_y)

    # Return coordinates of centroid
    return ctr
