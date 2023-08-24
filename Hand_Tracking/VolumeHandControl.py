import cv2 as cv
import time
import numpy as np
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam = 640
hCam = 480

cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# for fps calculation
pTime = 0  # previous time
cTime = 0  # current time

detector = htm.handDetector(detectionCon=0.7)
#dtectionCon = 0.7 means that the hand has to be 70% visible to be detected

# Github pycaw

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
#volume.SetMasterVolumeLevel(0, None)
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

while True:
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
        
        print(f'length: {int(length)}, vol: {vol}')
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


    
    cv.imshow("Image", img)
    if cv.waitKey(1) == ord('q'):
        break


















