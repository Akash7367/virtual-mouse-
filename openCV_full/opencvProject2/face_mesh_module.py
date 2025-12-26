import cv2
import numpy as np
import mediapipe as mp
import time

class FaceMeshDetector:
    def __init__(self,img_static_mode = False,max_face=2,refine_landmarks = False,
                 min_det_con=0.5,min_track_con=0.5):
        self.img_mode = img_static_mode
        self.max_faces = max_face
        self.refine_landmarks = refine_landmarks
        self.min_det_con = min_det_con
        self.min_track_con = min_track_con

        self.mp_faceMesh = mp.solutions.face_mesh
        self.face_mes = self.mp_faceMesh.FaceMesh(self.img_mode,self.max_faces,
                                                  self.refine_landmarks,self.min_det_con,
                                                  self.min_track_con)
        self.face_draw = mp.solutions.drawing_utils
        #for customisation of facemesh
        self.draw_spec = self.face_draw.DrawingSpec(thickness=1,circle_radius=1,color=(0,255,0))


    def findFaceMesh(self,img,draw):
        self.img_bgr = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        self.results = self.face_mes.process(self.img_bgr)

        # print(results.multi_face_landmarks)# this will detect the locations in x,y,z
        faces=[]
        if self.results.multi_face_landmarks:
            for lm in (self.results.multi_face_landmarks):
                if draw:
                    self.face_draw.draw_landmarks(img,lm,self.mp_faceMesh.FACEMESH_TESSELATION,self.draw_spec,self.draw_spec)
                face=[]
                for id,lms in enumerate(lm.landmark):
                    h,w,c= img.shape
                    cx,cy = int(w*lms.x),int(h*lms.y)
                    face.append([id,cx,cy])
                faces.append(face)
        return img,faces

def main():
    cap = cv2.VideoCapture(r"/video/11.mp4")
    ptime = 0
    detector = FaceMeshDetector()


    while True:
        ret, img = cap.read()

        img = cv2.resize(img, (640, 480))

        img,face=detector.findFaceMesh(img,True)
        if len(face)!=0:
            print(len(face))
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.imshow('face_mesh', img)

        if cv2.waitKey(1) & 0XFF == ord('x'):
            break
    cv2.destroyAllWindows()
    cap.release()

if __name__=='__main__':
    main()












