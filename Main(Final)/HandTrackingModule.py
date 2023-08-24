import cv2 as cv
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # Initialize the MediaPipe Hands module
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        # Convert image to RGB format (required by MediaPipe)
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        # Process hand detection on the image
        self.results = self.hands.process(imgRGB)
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    # Draw landmarks and connections on the image
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        
        return img
    
    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                # Calculate the pixel coordinates of the landmark
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                
                if draw:
                    # Draw circles at landmark positions
                    cv.circle(img, (cx, cy), 15, (255, 0, 255), cv.FILLED)
        
        return lmList

def main():
    pTime = 0  # previous time
    cTime = 0  # current time
    cap = cv.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()
        # Flip the image horizontally for a more intuitive user experience
        img = cv.flip(img, 1)
        # Perform hand detection on the image
        img = detector.findHands(img)
        # Find the positions of landmarks on the detected hand
        lmList = detector.findPosition(img)
        
        if len(lmList) != 0:
            # Print the position of a specific landmark (e.g., the tip of the index finger)
            print(lmList[4])
        
        # Calculate and display frames per second (FPS) on the image
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        # Display the image with landmarks and FPS information
        cv.imshow("Image", img)
        
        # Exit the loop if the 'q' key is pressed
        if cv.waitKey(1) == ord('q'):
            break

if __name__ == "__main__":
    main()
