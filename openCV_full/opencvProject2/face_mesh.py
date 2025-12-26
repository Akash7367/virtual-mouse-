import cv2
import numpy as np
import mediapipe as mp
import time

cap=cv2.VideoCapture(r"/video/11.mp4")
ptime=0

mp_faceMesh = mp.solutions.face_mesh
face_mes = mp_faceMesh.FaceMesh(max_num_faces=2)
face_draw = mp.solutions.drawing_utils
#for customisation of facemesh
draw_spec = face_draw.DrawingSpec(thickness=1,circle_radius=1,color=(0,255,0))

while True:
    ret, img = cap.read()

    img = cv2.resize(img,(640,480))

    img_bgr = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    results = face_mes.process(img_bgr)

    # print(results.multi_face_landmarks)# this will detect the locations in x,y,z

    if results.multi_face_landmarks:
        for lm in (results.multi_face_landmarks):
            face_draw.draw_landmarks(img,lm,mp_faceMesh.FACEMESH_TESSELATION,draw_spec,draw_spec)
            # print(lm) # this give all points
            for id,lms in enumerate(lm.landmark):
                print(id, lms) #there are 468 points on face which is denoted by ids
                #this all values are in decimals points we have to convert all in pixels
                h,w,c= img.shape
                cx,cy = int(w*lms.x),int(h*lms.y)

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime=ctime

    cv2.putText(img,str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    cv2.imshow('face_mesh',img)

    if cv2.waitKey(1) & 0XFF==ord('x'):
        break
cv2.destroyAllWindows()
cap.release()











