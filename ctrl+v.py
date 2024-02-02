import cv2
import mediapipe as mp
import math


# 針對給定的某個矩形做馬賽克
def mosaic(img, left_up, right_down):
    new_img = img.copy()
    # size代表此馬賽克區塊中每塊小區域的邊長
    size = 10
    for i in range(left_up[1], right_down[1] - size - 1, size):
        for j in range(left_up[0], right_down[0] - size - 1, size):
            try:
                # 將此小區域中的每個像素都給定為最左上方的像素值
                new_img[i:i + size, j:j + size] = img[i, j, :]
            except:
                pass
    return new_img


def vector_2d_angle(v1, v2):  # 求出v1,v2兩條向量的夾角
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_ = math.degrees(
            math.acos(
                (v1_x * v2_x + v1_y * v2_y) / (((v1_x**2 + v1_y**2)**0.5) *
                                               ((v2_x**2 + v2_y**2)**0.5))))
    except:
        angle_ = 100000.
    return angle_


def hand_angle(hand_):
    angle_list = []
    #---------------------------- thumb 大拇指角度
    angle_ = vector_2d_angle(((int(hand_[0][0]) - int(hand_[2][0])),
                              (int(hand_[0][1]) - int(hand_[2][1]))),
                             ((int(hand_[3][0]) - int(hand_[4][0])),
                              (int(hand_[3][1]) - int(hand_[4][1]))))
    angle_list.append(angle_)
    #---------------------------- index 食指角度
    angle_ = vector_2d_angle(((int(hand_[0][0]) - int(hand_[6][0])),
                              (int(hand_[0][1]) - int(hand_[6][1]))),
                             ((int(hand_[7][0]) - int(hand_[8][0])),
                              (int(hand_[7][1]) - int(hand_[8][1]))))
    angle_list.append(angle_)
    #---------------------------- middle 中指角度
    angle_ = vector_2d_angle(((int(hand_[0][0]) - int(hand_[10][0])),
                              (int(hand_[0][1]) - int(hand_[10][1]))),
                             ((int(hand_[11][0]) - int(hand_[12][0])),
                              (int(hand_[11][1]) - int(hand_[12][1]))))
    angle_list.append(angle_)
    #---------------------------- ring 無名指角度
    angle_ = vector_2d_angle(((int(hand_[0][0]) - int(hand_[14][0])),
                              (int(hand_[0][1]) - int(hand_[14][1]))),
                             ((int(hand_[15][0]) - int(hand_[16][0])),
                              (int(hand_[15][1]) - int(hand_[16][1]))))
    angle_list.append(angle_)
    #---------------------------- pink 小拇指角度
    angle_ = vector_2d_angle(((int(hand_[0][0]) - int(hand_[18][0])),
                              (int(hand_[0][1]) - int(hand_[18][1]))),
                             ((int(hand_[19][0]) - int(hand_[20][0])),
                              (int(hand_[19][1]) - int(hand_[20][1]))))
    angle_list.append(angle_)
    return angle_list


def hand_gesture(angle_list):
    gesture_str = None
    if 100000. not in angle_list:
        if (angle_list[1] > 40) and (angle_list[2]
                                     < 40) and (angle_list[3]
                                                > 40) and (angle_list[4] > 40):
            gesture_str = "middle"
    return gesture_str


def detect():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False,
                           max_num_hands=1,
                           min_detection_confidence=0.75,
                           min_tracking_confidence=0.75)
    # 開啟視訊鏡頭讀取器
    cap = cv2.VideoCapture(0)
    while True:
        # 偵測影像中的手部
        _, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        results = hands.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                keypoint_pos = []
                for i in range(21):
                    x = hand_landmarks.landmark[i].x * frame.shape[1]
                    y = hand_landmarks.landmark[i].y * frame.shape[0]
                    keypoint_pos.append((x, y))
                if keypoint_pos:
                    # 得到各手指的夾角資訊
                    angle_list = hand_angle(keypoint_pos)
                    # 根據角度判斷此手勢是否為中指
                    gesture_str = hand_gesture(angle_list)
                    if gesture_str == "middle":
                        for node in range(9, 13):
                            center_x = int(keypoint_pos[node][0])
                            center_y = int(keypoint_pos[node][1])
                            frame = mosaic(frame,
                                           [center_x - 15, center_y - 10],
                                           [center_x + 30, center_y + 50])
        cv2.imshow('MediaPipe Hands', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()


if __name__ == '__main__':
    detect()
