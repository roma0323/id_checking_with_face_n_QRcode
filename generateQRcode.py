import os
import qrcode

# Specify the directory containing your images
image_directory = "face_example"
output_directory = "qr_codes"

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Loop through each file in the image directory
for file_name in os.listdir(image_directory):
    if file_name.endswith((".jpg", ".png", ".jpeg")):  # Only process image files
        # QR Code data is the file name
        data = file_name
        
        # Create a QR Code object
        qr = qrcode.QRCode(
            version=1,  # Adjust version for different QR Code sizes
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Generate the QR Code image
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the QR Code with a new name
        qr_code_file_name = f"qr_code_{file_name.split('.')[0]}.png"
        img.save(os.path.join(output_directory, qr_code_file_name))

print("QR Codes have been generated and saved!")
