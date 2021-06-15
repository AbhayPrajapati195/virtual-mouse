import time
import math
import cv2
import mediapipe as mp
import pyautogui as pg
import numpy as np

cap = cv2.VideoCapture(0)
mpDraw = mp.solutions.drawing_utils
Mhands = mp.solutions.hands
hands = Mhands.Hands(min_detection_confidence = 0.7,
min_tracking_confidence = 0.5)
lmNameIndex = Mhands.HandLandmark
screen = pg.size()
width = screen.width
height = screen.height

max = 0
min = 2000
# tight click = 3.80 light click = 11.03

ss = pg.screenshot()

img = cv2.cvtColor(np.array(ss),cv2.COLOR_RGB2BGR)


def click():
    print(pg.position())
    pg.click()
    print("click")


pg.FAILSAFE = False

with hands as hands:
    while cap.isOpened:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        
        # print(results.multi_hand_landmarks)
        height, width, depth = img.shape
        if results.multi_hand_landmarks:
            for x in results.multi_hand_landmarks:
                print("tracking index finger....")
                indextip = [x.landmark[8].x * width, x.landmark[8].y * height]
                print(f"x: {x.landmark[8].x * width}")
                print(f"y: {x.landmark[8].y * height}")
                print(f"z: {x.landmark[8].z}")
                
                
                thumb = [x.landmark[4].x * width, x.landmark[4].y * height]
                
                dist = math.hypot(indextip[0]-thumb[0], indextip[1]-thumb[1])

                if max < dist:
                    max = dist
                
                if min > dist:
                    min = dist


                if dist < 20:
                    click()
                    pg.moveTo(indextip[0], indextip[1], duration= 0.5)
                
                    exit()


              
              
              
                # reference for other landmark accessing options
                # print("tracking thumb....")
                # print(f"x: {x.landmark[Mhands.HandLandmark.THUMB_TIP].x * width}")
                # print(f"y: {x.landmark[Mhands.HandLandmark.THUMB_TIP].y * height}")


                # print the min and max of the detection


                
                mpDraw.draw_landmarks(img,x)                

        cv2.imshow("image", img)
        cv2.waitKey(1)
        
        print()
        print(f"max: \nx: {max}\nmin: {min}\n")
        