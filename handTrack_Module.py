import numpy as np
import cv2
import mediapipe as mp
import time
import math

class handDetect():
    def __init__(self,mode=False,max_hand=2,detect_con=0.5,track_con=0.5):
    #thiese all value are from hand dectation module by click Hands() with ctrl
    # and all these can be written in constructor
    #     static_image_mode = False,
    #     max_num_hands = 2,
    #     model_complexity = 1,
    #     min_detection_confidence = 0.5,
    #     min_tracking_confidence = 0.5):

    #now define all variable such that we can use it later

        self.mode=mode
        self.max_hand=max_hand
        self.detect_con=detect_con
        self.track_con=track_con


        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hand,
            min_detection_confidence=self.detect_con,
            min_tracking_confidence=self.track_con
        )
        self.mpDraw = mp.solutions.drawing_utils

        self.tip_ids = [4, 8, 12, 16, 20]

    def find_hand(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handlms,self.mp_hands.HAND_CONNECTIONS)

        return img

    def find_pos(self,img,handNo=0,draw=True):
        xlist=[]
        ylist=[]
        bbox=[]

        self.lmlist=[]
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(my_hand.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                #     print(id,cx,cy)
                xlist.append(cx)
                ylist.append(cy)

                self.lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(img,center=(cx,cy),radius=5,color=(255,0,0),thickness=cv2.FILLED)

            xmin,xmax = min(xlist),max(xlist)
            ymin,ymax = min(ylist),max(ylist)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img,(xmin-20,ymin-20),(xmax+20,ymax+20),(0,255,0),2)

        return self.lmlist, bbox

    def fingerUp(self):
        fingers = []
        # this condition is specially for thumb because the tip position is difficult to down the 6th pos
        if self.lmlist[self.tip_ids[0]][1] < self.lmlist[self.tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # for all 4 fingers
        for id in range(1, 5):
            if self.lmlist[self.tip_ids[id]][2] < self.lmlist[self.tip_ids[id] - 2][2]:
                # print('index finger open')
                fingers.append(1)  # 1 means open and 0 means closed
            else:
                fingers.append(0)
        return fingers

    def findDistance(self,img,p1,p2,draw=True,r=15,t=3):
        x1,y1 = self.lmlist[p1][1:]
        x2,y2 = self.lmlist[p2][1:]
        cx,cy = (x1+x2)//2,(y1+y2)//2

        if draw:
            cv2.line(img,(x1,y1),(x2,y2),(255,0,255),t)
            cv2.circle(img,(x1,y1),r,(255,0,255),cv2.FILLED)
            cv2.circle(img,(x2,y2),r,(255,0,255),cv2.FILLED)
            cv2.circle(img,(cx,cy),r,(0,0,255),cv2.FILLED)
        length = math.hypot(x2-x1,y2-y1)

        return length, img, [x1,y1,x2,y2,cx,cy]



def main():
    ptime=0
    cap = cv2.VideoCapture(0)
    detector=handDetect()

    while True:
        success, img = cap.read()

        img=detector.find_hand(img)#if False then this fn isn't working
        lmlist = detector.find_pos(img)#we can chage the value of draw if it false nothing happen by this fn
        if len(lmlist)!=0:
            # print(lmlist[4])
            pass
        ctime = time.time()
        fps = 1 / (ctime - ptime)  # frame rate
        ptime = ctime
        cv2.putText(img, org=(15, 60), fontScale=3, color=(255, 0, 0), thickness=2, lineType=cv2.LINE_AA,
                    fontFace=cv2.FONT_HERSHEY_PLAIN, text=str(int(fps)))

        cv2.imshow('Window',img)
        if cv2.waitKey(1) & 0XFF == ord('x'):
            break


    cv2.destroyAllWindows()
    cap.release()


if __name__== '__main__':
    main()

