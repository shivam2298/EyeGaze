# import the necessary packages
import numpy as np
import argparse
import cv2

def detectPupil(image):
    cv2.imshow("eye_image",image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray,(5,5),0)
    
    # Otsu's thresholding after Gaussian filtering
    ret3,otsu_thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    inverted_image = cv2.bitwise_not(otsu_thresh)


    contours, hierarchy = cv2.findContours(inverted_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    drawing = np.copy(gray)

    print(len(contours))

    center = None

    for idx,contour in enumerate(contours):

        area = cv2.contourArea(contour)
        
        if(area>100):
            print("contour {} area: {}".format(idx,area))

            cv2.drawContours(drawing, [contour], 0, (255, 0, 0), 0)
            
            bounding_box = cv2.boundingRect(contour)

            extend = area / (bounding_box[2] * bounding_box[3])

            # reject the contours with big extend
            if extend > 0.8:
                continue

            # calculate countour center and draw a dot there
            m = cv2.moments(contour)
            if m['m00'] != 0:
                center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
                cv2.circle(image, center, 0, (0,0,255), -1)

            #cx and cy are centers of the image
            # draw line from center to contour center
            cx, cy = image.shape[1]//2,image.shape[0]//2    
            cv2.line(image,(cx,cy),(center[0],center[1]),(128,0,128),1)
            
            # fit an ellipse around the contour and draw it into the image
            try:
                ellipse = cv2.fitEllipse(contour)
                cv2.ellipse(image, box=ellipse, color=(0, 255, 0))
            except:
                pass

    return (center,image)

# show the frame

if __name__ == "__main__":
    file_name = raw_input("enter the name of file: ")
    print file_name
    image = cv2.imread(file_name,1)
    (pupil_x,pupil_y),image_with_pupil = detectPupil(image)
    cv2.imshow("detected_pupil",image_with_pupil)
    #print(drawing.shape)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
