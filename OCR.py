# OCR.py

import numpy as np
from pytesseract import Output
import pytesseract
from PIL import Image
import os

class TextExtractionApp:
    def __init__(self):
        pass

    def extract_text_from_image(self):
        path = os.getcwd() + '\\captureimg\\'
        filename = 'window_capture.png'
        image_path = path+filename
        img = Image.open(image_path)

        text = pytesseract.image_to_string(img, config='-l jpn')
        return text
