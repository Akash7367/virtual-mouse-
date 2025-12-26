import cv2
import mediapipe as mp
import time
import pose_dect_Module as pdm
import numpy as np


# 6->gym,8
cap = cv2.VideoCapture(r"C:\Users\akash\PycharmProjects\Open CV\video\12.mp4")
# cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

# img = cv2.imread(r"C:\Users\akash\PycharmProjects\Open CV\Images\gym.jpg")

ptime=0
detector = pdm.PoseDetect()
count=0
dir=0 # dir=0 means down and dir=1 means up

per = 400

while True:
    ret,img = cap.read()

    # for reading an image
    img = cv2.resize(img,(640,480))

    img = detector.FindPose(img,False)
    pose = detector.get_pos(img,False)

    print(img.shape)
    #
    # #13,14-> elbow 15,16->wrist
    if len(pose)!=0:
        # print(pose)
        #for rigth arm
        angle = detector.find_angle(img,12,14,16)

        # for left arm
        # detector.find_angle(img,11,13,15)

        per = np.interp(angle,(5,130),(0,100))
        bar = np.interp(angle,(2,180),(400,100))
        # print(angle, bar)
        # print(angle,per)
        # print(angle,bar)

        color = (255,0,255)
        if per == 100 and dir == 0:
            # if dir == 0:
            count+=0.5
            # color = (255,0,255)
            dir=1
        if per == 0 and dir == 1:
            # if dir == 1:
            # color=(0,255,255)
            count += 0.5
            dir=0


        ctime=time.time()
        fps = 1/(ctime-ptime)
        ptime=ctime

        # dumble up and down count
        cv2.rectangle(img,(3,350),(100,480),(0,255,0),-1)
        cv2.putText(img,str(int(count)),(20,460),cv2.FONT_HERSHEY_PLAIN,8,(255,0,0),7)

        # percentage Bar
        cv2.rectangle(img,(550,100),(600,400),color,2)
        cv2.rectangle(img,(550,int(bar)),(600,400),color,cv2.FILLED)
        cv2.putText(img,str(int(per)),(550,90),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)

        #fps count
        cv2.putText(img,f'fps: {int(fps)}',(50,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)

    cv2.imshow('gym',img)

    # cv2.waitKey(0)
    if cv2.waitKey(1) & 0XFF==ord('x'):
        break

cv2.destroyAllWindows()
cap.release()




