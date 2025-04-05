import cv2
import pytesseract
import numpy as np
from matplotlib import pyplot as plt
import re

images = []
# Load the image
image_path = "real_coupon.jpg"
image = cv2.imread(image_path)
images.append(image)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
images.append(gray)
# Apply adaptive thresholding to make the text stand out
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 11, 2)
images.append(thresh)
# Morphological closing to connect dashed lines
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,1))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
images.append(closed)

for i in images:
    cv2.imshow("Detected Rectangles", i)
    cv2.waitKey(0)
    cv2.destroyAllWindows()