import os
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()
face_example_dir = "face_example"

def convert_heic_to_jpg():
    def convert_to_jpg(input_file, output_file):
        try:
            img = Image.open(input_file)
            img = img.convert("RGB")
            img.save(output_file, "JPEG", quality=95)
            print(f"Successfully converted {input_file} to {output_file}")
            os.remove(input_file)  # Delete the original HEIC file
        except Exception as e:
            print(f"Error converting {input_file} to {output_file}: {e}")

    for root, _, files in os.walk(face_example_dir):
        for file in files:
            file_ext = os.path.splitext(file.lower())[1]
            if file_ext == '.heic':
                input_file = os.path.join(root, file)
                output_file = os.path.splitext(input_file)[0] + ".jpg"
                convert_to_jpg(input_file, output_file)