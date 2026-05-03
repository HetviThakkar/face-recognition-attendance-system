# face-recognition-attendance-system
Face recognition attendance system using OpenCV and Python
# Face Recognition Attendance System

This project is a real-time face recognition based attendance system built using Python, OpenCV, and the face_recognition library. It detects faces using a webcam and automatically marks attendance with date and time.

---

## Features

* Detects and recognizes faces in real-time
* Automatically marks attendance
* Stores name, date, and time in a CSV file
* Prevents duplicate entries for the same day

---

## Tech Stack

* Python
* OpenCV
* face_recognition
* NumPy

---

## Project Structure

face-recognition-attendance-system/
│
├── images/               # Known faces
├── main.py               # Main program
├── attendance.csv        # Attendance records
├── requirements.txt      # Dependencies
└── README.md             # Project documentation

---

## How to Run

1. Install dependencies:
   pip install -r requirements.txt

2. Run the program:
   python main.py

---

## Output

* Webcam opens and detects face
* Name is displayed on screen
* Attendance is stored in `attendance.csv`

---

## Future Improvements

* Add database (MySQL / MongoDB)
* Add GUI dashboard
* Deploy as a web application

---

## Author

Hetvi Thakkar
