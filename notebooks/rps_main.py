


### I N C L U D E S ###########################################################
import cv2
import mediapipe as mp
import time
import sys
import os

### "C O N S T A N T S" #######################################################
SCORE_FONT_COLOR  = (255, 255, 255)
SCORE_FONT_SIZE   = .8
TIMER_VAL_EXP     = 1.2

### F U N C T I O N s #########################################################

#------------------------------------------------------------------------------
# This funtion checks which of the gestures are present in an given landmark
# INPUT: hand_landmarks - the hands landmark
# OUTPUT: the gesture as a string
#       - "rock"
#       - "paper"
#       - "cissors"
#       - "unkown"
def detect_gesture(hand_landmarks):
    tips_ids = [4, 8, 12, 16, 20]
    pip_ids = [3, 6, 10, 14, 18]
    fingers = []

    if hand_landmarks.landmark[tips_ids[0]].x < hand_landmarks.landmark[pip_ids[0]].x:
        fingers.append(1)
    else:
        fingers.append(0)

    for i in range(1, 5):
        if hand_landmarks.landmark[tips_ids[i]].y < hand_landmarks.landmark[pip_ids[i]].y:
            fingers.append(1)
        else:
            fingers.append(0)

    print("Finger states:", fingers)

    if sum(fingers[1:]) <= 1:
        return "rock"
    elif sum(fingers[1:]) >= 4:
        return "paper"
    elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
        return "scissors"
    else:
        return "unknown"

#------------------------------------------------------------------------------
# this fct grabs into the camera and reads a frame. The frame is given to 
# mediapipe in oder to get a landmark of the given fingers
# the score is added to the image and then
# it is retuned
def create_image(cap):

    global score_human, score_pc

    with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:

        ret, frame = cap.read()
        if not ret:
            return
    
        # preapare MediaPipe
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Print Hand-Landmarks 
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        
        score_text = f"Human: {score_human} vs PC: {score_pc}"
        cv2.putText(image, score_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, SCORE_FONT_SIZE, SCORE_FONT_COLOR, 2, cv2.LINE_AA)

        return image



#++ State Machine +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Check ReadMe to get mre insigts whtas going on here

#------------------------------------------------------------------------------
# in the run state we just show the output of the webcam and add the current 
# score. Based on the key which are read we change within the StM, but better 
# read the readme...
def state_run(cap):
    
    global countdown_start, score_human, score_pc

    image = create_image(cap)
    cv2.putText(image, 'Press "S" to start', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, SCORE_FONT_SIZE, SCORE_FONT_COLOR, 2, cv2.LINE_AA)
    cv2.imshow("Rock-Paper-Scissors", image)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        print("STATE: will move to COUNT")
        countdown_start = time.time()
        return "count"
    elif key == ord('r'):
        score_pc    = 0
        score_human = 0
    elif key == 27:  # ESC
        print("STATE: will move to ESC")
        return "exit"
    return "run"


#------------------------------------------------------------------------------
# the game was started and now we count. one, two, three, GO!
# with GO we want to verify the gesture we've captured and move therefore to 
# the next state
def state_count(cap):

    global countdown_start, countdown_index
    countdown_texts = ["OK!!", "ONE", "TWO", "GO!"]

    
    elapsed = time.time() - countdown_start
    countdown_index = int(elapsed // TIMER_VAL_EXP)


    image = create_image(cap)

    if countdown_index < len(countdown_texts):
        text = countdown_texts[countdown_index]
        h, w, _ = image.shape
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 3
        thickness = 6
        color = (255, 255, 255)
        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
        x = (w - text_width) // 2
        y = (h + text_height) // 2
        cv2.putText(image, text, (x, y), font, font_scale, color, thickness, cv2.LINE_AA)
        cv2.imshow("Rock-Paper-Scissors", image)
        cv2.waitKey(1)
        return "count"
    else:
        print("STATE: will move to VERIFY")
        return "verify"


#------------------------------------------------------------------------------
# with verify we grab one window and get the gesture and based on a random 
# number, we do calculate the 
def state_verify(cap):
    global score_human, score_pc

    with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Could not read frame.")
            return "exit"

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        gesture = "unknown"
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                gesture = detect_gesture(hand_landmarks)
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # PC will pick a random joice
        import random
        pc_gesture = random.choice(["rock", "paper", "scissors"])

        # Do the game game evaluation
        if gesture == pc_gesture:
            result_text = "Draw!"
        elif gesture == "unknown":
            result_text = "Let's do it again"
        elif (gesture == "rock" and pc_gesture == "scissors") or \
             (gesture == "paper" and pc_gesture == "rock") or \
             (gesture == "scissors" and pc_gesture == "paper"):
            score_human += 1
            result_text = "You win!"
        else:
            score_pc += 1
            result_text = "PC wins!"

        # Add it to the frame
        cv2.putText(image, f"You: {gesture}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, SCORE_FONT_COLOR, 2)
        cv2.putText(image, f"PC: {pc_gesture}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, SCORE_FONT_COLOR, 2)
        cv2.putText(image, result_text, (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, SCORE_FONT_COLOR, 2)
        cv2.imshow("Rock-Paper-Scissors", image)
        cv2.waitKey(2000)  # 2 Sekunden anzeigen

    return "run"

#------------------------------------------------------------------------------
def state_exit(cap):
    print("Exiting game. Bye!")
    return None

#------------------------------------------------------------------------------
def run_fsm(cap):
    state = "run"
    while state:
        state_fn = states[state]
        state = state_fn(cap)


### G L O B A L S #############################################################

mp_hands   = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

countdown_start = 0
countdown_index = 0

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # TensorFlow/MediaPipe-Warnungen unterdrücken

states = {
    "run": state_run,
    "count": state_count,
    "verify": state_verify,
    "exit": state_exit
}

score_human = 0
score_pc    = 0

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

### M A I N ###################################################################
if __name__ == "__main__":

    cap = cv2.VideoCapture(0)                       # Let's activat the camaera
    if not cap.isOpened():
        sys.exit("ERROR: Camara couldn't be accessed")

    run_fsm(cap)

    cap.release()
    cv2.destroyAllWindows()
