import cv2
import time
import numpy as np
import handTrack_Module as htm
# import autopy
import pyautogui
import subprocess
import webbrowser
# import image_search as ims

###################################3####
wcam,hcam = 1200,720
frameR = 100 # this is frame reduction
wScr,hScr = pyautogui.size()# give the size of screen
smooth_value = 8 # when mouse is getting move then then it will flikker a lot hence we need to smoothing this
ptime=0
plocx,plocy=0,0#previous location of x
clocx,clocy=0,0#previous location of y
#########################################
# print(wScr,hScr)

cap = cv2.VideoCapture(0)
# cap=cv2.VideoCapture(r"C:\Users\akash\PycharmProjects\Open CV\video\1.mp4")
cap.set(3,wcam)
cap.set(4,hcam)

chrome_opened = False
detector = htm.handDetect(max_hand=1)
# img_sc = ims.image_search()


while True:
    ret,img = cap.read()

    # img= cv2.flip(img,1)
    # these are some steps to solve do this
    # 1. find hand_landmarks
    img = detector.find_hand(img)
    lms,bbox = detector.find_pos(img)

    if len(lms)!=0:
        # print(lms)
        # 2. get the tip of the index and middle fingers
        x1,y1 = lms[8][1:]
        x2,y2 = lms[12][1:]

        # 3.  check which finger are up
        finger=detector.fingerUp()
        # print(finger)
        cv2.rectangle(img,(frameR,frameR),(wcam-frameR,hcam-frameR),(255,0,255),2)

        # # search image when three fingers up
        # # time.sleep(2)
        # if finger[1]==1 and finger[2]==1 and finger[3]==1 and finger[4]==0:
        #     # time.sleep(4)
        #     img_sc.image_scan()

        # 4.  if index finger up means ->curser moving
        if finger[1]==1 and finger[2]==0:
            # print('index or middle finger up')
            pyautogui.FAILSAFE = False

            # 5. Convert Coordinatesx

            x3 = np.interp(x1,(frameR,wcam-300),(0,wScr))
            y3 = np.interp(y1,(frameR,hcam-300),(0,hScr))

            # 6. Smoothen Values
            clocx = plocx + (x3-plocx)/smooth_value
            clocy = plocy + (y3-plocy)/smooth_value

            # 7. Move Mouse
            # pyautogui.move(wScr-clocx,clocy)
            pyautogui.moveTo(wScr - clocx, clocy, duration=0.1)

            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)

            plocx,plocy = clocx,clocy

        # 8. if both index and middle finger up -> clicked
        if finger[1]==1 and finger[2]==1 and finger[3]==0:
            # print('index and middle both finger up')
            # 9. find distance between fingers
            length,img,lineinfo = detector.findDistance(img,8,12)
            # 10.Click mouse if distance short
            if length<40:
                cv2.circle(img,(lineinfo[4],lineinfo[5]),15,(0,255,255),cv2.FILLED)
                pyautogui.click()
                time.sleep(0.5)

        # Open Chrome when all fingers are up (Only Once)
        if 0 not in finger and not chrome_opened:
            chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            subprocess.Popen([chrome_path, "https://www.google.com"])
            chrome_opened = True  # Prevent multiple openings



        # Reset Chrome flag when fingers go down
        if 0 in finger:
            chrome_opened = False  # Allow opening again

    # 11.frame rates
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img, str(int(fps)),(30,50),cv2.FONT_HERSHEY_TRIPLEX,2,(255,0,0),2)

    # 12.Display
    cv2.imshow('mouse',img)

    if cv2.waitKey(1) & 0XFF == ord('x'):
        break

cv2.destroyAllWindows()
cap.release()

