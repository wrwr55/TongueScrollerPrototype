
Dependencies:

pip install opencv-python mediapipe numpy pyautogui


MUST HAVE A WEBCAM TO USE:

This project allows users to scroll through sites and use features such as Instagram Reels without any us of the hands. 

Setup: Download dependencies (listed at the top), run the program in an editor such as VSCode, click on the browser tab that you want to control.

Tracking: Tracks facial landmarks created by using MediaPipe's Face Mesh and primarily focuses on two points: the upper lip and the bottom of the chin.

Triggering: Conintuously monitoring the "red ratio" (which is the proportion of bright red and orange pixels) around these points and if it detects a spike above the custom baseline it interprets this as a gesture:
  Upper lip spike = Up "arrow" key press
  Chin spike = down "arrow" key press

Don't forget to install all dependencies!
