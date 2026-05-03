import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime

# STEP 1: Path of images folder
path = 'images'
images = []
classNames = []

# STEP 2: Read all images
myList = os.listdir(path)
print("Images found:", myList)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    if curImg is not None:
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])

# STEP 3: Encode faces
def findEncodings(images):
    encodeList = []
    for i, img in enumerate(images):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)

        if len(encodes) > 0:
            encodeList.append(encodes[0])
            print(f"✅ Encoding done for image {i+1}")
        else:
            print(f"⚠️ No face found in image {i+1}, skipping...")

    return encodeList

# STEP 4: Mark attendance
def markAttendance(name):
    file_path = 'attendance.csv'

    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write("Name,Date,Time\n")

    with open(file_path, 'r+') as f:
        data = f.readlines()
        nameList = []

        for line in data:
            entry = line.strip().split(',')
            if len(entry) > 1:
                nameList.append((entry[0], entry[1]))

        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        time = now.strftime('%H:%M:%S')

        if (name, date) not in nameList and name != "UNKNOWN":
            f.writelines(f'{name},{date},{time}\n')
            print(f"📌 Attendance marked for {name}")

# STEP 5: Encode known faces
encodeListKnown = findEncodings(images)
print("🎯 Encoding Complete")

# STEP 6: Start webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    # Resize (better accuracy)
    imgSmall = cv2.resize(img, (0, 0), None, 0.5, 0.5)
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

    # Detect faces
    facesCurFrame = face_recognition.face_locations(imgSmall)
    encodesCurFrame = face_recognition.face_encodings(imgSmall, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):

        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        if len(faceDis) == 0:
            continue

        matchIndex = np.argmin(faceDis)

        print(f"Distance: {faceDis[matchIndex]:.2f}")

        # Improved threshold
        if matches[matchIndex] and faceDis[matchIndex] < 0.6:
            name = classNames[matchIndex].upper()
            color = (0, 255, 0)
        else:
            name = "UNKNOWN"
            color = (0, 0, 255)

        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1*2, x2*2, y2*2, x1*2

        # Draw rectangle
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.rectangle(img, (x1, y2-35), (x2, y2), color, cv2.FILLED)

        cv2.putText(img, name, (x1 + 6, y2 - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Mark attendance
        if name != "UNKNOWN":
            markAttendance(name)

    cv2.imshow('Face Recognition Attendance System', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()