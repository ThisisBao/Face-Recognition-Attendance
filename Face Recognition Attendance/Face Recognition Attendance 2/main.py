import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pyodbc


path = 'Face Recognition Attendance 2/images'
images = []
classNames = []
myList = os.listdir(path)

for name in myList:
    img = cv2.imread(f'{path}/{name}')
    images.append(img)
    classNames.append(os.path.splitext(name)[0])

def findEncodings(images):
    encodeList = []
    for image in images:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(image)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name, inTime, InDate):
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-1F0T08U;'
                          'Database=attendancedb;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()
    sql = '''insert into attendancedb.dbo.tbl_attendance (Name,InDate,InTime) values(?,?,?)'''
    val=(name,InDate,inTime)
    cursor.execute(sql,val)
    conn.commit()


KnownEncodeList = findEncodings(images)
print('Encoding Completed')

cap = cv2.VideoCapture(0)
nm = 'a'

while True:
    ret, img = cap.read()
    imgS = cv2.resize(img, (0,0), None, 0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
    # print(encodesCurFrame)


    for encodeFace,faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(KnownEncodeList, encodeFace)
        faceDis = face_recognition.face_distance(KnownEncodeList, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            # print(name)
            y1, x2 , y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img, (x1, y2-35),(x2,y2), (0,255,0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

            currentTime = datetime.now().time()
            currentDate = datetime.now().date()
            if name != nm:
                markAttendance(name,str(currentTime),str(currentDate))
                nm=name


    cv2.imshow("frame", img)
    if cv2.waitKey(1) == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()







