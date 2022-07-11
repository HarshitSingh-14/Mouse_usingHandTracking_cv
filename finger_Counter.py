import cv2
import time
import os
import HandTrackingModule as htm

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionCon=0.75)
tipIds = [4,8, 12, 16, 20]

pTime = 0

folderPath = "finger_counting"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')


    # # RESIzing image
    width = int(200)
    height = int(200)
    dim = (width, height)
    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    # print(f'{folderPath}/{imPath}')
    overlayList.append(image)
    image.size


print(len(overlayList))


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList , bbow = detector.findPosition(img, draw=False)



    tipIds = [4, 8, 12, 16, 20]

    if len(lmList) != 0:
        fingers = []
        # Thumb to the left and write x axis
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:

            fingers.append(1)
        else:
            fingers.append(0)
        # 4 Fingers  ---> to up or loweer of two index bottom
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)



    # Image

        h, w, c = overlayList[totalFingers - 1].shape

        #
        img[0:h, 0:w] = overlayList[totalFingers - 1]
        #
        #
        cv2.putText(img, str(totalFingers), (500, 405), cv2.FONT_HERSHEY_PLAIN,
                    4, (0, 255, 0), 5)




# TIme
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400,50 ), cv2.FONT_HERSHEY_PLAIN,
                2, (0, 255, 255), 2)



    cv2.imshow("Image", img)
    cv2.waitKey(1)
