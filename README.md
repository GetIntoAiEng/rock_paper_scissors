# Rock_Paper_Scissors
Let's play Rock, Paper, Scissors with the computer by camara
## Introcduction
To be able to get deeper into AI and have some stuff to demonstrate to potential employers, I'd like to play a bit with hand gesture recognition.
Tags: Human-Computer Interaction (HCI) / Gesture Classification / hand gesture recognition 
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
- Github / MS Visual Coder / Jupiter Labs
- Python 3.12
- MediaPipe Hands (From Google)
  
## Stages of development
Let's start in the following way - one after another:
1. Get enviroment up and running
2. Let's get access to the webcam and move the picture to MediaPipe Hands an visualize that
3. Have a gesture detetion which is capable of detecting Rock, Paper, Scissors (Gesture Classification)
4. Add the game logic around that

## Folder structure

