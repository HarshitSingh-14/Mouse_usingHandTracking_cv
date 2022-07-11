import autopy.screen
import cv2
import numpy as np
import time
# import autopy
import HandTrackingModule as htm

pTime =0
width_screen, height_screen = autopy.screen.size()
wcam =640
hcam= 480
frame_R = 190
#######***********SEnstivity
senst= 5
prev_location_X ,prev_location_Y  = 0,0
current_location_X, current_location_X =0,0
##### ***********


cap = cv2.VideoCapture(0)

cap.set(3, wcam)
cap.set(4, hcam)

detector = htm.handDetector(maxHands=1)








while(True):

    #1) Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox= detector.findPosition(img)


    #2) Tip of index
    if len(lmList)!=0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        print(x1,y1,x2,y2)
    # Display

    # 3) Checking which finger is up
    if len(lmList)!=0:
        fingers = detector.fingersUp()
        print(fingers)


    # 4) Only index finger up MOVING MODE
        if fingers[1]==1 and fingers[2]==0:
            # 5) Converting coordinates
            # Reduced
            cv2.rectangle(img,(frame_R, frame_R), (wcam-frame_R, hcam-frame_R), (255,0,0),2)
            # Matching screens
            x3= np.interp(x1, (frame_R,wcam-frame_R),(0,width_screen))
            y3= np.interp(y1, (frame_R,hcam-frame_R), (0,height_screen))
            # x3 = np.interp(x1, (0, wcam), (0, width_screen))
            # y3 = np.interp(y1, (0, hcam), (0, height_screen))

            # IN a specific rec [HIgh senstivity]   Senstivity fast
            current_location_X= prev_location_X +(x3- prev_location_X) / senst
            current_location_Y = prev_location_Y + (y3 - prev_location_Y) / senst


        # 5) Move mouse
            if (width_screen-current_location_X>0):
                autopy.mouse.move(width_screen-current_location_X, current_location_Y)

            prev_location_X, prev_location_Y= current_location_X, current_location_Y


        # 6) both finger up -> click
        if fingers[1]==1 and fingers[2]==1:
            length, img ,line_Info= detector.findDistance(8, 12,img)
            if length< 35 :
                cv2.circle(img , (line_Info[4], line_Info[5]), 15, (0,255, 0), cv2.FILLED)
                autopy.mouse.click()

    cTime = time.time()

    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 100, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
