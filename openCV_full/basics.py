import cv2
import numpy as np

#read an images
img=cv2.imread("Images/anna.jpg")
# img2=cv2.imread('Images/ed.jpeg')
# print(type(img))

# img_cnvrt=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# img_blue=img[:,:,0]
# img_red=img[:,:,2]
# img_green = img[:,:,1]

# image resize
img_resize=cv2.resize(img,(img.shape[1]//10,img.shape[0]//10 ))

print("original image size: ",img.shape,"\nNew image size: ",img_resize.shape)

# multiple image
# img_r=np.hstack((img_blue,img_green,img_red))

# flip an image
img_h_flip=cv2.flip(img_resize,0)
img_v_flip=cv2.flip(img_resize,1)
img_mix_flip=cv2.flip(img_resize,-1)


#crop an image
img_crop = img[0:300,0:300]#(l,b) the top corner is always start at (0,0)

# to save an image
# cv2.imwrite('Images/croped image.jpg',img_crop)




img_com=np.hstack((img_h_flip,img_v_flip,img_mix_flip))

cv2.imshow('window',img_com)
cv2.waitKey(0)
