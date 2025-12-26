import cv2
import mediapipe as mp
import numpy as np
import os
import time
import handTrack_Module as htm

# cap = cv2.VideoCapture(r"C:\Users\akash\PycharmProjects\Open CV\video\finger_count.mp4")
cap = cv2.VideoCapture(0)
cap.set(3,1080)
cap.set(4,720)

folderpath = r"C:\Users\akash\PycharmProjects\Open CV\Count_Fing Images"# same as int images folder
mylist = os.listdir(folderpath)
print(mylist)

all_img_path=[]
for img_path in mylist:
    image = cv2.imread(f'{folderpath}\{img_path}')
    print(f"{folderpath}\{img_path}")
    all_img_path.append(image)


ptime=0

detector = htm.handDetect(detect_con=0.75)

tip_ids = [4,8,12,16,20]  # this are the tips of all fingers 4->thumb and so on..


while True:
    ret,img = cap.read()
    # img = cv2.resize(img,(640,480))

    img = detector.find_hand(img,True)

    lmlist,_ = detector.find_pos(img,draw=False)

    if len(lmlist)!=0:
        # print(lmlist)
        fingers=[]

        # this condition is specially for thumb because the tip position is difficult to down the 6th pos
        if lmlist[tip_ids[0]][1] > lmlist[tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)



        for id in range(1,5):
            if lmlist[tip_ids[id]][2]<lmlist[tip_ids[id]-2][2]:
                # print('index finger open')
                fingers.append(1) #1 means open and 0 means closed
            else:
                fingers.append(0)
        print(fingers)


        total_fingers = fingers.count(1)
        print(total_fingers)

    # img[0:200,0:200]=all_img_path[0] # this shows those image which have 200*200 px
    # but for all images

        h,w,c = all_img_path[total_fingers-1].shape
        img[0:h,0:w] = all_img_path[total_fingers-1]

        cv2.rectangle(img,(10,250),(150,420),(0,255,255),-1)
        cv2.putText(img,str(total_fingers),(30,380),cv2.FONT_HERSHEY_COMPLEX,5,(255,0,0),8)

    ctime=time.time()
    fps = 1/(ctime-ptime)
    ptime=ctime

    cv2.putText(img,f"fps: {int(fps)}",(180,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),2)


    cv2.imshow('finger_count',img)

    if cv2.waitKey(1) & 0XFF==ord('x'):
        break

cv2.destroyAllWindows()
cap.release()

