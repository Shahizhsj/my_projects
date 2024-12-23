import cv2
import mediapipe as mp
import random
import math

points = []
lengths = []
current_len = 0
total_allowd_len = 10
prv = 0, 0


def is_point_on_line(x1, y1, x2, y2, px, py):
    left_side = (py - y1) * (x2 - x1)
    right_side = (y2 - y1) * (px - x1)

    if left_side != right_side:
        return False

    if min(x1, x2) <= px <= max(x1, x2) and min(y1, y2) <= py <= max(y1, y2):
        return True

    return False


mp_hands = mp.solutions.hands


def dis(p_1, p_2):
    x_1, y_1 = p_1
    x_2, y_2 = p_2
    return math.sqrt(((x_2 - x_1) ** 2) + ((y_2 - y_1) ** 2))


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
score = 0
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
center_x = random.randint(50, width - 50)
center_y = random.randint(50, height - 50)

with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        cv2.circle(image, (center_x, center_y), 10, (0, 0, 200), -1)

        lml = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, _ = image.shape
                    xc, yc = int(lm.x * w), int(lm.y * h)
                    lml.append([id, xc, yc])

        try:
            if lml:
                x1, y1 = lml[8][1], lml[8][2]
                prev_x, prev_y = prv
                c_x, c_y = x1, y1
                points.append([c_x, c_y])
                distance = math.hypot(c_x - prev_x, c_y - prev_y)
                lengths.append(distance)
                current_len += distance
                prv = c_x, c_y

                if current_len > total_allowd_len:
                    for i, length in enumerate(lengths):
                        current_len -= length
                        lengths.pop(i)
                        points.pop(i)
                        if current_len < total_allowd_len:
                            break

                if len(points) > 3 and is_point_on_line(
                        points[0][0], points[0][1], points[-2][0], points[-2][1], points[-1][0], points[-1][1]):
                    print("Game Over!")
                    break

                for i, point in enumerate(points):
                    if i != 0:
                        cv2.line(image, points[i - 1], points[i], (10, 25, 255), 20)
                cv2.circle(image, points[-1], 20, (200, 200, 200), cv2.FILLED)

                if dis((x1, y1), (center_x, center_y)) <= 50:
                    score += 10
                    center_x = random.randint(20, width - 50)
                    center_y = random.randint(20, height - 50)
                    total_allowd_len += 10

        except Exception as e:
            print("Error:", e)
            pass

        score_text = f"Score: {score}"
        cv2.putText(
            image,
            score_text,
            (width // 2 - 100, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0, 255, 255),
            3,
            cv2.LINE_AA
        )
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
