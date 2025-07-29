def recognize_and_mark_attendance():
    import cv2, face_recognition, pickle, mysql.connector, numpy as np, datetime

    with open("encodings.pkl", "rb") as f:
        data = pickle.load(f)

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="aish1234",
        database="face_recognition"
    )
    cursor = conn.cursor()

    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        return None, "Webcam error"

    attendance_status = None
    recognized_name = None

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if face_encodings:
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(data["encodings"], face_encoding)
                face_distances = face_recognition.face_distance(data["encodings"], face_encoding)

                if len(face_distances) == 0:
                    continue

                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    full_name = data["names"][best_match_index]
                    roll_no, name = full_name.split("_", 1)

                    cursor.execute("SELECT id FROM students WHERE roll_no=%s AND name=%s", (roll_no, name))
                    result = cursor.fetchone()

                    if result:
                        student_id = result[0]
                        now = datetime.datetime.now()
                        today = now.date()
                        time = now.time()

                        cursor.execute("SELECT * FROM attendance WHERE student_id = %s AND date = %s", (student_id, today))
                        already_marked = cursor.fetchone()

                        if already_marked:
                            attendance_status = "already"
                            recognized_name = name
                        else:
                            cursor.execute(
                                "INSERT INTO attendance (student_id, name, date, time) VALUES (%s, %s, %s, %s)",
                                (student_id, name, today, time)
                            )
                            conn.commit()
                            attendance_status = "marked"
                            recognized_name = name
                    break

        cv2.imshow("Face Recognition Attendance", frame)
        if attendance_status:
            cv2.waitKey(3000)
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    conn.close()

    return recognized_name, attendance_status

