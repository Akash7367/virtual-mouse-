import cv2
import numpy as np
import mediapipe as mp
import handTrack_Module as htm
import time


# eraser thickness and brush thickness

brushThickness = 15
eraserThickness = 70


# cap = cv2.VideoCapture(r"C:\Users\akash\PycharmProjects\Open CV\video\hand_pointer.mp4")

draw_color = (255,0,255)

cap = cv2.VideoCapture(0)
cap.set(3,680)
cap.set(4,500)

images = cv2.imread(r"C:\Users\akash\PycharmProjects\Open CV\Images\brushes.png")
image = cv2.resize(images,(680,100))

ptime=0

detector =htm.handDetect(detect_con=0.85)
xp,yp =0,0

imgCanvas = np.zeros((500,680,3), np.uint8)#uint8 means unsigned integer

while True:
    # 1. images or video read
    ret, img = cap.read()
    img = cv2.resize(img,(680,500))

    # if we want to draw any thing then we have to flip the image
    img = cv2.flip(img,1)


    #2. hand detect
    hands = detector.find_hand(img)
    hand_lm,_ = detector.find_pos(img,draw=False)
    # print(hand_lm)
    # print(hand_lxm)
    # 3. find hand position or landmarks
    if len(hand_lm)!=0:
        # print(hand_lm)

        # # for index and middle fingers
        x1,y1 = hand_lm[8][1],hand_lm[8][2]
        x2,y2 = hand_lm[12][1],hand_lm[12][2]


        # 4. check which finger are up
        fingers = detector.fingerUp()
        # print(fingers)

        # 5. if selection Mode - two fingers are up
        if fingers[1] and fingers[2]:# two or more finger are up
            # print('Selection mode')
            xp,yp=0,0

            # now check its clicked or not
            if y1 < 100:
                if 0<x1<136:
                    draw_color = (0,255,0)
                    # print('Green')
                elif 136<=x1<272:
                    draw_color = (0,0,255)
                    # print('Red')
                elif 272<=x1<408:
                    draw_color = (255,0,0)
                    # print('Blue')
                elif 408<=x1<535:
                    draw_color = (0,0,0)
                    # print('Eraser')

            # lets make visiual mode
            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),draw_color,cv2.FILLED)


        if fingers[1] and fingers[2]==False:# its mean only one finger are up
            # print('Drawing Mode')
            cv2.circle(img,(x1,y1),15,draw_color,cv2.FILLED)

            # By this it will draw an line but removed instantly for we use numpy method by creating new image
            if xp==0 and yp==0:
                xp,yp=x1,y1

            # for brushes
            if draw_color == (0,0,0): # this will draw on black board
                cv2.line(img, (xp, yp), (x1, y1), draw_color, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), draw_color, eraserThickness)
            else:
                cv2.line(img,(xp,yp),(x1,y1),draw_color,brushThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),draw_color,brushThickness)

            xp,yp = x1,y1

    # some images property by cv
    imgGrey = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGrey,50,255,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)

    # print(img.shape, imgInv.shape) # this will insure that shape should same

    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imgCanvas)


    # 6. if drawing Mode - Index finger is up
    img[0:100,0:680]= image
    # img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)# this will two images but it is just too dull not too clear and hence use other cv2 images method
    cv2.imshow('pointer',img)
    # cv2.imshow('canvas',imgCanvas)#this is for black board
    # cv2.imshow('inv',imgInv) #this is for white board
    if cv2.waitKey(1) & 0XFF==ord('x'):
        break
cv2.destroyAllWindows()
cap.release()
