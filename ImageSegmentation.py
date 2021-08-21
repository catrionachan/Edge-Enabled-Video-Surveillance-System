#Note: the trained model was obtained from OpenCV repository

#Import libraries
import cv2
import imutils
import numpy as np
from datetime import datetime

#Set variables for inital boolean and integer values
#Person present in frame
present = False
#A file is open for recording 
recording = True
#Count of video files recorded 
counter =0
#Count of frames since inital video recording
counter2 =0


#Restart count of frames recorded
def restartCount():
    global counter2
    counter2 =0

#get count of videos recorded
def getCount1():
    global counter
    return counter
#get count of frames recorded
def getCount2():
    global counter2
    return counter2

# increment count of videos recorded
def addCount1():
    global counter
    counter +=1
    print(counter)
#Increment for count of frames recorded
def addCount():
    global counter2
    counter2 +=1
    #print(counter2)

#set camera resolution to 720p
def make_720p():
    cap.set(3, 1280)
    cap.set(4, 720)
    
#set camera resolution to 480p
def make_480p():
    cap.set(3, 640)
    cap.set(4, 480)

# Determine if face is detected in video frame    
def detectFace(frame):
    global present
    #obtain frame w/ uppper and lower bounds
    img = frame[84:225, 1:1280]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    #sets boolean variable Present if person in video frame
    if len(faces)>0:
        present = True
    else:
        present = False
    # Draw rectangle around the faces
    for (x, y, w, h) in faces:
       cv2.rectangle(frame, (x, y+84), (x+w, y+h+84), (255, 0, 0), 2)
       # adds cordinate of all the faces in the frame
       coordinateFile = open("coordinateTest.txt", "a")
       coordinateFile.write("\n"+str(x)+","+str(y)+","+str(x+w)+","+str(h+y))
       coordinateFile.close()


#load Haar Cascade classifier trained file  
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
fourcc = cv2.VideoWriter_fourcc(*'XVID')

#Create Video Writer to record frames
out= cv2.VideoWriter("t25v0.avi", cv2.VideoWriter_fourcc('M','J','P','G'), 15.0, (1280, 720))

#obtain video from IP camera address
#cap=cv2.VideoCapture("rtsp://10.0.0.125")
#obtain video from specified source

cap=cv2.VideoCapture(0)

#Main code loop which repeats while program is running 
while(True):
        #reads video frame
        ret, frame = cap.read()
        #if no frame can be identified, restarts connection
        if not ret:
            print ("No Frame")
            cap.release()
            cap = cv2.VideoCapture(0)
        #Resize camera to appropriate size
        else:
            if present:
                frame = imutils.resize(frame, width = 1280, height = 720)
            else:
                frame = imutils.resize(frame, width = 640, height = 480)
            #gets current time and add to video frame
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            cv2.putText(frame, current_time, (10, 450),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), thickness=2)
            #checks for person in frame
            detectFace(frame)
            #if new video file not ready, creates the video file
            if present and not recording:
                name = "t25v"+str(getCount1()) + ".avi"
                out= cv2.VideoWriter(name, cv2.VideoWriter_fourcc('M','J','P','G'), 15.0, (1280, 720))
                make_720p()
                addCount1()
                recording = True
                #print(current_time)
            #if person in frame, adds video frame into the video    
            if present:
                out.write(frame)
                key=cv2.waitKey(1)
                addCount()
            #if no person is present but count of frames recorded is less than 30 than continue to record
            elif getCount2()<=30:
                addCount()
                out.write(frame)
                key=cv2.waitKey(1)
            #if person is not present, video not recording and frames recorded is restarted
            else:
                recording = False
                make_480p()
                key=cv2.waitKey(1)
                restartCount()
                
            #stops code if q key is pressed
            if key == ord('q'):
                break
            # Display the output 
            #cv2.imshow('img', frame)
#once out of while loop the camera and video writer is released and the windows are destroyed
cap.release()
out.release()
cv2.destroyAllWindows()
