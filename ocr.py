import easyocr
import numpy as np
from PIL import Image


def create_reader():
    reader = easyocr.Reader(["en"])
    return reader


def read_text(uploaded_file):
    reader = create_reader()

    # Open the uploaded image using Pillow
    image = Image.open(uploaded_file)

    # Convert the image into a NumPy array
    image_array = np.array(image)

    # Perform OCR on the image
    results = reader.readtext(image_array)

    detected_text = []

    for result in results:
        text = result[1]
        confidence = result[2]

        detected_text.append({
            "text": text,
            "confidence": confidence
        })

    return detected_text