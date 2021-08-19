import cv2
import imutils
import numpy as np
present = False
videoCounter =1
recording = True
counter =0
counter2 =0

def getCount():
    global counter2
    return counter2

def addCount():
    global counter2
    counter2 +=1
    #print(counter2)

def restartCount():
    global counter2
    counter2 =0

from datetime import datetime

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out= cv2.VideoWriter("t25v0.avi", cv2.VideoWriter_fourcc('M','J','P','G'), 15.0, (640, 480))

#cap=cv2.VideoCapture("rtsp://10.0.0.125")

cap=cv2.VideoCapture(0)
def getCount1():
    global counter
    return counter

def getCount2():
    global counter2
    return counter2

def addCount1():
    global counter
    counter +=1
    print(counter)

def addCount():
    global counter2
    counter2 +=1
    #print(counter2)

def make_720p():
    cap.set(3, 1280)
    cap.set(4, 720)
    
def make_480p():
    cap.set(3, 640)
    cap.set(4, 480)

    
def detectFace(frame):
#    global videoRecording
    global present
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if len(faces)>0:
        present = True
    else:
        present = False
    # Draw rectangle around the faces
    for (x, y, w, h) in faces:
       cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
       coordinateFile = open("coordinateTest.txt", "a")
       coordinateFile.write("\n"+str(x)+","+str(y)+","+str(x+w)+","+str(h+y))
       coordinateFile.close()

while(True):
        ret, frame = cap.read()
        if not ret:
            print ("Nothing in Frame")
            cap.release()
            cap = cv2.VideoCapture(0)
            break
        else:
            frame = imutils.resize(frame, width = 640, height = 480)
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            cv2.putText(frame, current_time, (10, 450),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), thickness=2)
            detectFace(frame)
            if present and not recording:
                name = "t25v"+str(getCount1()) + ".avi"
                out= cv2.VideoWriter(name, cv2.VideoWriter_fourcc('M','J','P','G'), 15.0, (640, 480))
                addCount1()
                recording = True
                print(current_time)
            if present:
                out.write(frame)
                key=cv2.waitKey(1)
                addCount()
            elif getCount2()<=30:
                addCount()
                out.write(frame)
                key=cv2.waitKey(1)
            else:
                recording = False
                key=cv2.waitKey(1)
                restartCount()
            if key == ord('q'):
                break
            # Display the output 
            #cv2.imshow('img', frame)
cap.release()
out.release()
cv2.destroyAllWindows()
    
