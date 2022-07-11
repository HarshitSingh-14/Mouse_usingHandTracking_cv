import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume   # for using volume with this
import cv2


# SCREEN Size
wCam, hCam = 1080, 720
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0


# VOLUME RANGE SETUP
detector = htm.handDetector(detectionCon=0.8)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()  # -65 ,0 -> conversion needed****


minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0





while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)



    # MAIN PART
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])

        # iNdex 4 for thumb and 8 for index
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # to confirm
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)

        # line joining,
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)       # length
        # print(length)




# FIXING ACORding  to THE LENGTH ...
        # Hand range 50 - 230
        vol = np.interp(length, [50, 230], [minVol, maxVol])
        volBar = np.interp(length, [50, 230], [400, 150])
        volPer = np.interp(length, [50, 230], [0, 100])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)


        # Side volume BAR
        if length <50:
            cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)
    cv2.rectangle(img, (900, 150), (950, 400), (0, 255, 0), 3)    #initial position  ENDING POSITION   colour
    cv2.rectangle(img, (900, int(volBar)), (950, 400), (100, 105, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 50, 0), 3)


    # Fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime




    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (0, 0, 255), 3)
    cv2.imshow("Img", img)
    cv2.waitKey(1)