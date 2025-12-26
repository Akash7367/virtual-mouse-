import cv2
import numpy as np
import mediapipe as mp
import time

class Face_Detect():
    def __init__(self,detect_conf=0.2):
        self.detect_conf=detect_conf
        # self.model_select = model_select


        self.mp_face = mp.solutions.face_detection
        self.mp_draw = mp.solutions.drawing_utils
        self.face_detect = self.mp_face.FaceDetection(self.detect_conf)


    def find_face(self,img,draw=True):

        img_cvt = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        self.results = self.face_detect.process(img_cvt)
        bbox=[]
        if self.results.detections:
            for id, lm in enumerate(self.results.detections):
                # print(id, lm)
                # print(lm.location_data.relative_bounding_box)
                detect = lm.location_data.relative_bounding_box

                # mp_draw.draw_detection(img,lm)# this will draw a rectangle box

                h,w,c = img.shape
                b_box = int(detect.xmin*w),int(detect.ymin*h),int(detect.width*w),int(detect.height*h)

                self.optimise_rect(img,b_box)


                bbox.append([id, b_box, lm.score])
                cv2.putText(img,f'{int(lm.score[0]*100)}%',(b_box[0],b_box[1]-20),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),2)
        return img, bbox


    def optimise_rect(self,img,bbox,l=15,t=5,rt=1):
        x,y,w,h = bbox
        x1,y1=x+w,y+h

        cv2.rectangle(img,bbox,(255,0,255),rt)
        #top left x,y
        cv2.line(img,(x,y),(x+l,y),(255,0,255), t)
        cv2.line(img,(x,y),(x,y+l),(255,0,255), t)

        #top right x1,y
        cv2.line(img,(x1,y),(x1-l,y),(255,0,255), t)
        cv2.line(img,(x1,y),(x1,y+l),(255,0,255), t)

        #buttom left x,y1
        cv2.line(img, (x, y1), (x+l, y1), (255, 0, 255), t)
        cv2.line(img, (x, y1), (x, y1-l), (255, 0, 255), t)

        #buttom right x1,y1
        cv2.line(img, (x1, y1), (x1-l, y1), (255, 0, 255), t)
        cv2.line(img, (x1, y1), (x1, y1-l), (255, 0, 255), t)

def main():
    cap = cv2.VideoCapture(r"/video/11.mp4")
    detect = Face_Detect()
    ptime=0
    while True:
        ret, img = cap.read()


        img = cv2.resize(img, (640, 480))
        img,pg = detect.find_face(img)
        # print(pg)
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.imshow('Face', img)

        if cv2.waitKey(1) & 0XFF == ord('x'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__=="__main__":
    main()


