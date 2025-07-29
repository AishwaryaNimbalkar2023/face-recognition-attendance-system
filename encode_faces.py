# encode_faces.py
import face_recognition
import os
import pickle
import cv2

def train_and_save_encodings():
    dataset_dir = "dataset"
    known_encodings = []
    known_names = []

    for person_name in os.listdir(dataset_dir):
        person_path = os.path.join(dataset_dir, person_name)
        if not os.path.isdir(person_path):
            continue

        for filename in os.listdir(person_path):
            image_path = os.path.join(person_path, filename)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(person_name)

    # Save to pkl
    with open("encodings.pkl", "wb") as f:
        pickle.dump({"encodings": known_encodings, "names": known_names}, f)

    print("Training complete and encodings saved.")

