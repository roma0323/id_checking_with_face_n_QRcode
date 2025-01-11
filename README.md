# ID Checking with Face Recognition and QR Code

This project uses face recognition and QR code detection to verify identities. It captures video from a webcam, detects faces and QR codes, and checks if the detected face matches the identity encoded in the QR code.

## Requirements

Install the required Python packages using the following command:

```sh
pip install -r requirements.txt
```

## Project Structure

main.py: Main script to run the face recognition and QR code detection.
image_loader.py: Loads target images and encodes faces.
generateQRcode.py: Generates QR codes for images in the face_example directory.
convertHeicToJpg.py: Converts HEIC images to JPG format.
face_example: Directory containing face images.
qr_codes: Directory where generated QR codes are saved.
requirements.txt: List of required Python packages.

## Usage
1. Add Known Faces: Place all known face images in the face_example directory.

2. Generate QR Codes: Generate QR codes for the images in the face_example directory:

```sh
python generateQRcode.py
```

3. Run the Main Script: Start the face recognition and QR code detection:

```sh
python main.py
```
