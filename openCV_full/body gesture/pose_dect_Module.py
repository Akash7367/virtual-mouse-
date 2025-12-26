import cv2
import numpy as np
import mediapipe as mp
import time
import math


class PoseDetect():
    def __init__(self, mode=False, smooth=True, model_complexity=1,
                 detect_conf=0.5, track_conf=0.5):
        self.mode = mode
        self.smooth = smooth
        self.model_complexity = model_complexity
        self.detect_con = detect_conf
        self.track_con = track_conf

        # Initialize Mediapipe Pose model
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=self.mode,
            model_complexity=self.model_complexity,
            smooth_landmarks=self.smooth,
            min_detection_confidence=self.detect_con,
            min_tracking_confidence=self.track_con
        )
        self.mp_draw = mp.solutions.drawing_utils

    def FindPose(self, img, draw=True):

        img_cvt = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(img_cvt)

        if self.results.pose_landmarks:
            if draw:
                self.mp_draw.draw_landmarks(img, self.results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        return img

    #now get all poosition and put in a list
    def get_pos(self,img,draw):
        self.l=[]
        if self.results.pose_landmarks:
            for id,lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c = img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                self.l.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),5,(255,0,255),cv2.FILLED)
        return self.l

    def find_angle(self,img,p1,p2,p3,draw=True):

        # to get landmarks
        x1,y1 = self.l[p1][1:]#[1:] means we need only x and y value not id
        x2,y2 = self.l[p2][1:]
        x3,y3 = self.l[p3][1:]

        #to calculate angle
        # this will calculate angle between three points
        angle1 = math.atan2(y1-y2,x1-x2)
        angle2 = math.atan2(y3-y2,x3-x2)

        theta = abs(angle1-angle2)
        angle = math.degrees(theta)


        # if angle<0:
        #     angle+=360
        # print(x1,y1)
        # print(x2,y2)
        # print(x3,y3)
        # print(angle)

        # to draw or visiualize
        if draw:
            cv2.circle(img, (x1, y1), 6, (0, 0, 255), -1)
            cv2.circle(img, (x2, y2), 6, (0, 0, 255), -1)
            cv2.circle(img, (x3, y3), 6, (0, 0, 255), -1)

            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)

            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.line(img, (x2, y2), (x3, y3), (0, 255, 0), 2)

            cv2.putText(img,f'{int(angle)}',(x2+20,y2+10),cv2.FONT_HERSHEY_PLAIN,3,(255,255,0),3)

        return angle

def main():
    cap = cv2.VideoCapture(r"C:\Users\akash\PycharmProjects\Open CV\video\2.mp4")  # Change the path to your video file
    ptime = 0
    detector = PoseDetect()
    while True:
        ret, img = cap.read()
        if not ret:
            break  # Exit if video is over
        img = cv2.resize(img, (640, 480))
        img = detector.FindPose(img, True)

        li=detector.get_pos(img,True)
        # track any specific point
        if len(li)!=0:
            cv2.circle(img,(li[12][1],li[12][2]),10,(255,255,0),cv2.FILLED)

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow("Video", img)

        if cv2.waitKey(1) & 0xFF == ord('x'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
