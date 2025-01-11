import face_recognition
import cv2
from image_loader import load_target_images

# Reduce the resolution of the video feed
video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Load the target image file if it exists
known_face_encodings, known_face_names = load_target_images()
print("Loaded face names:", known_face_names)

while True:
    ret, frame = video_capture.read()
    if not ret:
        break
    camera_face_name = "Unknown"         
    certain_known_face_name = "Unknown"
    qrData ="Unknown"
    try:
        # Detect QR codes in the frame
        qr_code_detector = cv2.QRCodeDetector()
        qrData, bbox, _ = qr_code_detector.detectAndDecode(frame)
        
        if bbox is not None and qrData:
            
            known_face_encodings_index = -1
            if qrData in known_face_names:
                known_face_encodings_index = known_face_names.index(qrData)
                print(f"{qrData} is in position {known_face_encodings_index}")
                certain_known_face_encodings = [known_face_encodings[known_face_encodings_index]] if known_face_encodings_index != -1 else []
                certain_known_face_name = known_face_names[known_face_encodings_index] if known_face_encodings_index != -1 else []
                
            # , draw a circle around the QR code
            color = (0, 255, 0) if qrData in known_face_names else (0, 0, 255)  # Green if match, red otherwise
            pts = bbox.astype(int).reshape(-1, 1, 2)
            cv2.polylines(frame, [pts], isClosed=True, color=color, thickness=3)
            cv2.putText(frame, qrData, (pts[0][0][0], pts[0][0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)    
            
            
            face_locations = face_recognition.face_locations(frame)
            if  face_locations:
                face_encodings = face_recognition.face_encodings(frame)
                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    # Compare the face encoding with known encodings
                    matches = face_recognition.compare_faces(certain_known_face_encodings, face_encoding, 0.45)
                    face_distances = face_recognition.face_distance(certain_known_face_encodings, face_encoding)

                    # Set rectangle color based on whether a match was found
                    color = (0, 255, 0) if any(matches) else (0, 0, 255)  # Green if match, red otherwise

                    # Optionally, annotate the frame with the name of the matched face
                    distance_text = ""
                    if any(matches):
                        camera_face_name = certain_known_face_name
                        distance_text = f" ({face_distances[0]:.2f})"

                    # Draw a rectangle around the face
                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                    # Display the name and distance (optional)
                    cv2.putText(frame, f"{camera_face_name}{distance_text}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    # Display the distance for each known face encoding
                    for i, known_face_encoding in enumerate(certain_known_face_encodings):
                        distance_text = f" {certain_known_face_name} : {face_distances[i]:.2f}"
                        cv2.putText(frame, distance_text, (10, 30 + i * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            else :
                print("No face found")
        else:
            print("No QR code found")        
        # tell qr code whether correct guy
        cv2.putText(frame, "qrData: "+qrData+" name: "+camera_face_name, (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        if qrData == camera_face_name:
            cv2.putText(frame, "pass", (10, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        else:
            cv2.putText(frame, "no pass", (10, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                    
        
    except Exception as e:
        print("Error generating face encodings:", e)

    # Display the video
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()