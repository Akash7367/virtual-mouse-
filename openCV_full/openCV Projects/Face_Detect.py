import cv2
import numpy as np
import mediapipe as mp
import time

# cap=cv2.VideoCapture(r"/video/11.mp4")
cap=cv2.VideoCapture(0)
ptime=0

mp_face = mp.solutions.face_detection
mp_draw = mp.solutions.drawing_utils
face_detect = mp_face.FaceDetection()


while True:
    ret, img = cap.read()
    img=cv2.resize(img,(640,480))
    img_cvt = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)


    results = face_detect.process(img_cvt)
    #give all information like point if face available
    # print(results.detections)

    if results.detections:
        for id, lm in enumerate(results.detections):
            # print(id, lm)
            # print(lm.location_data.relative_bounding_box)
            detect = lm.location_data.relative_bounding_box

            # mp_draw.draw_detection(img,lm)# this will draw a rectangle box

            h,w,c = img.shape
            b_box = int(detect.xmin*w),int(detect.ymin*h),int(detect.width*w),int(detect.height*h)
            #see this reults you will know some key points how we fetch the exact location

            # the draw function draw a rectangle but we will try draw a rectangle by another way
            # to do customisation like at corner it will thicker

            cv2.rectangle(img,b_box,(255,0,255),2)
            cv2.putText(img,f'{int(lm.score[0]*100)}%',(b_box[0],b_box[1]-20),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),2)


    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime

    cv2.putText(img,str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    cv2.imshow('Face',img)

    if cv2.waitKey(1) & 0XFF==ord('x'):
        break

cap.release()
cv2.destroyAllWindows()
