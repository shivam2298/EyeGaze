# import the necessary packages
import numpy as np
import argparse
import cv2

# construct the argument parse and parse the arguments

img = cv2.imread('imgs/5.png', 0)
orig = cv2.imread('imgs/5.png',0)
cv2.imshow('rgb orig',orig)
# Otsu's thresholding after Gaussian filtering
blur = cv2.GaussianBlur(img,(5,5),0)
ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
th3 = cv2.bitwise_not(th3)
cv2.imshow('th',th3)
thresholded, contours, hierarchy = cv2.findContours(th3, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

drawing = np.copy(img)
# cv2.drawContours(drawing, contours, -1, (255, 0, 0), 2)

print(len(contours))

for contour in contours:
    area = cv2.contourArea(contour)

    if(area>500):
        print(area)
        cv2.drawContours(drawing, contour, -1, (255, 0, 0), 2)
        bounding_box = cv2.boundingRect(contour)

        extend = area / (bounding_box[2] * bounding_box[3])

        # reject the contours with big extend
        if extend > 0.8:
            continue

        # calculate countour center and draw a dot there
        m = cv2.moments(contour)
        if m['m00'] != 0:
            center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
            cv2.circle(drawing, center, 3, (0,255,0), -1)

        # fit an ellipse around the contour and draw it into the image
        try:
            ellipse = cv2.fitEllipse(contour)
            cv2.ellipse(drawing, box=ellipse, color=(0, 255, 0))
        except:
            pass

# show the frame
cv2.imshow("Drawing",drawing)
print(drawing.shape)

cv2.waitKey(0)
cv2.destroyAllWindows()
