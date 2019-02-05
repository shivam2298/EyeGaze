import cv2
import numpy as np

img = cv2.imread('jack.png',0)
mask = img > 1
img[mask] = 255
mask = img <= 1
img[mask] = 0
print(img.shape)
# print(img)
cimg = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

# mask = np.zeros(cimg.shape[0], cimg.shape[1])
cv2.imshow("frame",cimg)
# circles = cv2.HoughCircles(cimg,cv2.HOUGH_GRADIENT,1,1000,
#                             param1=50,param2=30,minRadius=0,maxRadius=0)
# print(circles)
# circles = np.uint16(np.around(circles))
# for i in circles[0,:]:
#     # draw the outer circle
#     cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
#     # draw the center of the circle
#     cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
#
# cv2.imshow('detected circles',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
