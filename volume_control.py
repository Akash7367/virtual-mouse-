import numpy as np
import mediapipe as mp
import cv2
import os
import time
import handTrack_Module as htm
import math

# for volume control  we use this liberary at github
# https://github.com/AndreMiras/pycaw
# and use this modules
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# these all are the properties of volume control by pychaw

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()#  this is the range
# volume.SetMasterVolumeLevel(0, None)

min_vol = volRange[0]
max_vol = volRange[1]

vol=0
volBar=400
vol_per=0


wcam,hcam=1400,900
cap = cv2.VideoCapture(0)

#use for video camera
cap.set(3,wcam)
cap.set(4,hcam)

ptime=0

detector = htm.handDetect(detect_con=0.7)

# htm.handDetect()

while True:
    ret, img = cap.read()
    img=detector.find_hand(img)

    #get hand position
    lms,_ = detector.find_pos(img,draw=False)
    if len(lms)!=0:
        # print(lms[4],lms[8])

        # we can also define all points in a variable
        x1,y1=lms[4][1],lms[4][2]
        x2,y2 = lms[8][1],lms[8][2]
        cx,cy = (x1+x2)//2,(y1+y2)//2

        cv2.circle(img,(lms[4][1],lms[4][2]),15,(255,0,0),cv2.FILLED)
        cv2.circle(img,(lms[8][1],lms[8][2]),15,(255,0,0),cv2.FILLED)
        cv2.line(img,(lms[4][1],lms[4][2]),(lms[8][1],lms[8][2]),(255,0,0),5)
        cv2.circle(img,((lms[4][1]+lms[8][1])//2,(lms[4][2]+lms[8][2])//2),15,(255,0,0),cv2.FILLED)

        line_length = math.hypot(x2-x1,y2-y1)
        print(line_length)

        # by this length we know the range which is 50-300
        # and volume_range = (-96.0, 0.0, 0.125)

        # for ranging this we will use numpy interp method
        vol = np.interp(line_length,[50,250],[min_vol,max_vol])
        volBar = np.interp(line_length,[50,250],[400,150])
        vol_per = np.interp(line_length,[50,250],[0,100])


        print(int(line_length),vol)
        volume.SetMasterVolumeLevel(vol,None)

        if line_length<50:
            cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)

        # now all thing is happened lets draw a volume bar at the side of video
        cv2.rectangle(img,(50,150),(85,400),(0,255,255),3)
        cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,255),cv2.FILLED)
        cv2.putText(img,f"{int(vol_per)} %",(40,450),cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),3)

    #for video
    # img = cv2.resize(img,(640,480))

    # img_bgr = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    ctime= time.time()
    fps = 1/(ctime-ptime)
    ptime=ctime

    cv2.putText(img,str(int(fps)),(50,70),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),1,cv2.LINE_AA)

    cv2.imshow('hand_vol',img)

    if cv2.waitKey(1) & 0XFF==ord('x'):
        break
cv2.destroyAllWindows()
cap.release()