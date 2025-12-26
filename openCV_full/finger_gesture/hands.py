import numpy as np
import cv2
import mediapipe as mp
import time

# from mediapipe.python.solutions.hands_connections import HAND_CONNECTIONS

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mpDraw = mp.solutions.drawing_utils

ptime=0
ctime=0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # print(results.multi_hand_landmarks)
    # this will give an output in x,y,z directions

    # if you want to use all this value for different purpose
    # then we have to make this a module

    if results.multi_hand_landmarks:
        for i in results.multi_hand_landmarks:
            # for each point we have to give an unique value call as id
            # print(i.landmark)#each location in x,y,z

            # x,y,z is the decimal values may be the ration for this we have to convert in pixel
            # our image have this pixel
            h,w,c = img.shape
            print(h,w,c)

            for id, lm in enumerate(i.landmark):
                cx,cy=int(lm.x*w),int(lm.y*h)
                print(id,cx,cy)

                #there is 21 point in single hand and you can control any point of them by id value
                #4->thumb, 4*i ((8)i=2(index finger),i=3(middle finger)..i->5(small finger)
                # understand with code
                if id==4:#this will for top thumb
                    cv2.circle(img,center=(cx,cy),radius=15,color=(255,0,0),thickness=cv2.FILLED)



                # print(id,lm)#id->id of each location, lm->location of hand center
            mpDraw.draw_landmarks(img,i,mp_hands.HAND_CONNECTIONS)
            #i -> dots on hand,mp_hands.HAND_CONNECTIONS join all the dots


    ctime=time.time()
    fps = 1/(ctime-ptime)#frame rate
    ptime=ctime

    cv2.putText(img, org=(15, 60), fontScale=3, color=(255,0,0), thickness=2, lineType=cv2.LINE_AA,
                fontFace=cv2.FONT_HERSHEY_PLAIN, text=str(int(fps)))

    # cv2.putText(img,org=(10,10),fontScale=3,color=(255,0,0),fonFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,lineType=cv2.LINE_AA, text=str(fps))

    cv2.imshow('Window',img)

    if cv2.waitKey(1) & 0xff==ord('x'):
        break

cv2.destroyAllWindows()