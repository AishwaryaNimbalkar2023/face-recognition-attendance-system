import mysql.connector
import datetime

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="aish1234",
        database="face_recognition"
    )

def get_attendance_records(mode, value):
   
    conn = connect_db()
    cursor = conn.cursor()

    try:
        if mode == 'day':
            datetime.datetime.strptime(value, "%Y-%m-%d")
            query = "SELECT name, student_id, date, time FROM attendance WHERE date = %s"
            params = (value,)

        elif mode == 'month':
            datetime.datetime.strptime(value, "%Y-%m")
         
            query = "SELECT name, student_id, date, time FROM attendance WHERE DATE_FORMAT(date, '%Y-%m') = %s"
            params = (value,)
        else:
            raise ValueError("Invalid mode. Use 'day' or 'month'.")

        cursor.execute(query, params)
        records = cursor.fetchall()
        return records

    except mysql.connector.Error as e:
        raise Exception(f"MySQL Error: {e}")
    finally:
        conn.close()

