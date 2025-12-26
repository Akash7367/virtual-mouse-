import cv2
import numpy as np

vid = cv2.VideoCapture(0)
#to save video
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output.avi',fourcc,20.0,(640,480))

while True:
    ret, frame = vid.read()

    cv2.imshow('web',frame)
    # out.write(frame)

    #change color
    cvt_color=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    # print()

    if cv2.waitKey(1) & 0xff == ord('x'):
        break

# out.release()
cv2.destroyAllWindows()
