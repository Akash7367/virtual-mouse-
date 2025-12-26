import cv2
import numpy as np

flag=False
curr_x=0
curr_y=0

def draw(event,x,y,flags,params):
    global flag,curr_x,curr_y

    if event==1:
        # print('mouse clicked')

        #circle made while clicking
        # cv2.circle(img,center=(x,y),radius=50,color=(0,0,255),thickness=-1)

#       make a rectangle by clicking and moving and releasing

        flag=True
        curr_x=x
        curr_y=y


    elif event==0:
        if flag==True:
            cv2.rectangle(img,pt1=(curr_x,curr_y),pt2=(x,y),color=(0,255,255),thickness=-1)
        # print('mouse  moved')

    else:
        # print('mouse released')
        flag=False
        # cv2.rectangle(img, pt1=(curr_x, curr_y), pt2=(x, y), color=(0, 255, 255), thickness=-1)

cv2.namedWindow(winname="window")
cv2.setMouseCallback("window",draw)


img=np.zeros((512,512,3))

while True:
    cv2.imshow("window",img)

    if cv2.waitKey(1) & 0xFF == ord('x'):
        break
cv2.destroyAllWindows()