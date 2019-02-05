import numpy as np  
import cv2  
import dlib  
from main import detectPupil
 
cascPath = "haarcascade_frontalface_default.xml"  
PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"  

JAWLINE_POINTS = list(range(0, 17))  
RIGHT_EYEBROW_POINTS = list(range(17, 22))  
LEFT_EYEBROW_POINTS = list(range(22, 27))  
NOSE_POINTS = list(range(27, 36))  
RIGHT_EYE_POINTS = list(range(36, 42))  
LEFT_EYE_POINTS = list(range(42, 48))  
MOUTH_OUTLINE_POINTS = list(range(48, 61))  
MOUTH_INNER_POINTS = list(range(61, 68))  

# Create the haar cascade  
faceCascade = cv2.CascadeClassifier(cascPath)  

predictor = dlib.shape_predictor(PREDICTOR_PATH)  


video_capture = cv2.VideoCapture(0)

while(True):
    # Read the image  
    ret, frame = video_capture.read()

    image = cv2.flip(frame,1)  
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  

    # Detect faces in the image  
    faces = faceCascade.detectMultiScale(  
    gray,  
    scaleFactor=1.05,  
    minNeighbors=5,  
    minSize=(100, 100),  
    flags=cv2.CASCADE_SCALE_IMAGE  
    )  

    #print("Found {0} faces!".format(len(faces)))  

    # Draw a rectangle around the faces  
    for (x, y, w, h) in faces:  
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  

        # Converting the OpenCV rectangle coordinates to Dlib rectangle  
        dlib_rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))  

        landmarks = np.matrix([[p.x, p.y]  
               for p in predictor(image, dlib_rect).parts()])  

        landmarks_display = landmarks[RIGHT_EYE_POINTS]

        if landmarks_display is None:
            continue

        maxX,minX,maxY,minY = (0,640,0,480)
        for idx, point in enumerate(landmarks_display):
            pos = (point[0, 0], point[0, 1])
            ptx = point[0, 0]
            pty = point[0,1]

            maxX = max(maxX,ptx)
            minX = min(minX,ptx)
            maxY = max(maxY,pty)
            minY = min(minY,pty)  
            cv2.circle(image, pos, 0, color=(0, 255, 255), thickness=-1)

        roi = image[minY+1:maxY-1, minX+1:maxX-1]
        
        try:
            (pup_x,pup_y),pupil_frame =  (detectPupil(roi))
            cv2.imshow("pupil",pupil_frame)
        except Exception as e:
            print e
        cv2.rectangle(image, (minX, minY), (maxX, maxY), (0, 255, 0), 0) 
        
    cv2.imshow("Landmarks found", image)  
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
