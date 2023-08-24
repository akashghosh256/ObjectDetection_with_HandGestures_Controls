# Object Detection and Hand Gesture Volume Control

This project combines object detection using CVLIB and hand gesture volume control using OpenCV, HandTrackingModule, and the pycaw library. The program captures video from the webcam, detects objects in the video stream, and controls the system's volume based on hand gestures.

## Installation

To run this project, you need to install the following dependencies:

1. OpenCV: `pip install opencv-contrib-python`
2. numpy: `pip install numpy`
3. comtypes: `pip install comtypes`
4. pycaw: `pip install pycaw` https://github.com/akashghosh256/ObjectDetection_with_HandGestures_Controls/blob/main/README.md
For controlling audio volume, this project uses the `pycaw` library. You can find more information about the library and its usage on its GitHub repository: [https://github.com/AndreMiras/pycaw](https://github.com/AndreMiras/pycaw)
5. cvlib: `pip install cvlib`
6. gTTS (Google Text-to-Speech): `pip install gTTS`
7. pygame: `pip install pygame`

## Usage

1. Clone the repository or download the main script files.
2. Install the required dependencies as mentioned above.
3. The repository also contains various folders that divide the project into different   parts, such as Object Detection and hand Tracking. You can run them individually to see how they work. But to run the main project, you need to open the `Main(Final)` folder and run the script from there.
4. Run the script using `python ObjectWithGesture(Main).py`.

## Features

- Object Detection: The program uses the `cvlib` library to detect common objects in the video stream and highlights them with bounding boxes.
- Hand Gesture Volume Control: The program uses hand tracking with the `HandTrackingModule` to detect hand gestures, allowing you to control the system's volume by moving your hand up and down.

## Instructions

1. Run the script using the command mentioned above.
2. The main window will display the webcam feed with object detection and hand gesture volume control.
3. To control the volume, move your hand vertically in front of the camera. The program will display the current volume level and adjust the system volume accordingly.
4. Detected objects will be highlighted with bounding boxes, and if a new object is detected, the system will announce it using text-to-speech.

## Troubleshooting

- If you encounter any issues with audio playback or hand tracking, ensure that your webcam and audio devices are properly connected and configured.
- Make sure that the necessary dependencies are installed, as mentioned in the "Installation" section.
- Could you make sure you have Python 3.7 or above installed?
- Could you make sure you have the latest version of pip installed?
- Check your internet connection.
- Make sure you have enough RAM and CPU to run the program. (It is required for better FPS and performance of the program)
