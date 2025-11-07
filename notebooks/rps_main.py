import cv2
import mediapipe as mp


mp_hands   = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils



def live_hand_tracking():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Fehler: Kamera konnte nicht geöffnet werden.")
        return

    with mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ) as hands:

        print("Handtracking gestartet. Drücke ESC zum Beenden.")
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Bild für MediaPipe vorbereiten
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)

            # Zurück zu BGR für OpenCV
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Zeichne Hand-Landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            cv2.imshow("MediaPipe Hands", image)

            if cv2.waitKey(1) & 0xFF == 27:  # ESC
                break

    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    print("Script läuft!")
    frame = live_hand_tracking()
    if frame is not None:
        print("Bild erfolgreich aufgenommen!")