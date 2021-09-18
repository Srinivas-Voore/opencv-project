#import the necessary packages
import numpy as np
import cv2
# load the image and convert it to grayscale
def mark(frame):
    image = cv2.imread(frame)
    orig = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # apply a Gaussian blur to the image then find the brightest
    # region
    gray = cv2.GaussianBlur(gray,(41,41),0)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    # print(maxVal)
    if(maxVal>200):
        image = orig.copy()
        cv2.circle(image, maxLoc, 41, (255, 0, 0), 2)
        # display the results of our newly improved method
        cv2.imshow("Robust", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
