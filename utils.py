import os
from deepface import DeepFace

def recognize_face_from_frame(frame, students):
    """
    Saves the incoming frame temporarily and verifies it against registered students.
    """
    temp_path = "temp_scan.jpg"
    import cv2
    cv2.imwrite(temp_path, frame)

    matched_student = None
    for student in students:
        if not os.path.exists(student.image_path):
            continue
        try:
            # Compare live frame against the student's reference image
            result = DeepFace.verify(
                img1_path=temp_path, 
                img2_path=student.image_path, 
                enforce_detection=False,
                model_name="VGG-Face"
            )
            if result["verified"]:
                matched_student = student
                break
        except Exception as e:
            print(f"Error checking student {student.name}: {e}")

    # Clean up temp image
    if os.path.exists(temp_path):
        os.remove(temp_path)

    return matched_student