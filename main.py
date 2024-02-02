import cv2
import mediapipe as mp
import smoothMouseControl
import numpy

import fps
import gesture

mouseControl = smoothMouseControl.control()

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(model_complexity=1,
                      min_detection_confidence=0.9,
                      min_tracking_confidence=0.01)
mpDraw = mp.solutions.drawing_utils

FPS = fps.fps()

while True:
    ret, img = cap.read()

    if (ret):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(imgRGB)

        if (result.multi_hand_landmarks):

            mainLandmark = result.multi_hand_landmarks[0]

            curGesture = gesture.gesturesName(
                gesture.analize(mainLandmark.landmark))

            print(curGesture)
            if (curGesture == "click"):
                mouseControl.mouseDown()
            elif (curGesture == "fist"):
                break
            else:
                mouseControl.mouseUp()

            handX = mainLandmark.landmark[9].x
            handY = mainLandmark.landmark[9].y
            handPosition = numpy.array((1 - handX, handY))
            # print(handPosition)
            handPosition = smoothMouseControl.mousePosScale(handPosition)
            # print(handPosition)
            mouseControl.pushPos(handPosition)

            for handLms in result.multi_hand_landmarks:
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
                # for i, lm in enumerate(handLms.landmark):
                #     print(i, lm.x, lm.y)

        curFps = FPS.get()
        cv2.putText(img, "fps: " + str(int(curFps)), (0, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)

        cv2.imshow("img", img)

    cv2KeyEvent = cv2.waitKey(1)
    if (cv2KeyEvent == ord('q')):
        break

    if (cv2KeyEvent == 27):
        break
