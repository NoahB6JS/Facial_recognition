
import cv2
import sqlite3
import face_recognition
import pickle
import os

# ---create the database ---
def sql_creation():
    # check if db exists or not
    if os.path.exists("faces.db"):
        print("DB already exists, using it")
    else:
        database = sqlite3.connect("faces.db")
        cursor = database.cursor()

        # create table for users, includes encoding for faces
        cursor.execute("""
            CREATE TABLE users (
                name TEXT,
                face_id INTEGER,
                encoding BLOB
            )
        """)

        # load a face from a file
        image = face_recognition.load_image_file("Noah.jpg")  # make sure this pic is here
        encoding = face_recognition.face_encodings(image)  # returns list of face encodings
        if len(encoding) > 0:
            cursor.execute(
                "INSERT INTO users (name, face_id, encoding) VALUES (?, ?, ?)",
                ("Noah", 1, pickle.dumps(encoding[0]))
            )

        database.commit()
        database.close()
        print("Database created and Noah added (if pic exists)")

#--- get all faces from db -------
def get_db_faces():
    database = sqlite3.connect("faces.db")
    cursor = database.cursor()

    cursor.execute("SELECT name, encoding FROM users")
    db_faces = cursor.fetchall()
    database.close()
    return db_faces

#-----  match live face to db ----
def match_faces(live_face):
    db_faces = get_db_faces()
    for name, encoding_blob in db_faces:
        db_encoding = pickle.loads(encoding_blob)
        distance = face_recognition.face_distance([db_encoding], live_face)[0]
        if distance < 0.6:
            return name
    return "Unknown"

# - capture from webcam and detect faces ---
def read_screen_for_faces():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("uh oh couldnt read frame")
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        live_faces = face_recognition.face_encodings(rgb_frame)

        # draw rectangles on the faces we detect (not perfect sometimes)
        face_locations = face_recognition.face_locations(rgb_frame)
        for (top, right, bottom, left), live_face in zip(face_locations, live_faces):
            name = match_faces(live_face)
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)

        cv2.imshow("Face Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('p'):
            break

    cap.release()
    cv2.destroyAllWindows()


sql_creation()
read_screen_for_faces()