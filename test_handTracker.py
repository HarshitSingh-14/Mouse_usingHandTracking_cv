import cv2
import time
import HandTrackingModule as htm


p_Time = 0
curr_Time = 0

cam = cv2.VideoCapture(0)

#  TEsT
detector = htm.handDetector()

while (True):
    success, img = cam.read()

    img = detector.findHands(img,draw = True )  # FUnction 1
    hand_lm = detector.findPosition(img , draw = False)
    if len(hand_lm) != 0:
        print(hand_lm[4])  # TIP of thumb

    # Frames per second
    curr_time = time.time()
    fps = 1 / (curr_time) - (p_Time)
    p_Time = curr_Time

    cv2.putText(img, str(int(self.number_of_hands)), (10, 60), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0),
                3)  # position , font, scale , colour, thickness

    cv2.imshow("Image", img)
    cv2.waitKey(1)