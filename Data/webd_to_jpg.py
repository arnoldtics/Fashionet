import os
from PIL import Image

def convert_webp_to_jpg(directory):
    if not os.path.isdir(directory):
        print(f"The directory {directory} don't exist")
        return

    files = os.listdir(directory)
    
    for file in files:
        if file.lower().endswith('.webp'):
            file_path = os.path.join(directory, file)
            try:
                with Image.open(file_path) as img:
                    base_name = os.path.splitext(file)[0]
                    new_name = os.path.join(directory, f"{base_name}.jpg")
                    
                    if img.mode in ("RGBA", "P"): img = img.convert("RGB")
                    
                    img.save(new_name, "JPEG")
            except Exception as e:
                print(f"Error in {file}: {e}")

# Directorio de entrada
directory = input("Directory: ").strip()
convert_webp_to_jpg(directory)
