import cv2
import numpy as np
from numpy.ma.core import filled

# read an image

img=np.zeros((512,512,3))

#creating or draw an image
#rectangle
cv2.rectangle(img,pt1=(100,30),pt2=(260,70),color=(0,0,255),thickness=-1)

cv2.rectangle(img,pt1=(100,60),pt2=(260,100),color=(255,255,255),thickness=-1)

cv2.rectangle(img,pt1=(100,90),pt2=(260,120),color=(0,255,0),thickness=-1)

#Ciecle
cv2.circle(img,center=(100,400),radius=30,thickness=-1,color=(0,0,255))
cv2.circle(img,center=(100,390),radius=25,thickness=-1,color=(150,210,0))
cv2.circle(img,center=(180,75),radius=15,color=(255,0,0),thickness=1)

#line
cv2.line(img,pt1=(100,390),pt2=(100,30),color=(0,255,0),thickness=3)#pt1=(x,y)

#text
cv2.putText(img,org=(130,300),fontScale=4,color=(0,255,255),thickness=2,lineType=cv2.LINE_AA,fontFace=cv2.FONT_HERSHEY_PLAIN,text='INDIAN FLAG')

cv2.imshow('win',img)
cv2.waitKey(0)