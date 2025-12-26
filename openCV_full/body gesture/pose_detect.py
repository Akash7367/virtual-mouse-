import cv2
import numpy as np
import mediapipe as mp
import time

cap = cv2.VideoCapture(r"/video/1.mp4")  # Change the path to your video file
ptime=0

# make object which can detect our pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
#for drawing
draw=mp.solutions.drawing_utils


while True:
    ret, img = cap.read()


    # Resize the frame to a normal size (e.g., 640x480)
    img = cv2.resize(img,(640,480))

    #our model didn't detect rgb image hence we change our image into bgr
    img_cvt = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    results = pose.process(img_cvt)

    # for seeing results use this method
    # print(results.pose_landmarks)# it gives all location value in x,y,z
    if results.pose_landmarks:
        #this will give all points
        # draw.draw_landmarks(img,results.pose_landmarks)

        # for connection add another parameter mp_pose.poss_connection
        draw.draw_landmarks(img,results.pose_landmarks,mp_pose.POSE_CONNECTIONS)

        #give all points to their ids
        for id,lm in enumerate(results.pose_landmarks.landmark):
            # lm gives location and visibility
            #all points are in decimals and hence change into pixel

            h,w,c=img.shape

            cx,cy = int(lm.x*w),int(lm.y*h)
            print(id,cx,cy)

            #some id have denote this total 33 point available hence each point have their id
            #8->right eye,7->left eye,12 and 11 for right and left soldiers resp.
            #24 23 kamar



    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime




    cv2.putText(img,str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)



    cv2.imshow("Video", img)

    if cv2.waitKey(1) & 0XFF==ord('x'):
        break

cv2.destroyAllWindows()

