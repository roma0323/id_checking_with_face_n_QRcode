import face_recognition
import cv2
import os
import glob

image_extensions = ["*.png", "*.jpg", "*.jpeg", "*.bmp", "*.tiff"]
face_example_dir = "face_example"
target_width = 640
target_height = 480

def load_target_images():
    known_face_encodings = []
    known_face_names = []

    for ext in image_extensions:
        for image_path in glob.glob(os.path.join(face_example_dir, ext)):
            image = face_recognition.load_image_file(image_path)
            
            image = cv2.resize(image, (target_width, target_height))
            
            face_encodings = face_recognition.face_encodings(image)
            if face_encodings:
                known_face_encodings.append(face_encodings[0])
                known_face_names.append(os.path.splitext(os.path.basename(image_path))[0])

    if not known_face_encodings:
        print("No faces found in the directory")

    return known_face_encodings, known_face_names