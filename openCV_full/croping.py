import cv2
import numpy as np

flag=False
ix=0
iy=0

def crop(event,x,y,flags,params):
    global flag,ix,iy

    if event == 1:
        flag=True
        ix=x
        iy=y

        # print('mouse clicked')
    elif event==4:
        fx=x
        fy=y
        flag=False
        cv2.rectangle(img_resize,pt1=(ix,iy),pt2=(x,y),color=(0,0,0),thickness=1)
        img_crop = img_resize[iy:fy,ix:fx]#[y:x]
        cv2.imwrite('Images/Fruit crop.jpg',img_crop)
        # cv2.imshow('wind',img_crop)
        # cv2.waitKey(0)


cv2.namedWindow(winname='win')
cv2.setMouseCallback('win',crop)


img=cv2.imread('Images/anna.jpg')

img_resize = cv2.resize(img,(img.shape[1]//8,img.shape[0]//8))

while True:
    cv2.imshow('win',img_resize)

    if cv2.waitKey(1) & 0xff == ord('x'):
        break
cv2.destroyAllWindows()



