import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

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

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                h, w, _ = image.shape
                thumb_tip = hand_landmarks.landmark[4]
                index_tip = hand_landmarks.landmark[8]

                thumb_pos = (int(thumb_tip.x * w), int(thumb_tip.y * h))
                index_pos = (int(index_tip.x * w), int(index_tip.y * h))

                # Couleurs différentes selon la main
                label = handedness.classification[0].label
                if label == 'Left':
                    thumb_color = (255, 255, 255)  # Blanc
                    index_color = (0, 0, 0)   # Noir
                else:
                    thumb_color = (0, 0, 255)   # Rouge
                    index_color = (255, 0, 0) # Bleu 

                cv2.circle(image, thumb_pos, 10, thumb_color, -1)
                cv2.circle(image, index_pos, 10, index_color, -1)
                cv2.line(image, thumb_pos, index_pos, (255, 0, 0), 3)

                cv2.putText(image, f'Thumb: {thumb_pos}', (thumb_pos[0] + 10, thumb_pos[1] - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, thumb_color, 1)
                cv2.putText(image, f'Index: {index_pos}', (index_pos[0] + 10, index_pos[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, index_color, 1)

        cv2.imshow('Main Tracker', image)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
