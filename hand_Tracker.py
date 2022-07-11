import cv2
import mediapipe as mp
import time
from mediapipe.python.solutions.hands_connections import HAND_CONNECTIONS

cam = cv2.VideoCapture(0)

# initiation
mediapipe_hands = mp.solutions.hands
hands = mediapipe_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Time inialisation
p_Time = 0
curr_Time = 0

while (True):
    # Camera Setup
    success, img = cam.read()

    img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_RGB)

    # print(result.multi_hand_landmarks)

    # Multiple Hands
    number_of_hands= 0
    if (result.multi_hand_landmarks):
        for hands_count in result.multi_hand_landmarks:
            number_of_hands = number_of_hands+1
            # Landmarks _boxes
            for id, land_mark in enumerate(hands_count.landmark):   # id from 1  - 21 point

                # print(id, land_mark)  # gives the ratio --> convert to
                # shAPING->
                h, w, c = img.shape
                cx , cy = int(land_mark.x * w) , int(land_mark.y * h)
                print(id, cx, cy)

                if id == 0:
                    cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)


            mp_drawing.draw_landmarks(img, hands_count, HAND_CONNECTIONS)

    # Frames per second
    curr_time = time.time()
    fps = 1 / (curr_time) - (p_Time)
    p_Time = curr_Time

    cv2.putText(img, str(int(number_of_hands)), (10, 60), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 255), 3)  #position , font, scale , colour, thickness

    cv2.imshow("Image", img)
    cv2.waitKey(1)
