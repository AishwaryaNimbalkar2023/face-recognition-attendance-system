formateed import cv2
import os
import mysql.connector
from tkinter import messagebox

def capture_faces(name, roll_no):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="aish1234",
        database="face_recognition"
    )
    cursor = db.cursor()

    try:
        cursor.execute("INSERT INTO students (name, roll_no) VALUES (%s, %s)", (name, roll_no))
        db.commit()
    except mysql.connector.errors.IntegrityError:
        messagebox.showerror("Error", "Roll number already exists!")
        db.close()
        return

    db.close()

    folder = f'dataset/{roll_no}_{name}'
    os.makedirs(folder, exist_ok=True)

    cap = cv2.VideoCapture(0)
    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if count < 15:
            img_name = f"{folder}/{count}.jpg"
            cv2.imwrite(img_name, frame)
            count += 1

        cv2.imshow("Capturing Face - Press 'q' to quit", frame)

        if count >= 15 or cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("Success", f"Captured 15 photos for {name} ({roll_no})")

