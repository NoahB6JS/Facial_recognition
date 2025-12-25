import cv2
import sqlite3

def sql_creation():
    conn = sqlite3.connect("faces.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            name TEXT,
            face_id INTEGER
        )
    """)

    cursor.execute(
        "INSERT INTO users VALUES (?, ?)",
        ("Noah", 465)
    )

    conn.commit()
    conn.close()
        
def get_db_faces():
    conn = sqlite3.connect("faces.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, face_id FROM users")

    for name, face_id in cursor:
        print(name, face_id)

    conn.close()

        
def read_screen_for_faces():

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
        
sql_creation()  
get_db_faces()
read_screen_for_faces()




