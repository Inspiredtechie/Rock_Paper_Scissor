import cv2
import cvzone
import time
import random
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
score = [0,0]

while True:
    imgBG =cv2.imread("Background3.png")
    success, img = cap.read()
    
    imgScaled = cv2.resize(img, (0,0), None, 0.84, 0.62)
    imgScaled = imgScaled[:, 76:480]
    
    hands, img = detector.findHands(imgScaled)
    
    if startGame:
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (660,391), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (255,234,0), 6)#scale,colour,thickness
            if timer>3:
                stateResult = True
                timer = 0
                
                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [1,1,1,1,1]:
                        playerMove = "Paper"
                    if fingers == [0,0,0,0,0]:
                        playerMove = "Rock"
                    if fingers == [0,1,1,0,0]:
                        playerMove = "Scissor"
                    
                    randomMove = random.choice(["Rock", "Paper", "Scissor"])
                    imgAI = cv2.imread(f"{randomMove}.png", cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, [120,269])
                    
                    #player score count
                    if (playerMove == "Rock" and randomMove == "Scissor") or (playerMove == "Paper" and randomMove == "Rock") or (playerMove == "Scissor" and randomMove == "Paper"):
                        score[1] += 1
                    elif playerMove == randomMove:
                        pass
                    
                    #BOt score count
                    if (playerMove == "Scissor" and randomMove == "Rock") or (playerMove == "Rock" and randomMove == "Paper") or (playerMove == "Paper" and randomMove == "Scissor"):
                        score[0] += 1
                    elif playerMove == randomMove:
                        pass
                    
                    print(playerMove)
    
    imgBG[272:570,858:1262] = imgScaled #adjust or move the frame in the background
    
    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, [120,269])
    
    cv2.putText(imgBG, str(score[0]), (608,680), cv2.FONT_ITALIC, 2, (0,0,0), 4)
    cv2.putText(imgBG, str(score[1]), (719,680), cv2.FONT_ITALIC, 2, (0,0,0), 4)
    
    # cv2.imshow("Image", img)
    # cv2.imshow("Scaled", imgScaled)
    cv2.imshow("Background", imgBG)
    
    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False
    
    if key == ord('q'):
        break