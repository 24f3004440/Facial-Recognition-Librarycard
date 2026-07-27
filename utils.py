import cv2
import face_recognition
import numpy as np

def recognize_face_from_frame(frame, students):
    """
    Takes an OpenCV frame and a list of Student objects from SQLAlchemy,
    returns the matched Student object or None.
    """
    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    if not face_encodings:
        return None

    for face_encoding in face_encodings:
        for student in students:
            # Compare database encoding with current face encoding
            match = face_recognition.compare_faces([student.face_encoding], face_encoding, tolerance=0.6)
            if match[0]:
                return student
                
    return None