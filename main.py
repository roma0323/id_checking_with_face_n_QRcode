import face_recognition
import cv2
import os
import glob

# Reduce the resolution of the video feed
video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


# Directory containing face example images
face_example_dir = "face_example"

# Supported image file extensions
image_extensions = ["*.png", "*.jpg", "*.jpeg", "*.bmp", "*.tiff"]

# List to hold face encodings and names
known_face_encodings = []
known_face_names = []

# Load each image file in the directory
for ext in image_extensions:
    for image_path in glob.glob(os.path.join(face_example_dir, ext)):
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        if face_encodings:
            known_face_encodings.append(face_encodings[0])
            # Extract the name from the file name (optional)
            name = os.path.splitext(os.path.basename(image_path))[0]
            known_face_names.append(name)

# Optional: Print loaded names for verification
print("Loaded face names:", known_face_names)


while True:
    ret, frame = video_capture.read()
    if not ret:
        break


    rgb_frame = frame[:, :, ::-1]
    # face_locations = face_recognition.face_locations(rgb_frame)
    face_locations = face_recognition.face_locations(rgb_frame,model="cnn")

    try:
        if not face_locations:
            print("No faces detected in this frame.")
        else:    
            face_encodings = face_recognition.face_encodings(frame)
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Compare the face encoding with known encodings
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, 0.4)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

                # Set rectangle color based on whether a match was found
                color = (0, 255, 0) if any(matches) else (0, 0, 255)  # Green if match, red otherwise

                # Optionally, annotate the frame with the name of the matched face
                name = "Unknown"
                distance_text = ""
                if any(matches):
                    match_index = matches.index(True)
                    name = known_face_names[match_index]
                    distance_text = f" ({face_distances[match_index]:.2f})"

                # Draw a rectangle around the face
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

                # Display the name and distance (optional)
                cv2.putText(frame, f"{name}{distance_text}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
                # Display the distance for each known face encoding
                for i, known_face_encoding in enumerate(known_face_encodings):
                    distance_text = f" {known_face_names[i]} : {face_distances[i]:.2f}"
                    cv2.putText(frame, distance_text, (10, 30 + i * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    
            print("Face encodings generated successfully.")
        
    except Exception as e:
        print("Error generating face encodings:", e)

    # Display the video
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()