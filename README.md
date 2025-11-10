# Rock_Paper_Scissors
Let's play Rock, Paper, Scissors with the computer by camara
## Introcduction
To be able to get deeper into AI and have some stuff to demonstrate to potential employers, I'd like to play a bit with hand gesture recognition.
Tags: Human-Computer Interaction (HCI) / Gesture Classification / hand gesture recognition 

## How to play it 
1. Press "s" to start or "ESC " to abbort
2. PC will count 1, 2, GO!. With "GO!" show what you've got (I recomend to have your hand shown in an horizontal way)
3. PC will tell you its solution and calculate the winner 
4. Press "s" to start or "ESC " to abbort - "r" will reset the score

## How it should work
After counting "3, 2, 1, Go!" The gesture of the hand, taken by the camara of the PC, shall be analyzed for the gestures
- Stone    - a fist
- Paper    - open hand
- Scissors - Index and middle fingers extended to form a "V" - Other fingers curled in, or
- not detected
and be compared with a random value from the computer.
The Winner would be
- Stone beats Scissors,
- Scissory beats Paper,
- Paper beats Stone

## Tech Stack To Be Used
- Github / MS Visual Coder
- **Python 3.12** (pls check requirements.txt for the used versions)
    -> OpenCV
    -> Numpy
    -> MediaPipe Hands (From Google)
  
## Stages of development
Let's start in the following way - one after another:
1. Get enviroment up and running
2. Let's get access to the webcam and move the picture to MediaPipe Hands an visualize that
3. Have a gesture detetion which is capable of detecting Rock, Paper, Scissors (Gesture Classification)
4. Add the game logic around that

## Main Statemachine (StM)
![Main Satemachine](additionals/StM.jpg)

### States

#### RUN
The current game score is visible in the upper right corner Human: X - PC: Y 
"Press 'G' to start" is visible in the middle of the screen
In RUN State the Camera output is shown, both hands are shown with grids

#### COUNT
The current game score is visible in the upper right corner Human: X - PC: Y
In the count state the text ONE - TWO - THREE - GO! is shown for each 1.2sec
After this time we jump to to verify

#### VERIFY
The Picture is frozen. 
The Gesture is detected (Rock, Paper, Scissors, Don't Know)
A random algorithm is returning the computers bet (Rock, Paper, Scissors)
An Output is created and moved on the Screen
The current game score is updated and visible in the upper right corner Human: X - PC: Y

### Transitions
#### Into RUN
Jump into RUN state 
- after program start
- after the output was shown for 5 seconds

#### RUN -> COUNT
If key 'g' (for GO!) was pressed

#### COUNT -> VERIFY
if "GO!" was shown for 1.2 sec 

#### VERIFY -> RUN
after result was shown for 5 sec

#### RUN -> EXIT
if key 'ESC' was selected

## Folder structure

