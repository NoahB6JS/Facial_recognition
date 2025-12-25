import cv2
import sqlite3

def sql_creation():

        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE users (name TEXT, face_id INTEGER)')
        cursor.execute("INSERT INTO users VALUES ('Noah', 465 277 295 295")
        conn.commit()

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0) #Opens the built in Mac camera

while True: #loop for frame
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #converts frames into gray scale for easier recognition

    faces = face_cascade.detectMultiScale( #detection object
        gray, scaleFactor=1.1, minNeighbors=6
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2) #building rectangle on detected face

    cv2.imshow("Face Detection", frame) #blitting frame to screen

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cap.release()

cv2.destroyAllWindows()

