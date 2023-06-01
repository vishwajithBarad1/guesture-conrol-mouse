
# Gesture-Based Mouse Control with Hand Detection and Audio Volume Adjustment

This program enables mouse control through hand gestures. It uses a webcam feed and libraries like cv2, mediapipe, pyautogui, ctypes, and pycaw. Hand landmarks are detected, and finger distances are calculated to perform actions like left-click, right-click, mouse movement, and dragging. It differentiates between left and right hand gestures and adjusts audio volume. The program provides a hands-free alternative to traditional mouse input methods.


## Installation

Install libraries for the project using pip

```bash
  pip install cv2
  pip install mediapipe
  pip install pyautogui
  pip install pycaw

```
    
## Demo
bellow is the link to demo video

[![IMAGE ALT TEXT HERE](https://i.ibb.co/VLxD1BV/thumbnail.jpg)](https://youtu.be/smaINSCbzlw)
![Alt text](https://i.ibb.co/bRtcyJS/Screenshot-2023-05-26-020453.png)

## About this Project

The purpose of the program is to control the mouse using hand gestures. It uses the right hand gestures for left-click, right-click, mouse movement, and dragging operations, while also providing some functionality for the left hand. The program utilizes several libraries including time, cv2, mediapipe, pyautogui, ctypes, and pycaw.

The webcam feed is obtained using the cv2 library and processed by passing the frames through the hand detection model provided by the mediapipe library. This allows the program to detect and extract hand landmarks from the frames.

The finger distances are calculated using a simple mathematical formula to measure the distance between two points on the hand. These distances are then used to determine the appropriate mouse click operations based on the hand gestures.

The left or right hand is determined by analyzing the position of the thumb tip location and the pinky finger location. This information helps differentiate between left and right hand gestures.

Based on the hand detection and finger positions, various actions are performed. For example, left-click and right-click operations are triggered by specific finger distance values. Mouse movement is achieved by tracking the relative movement of the hand. Additionally, dragging operations are initiated when specific finger positions are detected.

The audio volume is adjusted using the pycaw library by mapping the mid value of the index and thumb tip positions to the desired volume level.

To ensure smooth interaction, there is a 0.1-second time delay between actions.

The overall structure of the program revolves around a while loop, where the frameOut() function is continuously called to obtain hand data from the webcam feed. The program does not display the reference video output for convenience.

Overall, this program provides an intuitive way to control the mouse using hand gestures, offering a hands-free alternative to traditional mouse input methods.

