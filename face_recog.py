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

    face_locations = face_recognition.face_locations(rgb_small_frame) #return coordinates of detected face (1 tuple for one face)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations) #makes a unique 128-D vector for the face
    #o/p is an numpy array.
    """
    Used face_locations:[(top,right,bottom,left)] format to speedup face_encodings.
    """
    for face_encoding in face_encodings:

        for student in students:
            # student.face_encodings is a list ([encoding_photo1, ..photo2])
            matches = face_recognition.compare_faces(student.face_encodings, face_encoding, tolerance=0.6)
            
            if True in matches:
                return student
                
    return None