import cv2
import mediapipe as mp
import time
from mediapipe.python.solutions.hands_connections import HAND_CONNECTIONS




# Creating Class

class handDetector():
    def __int__(self,mode=False,maxHands=2,detection_confidence=0.5,tracking_confidence=0.5 ):
        self.mode = mode
        self.maxHands = self.maxHands
        self.detection_confidence = self.detection_confidence
        self.tracking_confidence = self.tracking_confidence
        self.mediapipe_hands = mp.solutions.hands
        self.hands = self.mediapipe_hands.Hands(self.mode, self.maxHands, self.detection_confidence, self.tracking_confidence)
        self.mp_drawing = mp.solutions.drawing_utils

    def findHands(self, img, draw = True):
    # Time inialisation

        img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(img_RGB)

        # print(result.multi_hand_landmarks)

        # Multiple Hands
        self.number_of_hands= 0
        if (self.result.multi_hand_landmarks):
            for hands_count in self.result.multi_hand_landmarks:
                number_of_hands = number_of_hands+1
                # Landmarks _boxes
                if(draw):

                    self.mp_drawing.draw_landmarks(self.img, self.hands_count, self.HAND_CONNECTIONS)
        return img


    def findPositions(self, img, handNo= 0, draw = True):
        hand_lm=[] # for landmarks
        if self.result.multi_hand_landmarks:
            my_hand = self.result.multi_hand_landmarks[handNo]
            for id, land_mark in enumerate(my_hand.landmark):  # id from 1  - 21 point

                # print(id, land_mark)  # gives the ratio --> convert to
                # shAPING->
                h, w, c = img.shape
                cx, cy = int(land_mark.x * w), int(land_mark.y * h)
                # print(id, cx, cy)
                hand_lm.append([id, cx, cy])

                if id == 0:
                    cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)


def main():
    p_Time = 0
    curr_Time = 0

    cam = cv2.VideoCapture(0)

    #  TEsT
    detector = handDetector()


    while (True):
        success, img = cam.read()

        img =detector.findHands(img)      # FUnction 1
        hand_lm= detector.findPosition(img)
        if len(hand_lm) !=0:
            print(hand_lm[4]) # TIP of thumb

        # Frames per second
        curr_time = time.time()
        fps = 1 / (curr_time) - (p_Time)
        p_Time = curr_Time

        cv2.putText(img, str(int(self.number_of_hands)), (10, 60), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255),
                    3)  # position , font, scale , colour, thickness

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ =="__main__":
    main()