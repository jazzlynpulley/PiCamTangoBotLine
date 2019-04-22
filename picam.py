#############################
# Edited by: Jazzlyn Pulley #
#            Josh Cullings  #
# Team Number: 35           #
#############################

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from maestro import Controller
import tkinter as tk
import numpy as np
#from keyboardControl import KeyControl

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
inx = 640
iny = 480
camPos = 4000
MOTORS = 1 # left motor
TURN = 2 # opposite
BODY = 0
HEADTILT = 4
HEADTURN = 3

# allow the camera to warmup
time.sleep(3)
myC = Controller()
#myC.setTarget(1,0)
#myC.setTarget(1, 6000)
#myC.setTarget(2, 6000)

def reset():
    camPos = 4000
    myC.setTarget(BODY,6000)
    myC.setTarget(MOTORS,6000)
    myC.setTarget(TURN,6000)
    myC.setTarget(HEADTURN,6000)
    myC.setTarget(HEADTILT,4000)

def cog():
    # code for center of gravity will go here
    print("Starting cog")

def forward():
    myC.setTarget(MOTORS, 6000)
    myC.setTarget(MOTORS, 7400)

def reverse():
    myC.setTarget(MOTORS, 6000)
    myC.setTarget(MOTORS, 2110)

def stop():
    myC.setTarget(MOTORS, 6000)
    myC.setTarget(TURN, 6000)

def right():
    print("Turning right")
    myC.setTarget(TURN, 6000)
    myC.setTarget(TURN, 7400)
    time.sleep(0.2)
    myC.setTarget(TURN, 6000)

def left():
    print("Turning left")
    myC.setTarget(TURN, 5000)
    time.sleep(0.2)
    myC.setTarget(TURN, 6000)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurImage = cv2.GaussianBlur(grayImage, (5, 5), 0)
    pic = cv2.threshold(blurImage, 200, 255, 0)[1]

    cont, heir = cv2.findContours(pic, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, cont, -1, (0,0,255), 3)

    if cont is not None:
        momentCount = 0
        xCount = 0
        yCount = 0
        avX = 0
        avY = 0
        for c in cont:

     # calculate moments for each contour
            M = cv2.moments(c)

   # calculate x,y coordinate of center
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.circle(image, (cX, cY), 5, (255, 255, 255), -1)
                yCount += cY
                if(cY > 240):
                    xCount += cX
                    momentCount += 1

        if (momentCount > 0):
            avX = xCount / momentCount
            avY = yCount / momentCount

        print ("x: "+str(avX))

        '''if (avX < 325  and avX > 275):
            myC.setTarget(2,6000)
            myC.setTarget(1,6000)
        elif (avX < 275):
            myC.setTarget(1,5000)

        elif (avX > 325):
            myC.setTarget(2,5000)'''
        #if (avX == 0):
            #reset()

        #if (avY>60):
            #myC.setTarget(1,5250)
        if (avX > 240 and avX < 400):
            myC.setTarget(1,5250)
            myC.setTarget(2,6000)
        if (avX < 240 ):
        #turn right
            myC.setTarget(1,5250)
            myC.setTarget(2,6950)

        if (avX > 400 ):
        #turn left
            myC.setTarget(1,5250)
            myC.setTarget(2,5050)
        '''
        if (avX == 0):
            print("No path found")
            myC.setTarget(1,6000)
            myC.setTarget(2,6000)
       '''

    # show the frame
    newFrame = image[240:480, 0:640]
    cv2.imshow("Frame", newFrame)
    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)



    '''  Code for moving the camera
    if key == 82:
        camPos += 100
        myC.setTarget(4, camPos)
        print(str(camPos))

    if key == 84:
        if(camPos>4000):
            camPos -= 100
            myC.setTarget(4, camPos)
            print(str(camPos))
        else:
            print("At lowest orientation")'''

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        myC.setTarget(TURN, 6000)
        myC.setTarget(MOTORS, 6000)
        break
             
