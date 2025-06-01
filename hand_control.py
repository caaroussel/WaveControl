import cv2
import mediapipe as mp
import math
import wave_control
import queue

def run_hand_tracking(image_queue=None):
    mp_hands = mp.solutions.hands
    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    h, w, _ = image.shape
                    thumb_tip = hand_landmarks.landmark[4]
                    index_tip = hand_landmarks.landmark[8]

                    dx = index_tip.x - thumb_tip.x
                    dy = index_tip.y - thumb_tip.y
                    dist = math.sqrt(dx**2 + dy**2)

                    wave_control.amplitude_base = 20 + 100 * dist
                    wave_control.frequency_base = 10 + 30 * dist

                    thumb_pos = (int(thumb_tip.x * w), int(thumb_tip.y * h))
                    index_pos = (int(index_tip.x * w), int(index_tip.y * h))
                    cv2.line(image, thumb_pos, index_pos, (255, 0, 0), 2)

            if image_queue:
                try:
                    preview = cv2.resize(image, (320, 240))
                    image_queue.put_nowait(preview)
                except queue.Full:
                    pass

    cap.release()
