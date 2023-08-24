import os
import cv2 as cv
import cvlib as cvl
from cvlib.object_detection import draw_bbox
from gtts import gTTS
import pygame
import time

# Initialize previous time (pTime) and current time (cTime) for FPS calculation
pTime = 0
cTime = 0

# Open the default camera (camera index 0)
video = cv.VideoCapture(0)

# Set to store the names of detected objects
detected_objects = set()

# Infinite loop for real-time object detection
while True:
    # Read a frame from the video feed
    ret, frame = video.read()
    frame = cv.flip(frame, 1)
    
    # Detect common objects in the frame using cvlib
    bbox, label, conf = cvl.detect_common_objects(frame)
    
    # Draw bounding boxes and labels on the frame
    output_image = draw_bbox(frame, bbox, label, conf)
    
    # Calculate FPS (Frames Per Second)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    
    # Display the FPS on the frame
    cv.putText(frame, f'FPS: {int(fps)}', (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    
    # Show the frame with object detection results
    cv.imshow("Real-time object detection", output_image)
    
    # Calculate new detected objects
    new_objects = set(label) - detected_objects
    
    # Process new detected objects
    for obj_label in new_objects:
        print("New object detected:", obj_label)
        
        # Convert object label to speech and save as an MP3 file
        obj_label = "New object detected: " + obj_label
        language = "en"
        output = gTTS(text=obj_label, lang=language, slow=False)
        output.save("./sounds/output.mp3")
        
        # Initialize and play the MP3 audio using Pygame
        pygame.init()
        mp3_file = "./sounds/output.mp3"
        pygame.mixer.music.load(mp3_file)
        pygame.mixer.music.play()
        
        # Allow time for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.delay(100)
        
        # Clean up resources
        pygame.quit()

    # Update the set of detected objects
    detected_objects.update(new_objects)
    
    # Exit the loop if 'q' key is pressed
    if cv.waitKey(1) == ord('q'):
        break

# Release the video feed and close all windows
video.release()
cv.destroyAllWindows()
