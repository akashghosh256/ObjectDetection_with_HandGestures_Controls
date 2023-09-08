# Main File for Object Detection and Hand Gesture Volume Control
import cv2 as cv
import time
import numpy as np
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import cvlib as cvl
from cvlib.object_detection import draw_bbox
from gtts import gTTS
import pygame


wCam = 640
hCam = 480

cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# for fps calculation
pTime = 0  # previous time
cTime = 0  # current time
detected_objects = set()  # To store the names of detected objects, in object detection

detector = htm.handDetector(detectionCon=0.7) #dtectionCon = 0.7 means that the hand has to be 70% visible to be detected

# Github  repository: " pychaw " used for controling the volume of the device
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()   # Not required for this project
#volume.GetMasterVolumeLevel()  # Not required for this project
volRange = volume.GetVolumeRange()
#volume.SetMasterVolumeLevel(0, None)  # Not required for this project

minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

while True:
    # Code starts for volume control-------------------------------------------------------------------------------------------------------------
    success, img = cap.read()
    img = cv.flip(img, 1) # to avoid mirror effect, we flip the image
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist) != 0:
       # print(lmlist[4]) #print the position of the tip of the index finger
        x1, y1 = lmlist[4][1], lmlist[4][2] #x1 and y1 are the coordinates of the tip of the index finger
        x2, y2 = lmlist[8][1], lmlist[8][2] #x2 and y2 are the coordinates of the tip of the middle finger
        cx, cy = (x1+x2)//2, (y1+y2)//2 #cx and cy are the coordinates of the center of the line between the tip of the index finger and the tip of the middle finger

        cv.circle(img, (x1,y1), 15, (255, 0, 255), cv.FILLED) #draw a circle on the tip of the index finger  
        cv.circle(img, (x2,y2), 15, (255, 0, 255), cv.FILLED) #draw a circle on the tip of the middle finger
        cv.line(img, (x1,y1), (x2,y2), (255, 0, 255), 3) #draw a line between the tip of the index finger and the tip of the middle finger
        cv.circle(img, (cx,cy), 15, (255, 0, 255), cv.FILLED) #draw a circle on the center of the line between the tip of the index finger and the tip of the middle finger
        length = math.hypot(x2-x1, y2-y1) #calculate the length of the line between the tip of the index finger and the tip of the middle finger
       # print(length)

        # Hand range 50 - 300
        # Volume range -65 - 0
        vol = np.interp(length, [50,200], [minVol, maxVol]) #interpolate the length of the line between the tip of the index finger and the tip of the middle finger to the volume range
        volBar = np.interp(length, [50,250], [400, 120]) #interpolate the length of the line between the tip of the index finger and the tip of the middle finger to the volume bar range
        volPer = np.interp(length, [50,200], [0, 100]) #interpolate the length of the line between the tip of the index finger and the tip of the middle finger to the volume percentage range
        
        print(f'length: {int(length)}, volume: {int(volPer)}')
        volume.SetMasterVolumeLevel(vol, None)

        if length<50:
            cv.circle(img, (cx,cy), 15, (0, 255, 0), cv.FILLED)
            cv.putText(img,f' Muted', (10, 130), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        if length > 50 and length < 200:
           cv.putText(img,f' {int(volPer)}', (20, 130), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3) #print the volume percentage on the screen

        #adding a volume bar
        cv.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)

        # to make the volume bar move smoothly, we use cv.FILLED and to keep the volume bar in the range of 50 to 250, we use if statement
        if length < 200:
         cv.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv.FILLED)
        else:
          cv.rectangle(img, (50, 150), (85, 400), (255, 0, 0), cv.FILLED)
          cv.putText(img,f' Max Volume', (10, 130), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)



    #fps calculation
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv.putText(img,f'FPS: {int(fps)}', (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
   


# code starts for object detection-------------------------------------------------------------------------------------------------------------

    #ret, frame = cap.read()
    bbox, label, conf = cvl.detect_common_objects(img)
    output_image = draw_bbox(img, bbox, label, conf)

    cv.imshow("Object and Hand Gesture  Voulme Control", output_image)  # This line is added to show the object detection and hand gesture volume control in one window

    new_objects = set(label) - detected_objects  # Calculate new detected objects
    # This set is used to store only the name of new objects detected, to avoid the repetitive sound of the same object again and again (which can be annoying) 

    
    for obj_label in new_objects:
        print("New object detected:", obj_label)
        obj_label = "New object detected: "+obj_label
        language = "en"
        output = gTTS(text=obj_label, lang=language, slow=False)
        output.save("./sounds/output.mp3")
        
        pygame.init()

        # Load the MP3 file
        mp3_file = "./sounds/output.mp3"
        pygame.mixer.music.load(mp3_file)

       # Play the MP3
        pygame.mixer.music.play()

        # Allow time for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.delay(100)

        # Clean up resources
        pygame.quit()

        

    detected_objects.update(new_objects)  # Update the set of detected objects
    









   # cv.imshow("Object and Hand Gesture  Voulme Control", output_image)
    if cv.waitKey(1) == ord('q'):
        break



cap.release()
cv.destroyAllWindows()















