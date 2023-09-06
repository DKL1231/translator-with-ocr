# OCR.py

import numpy as np
from pytesseract import Output
import pytesseract
from PIL import Image
import os

tesseract_lang = {'en':'eng', 'jp':'jpn', 'ko':'kor'}

class TextExtractionApp:
    def __init__(self):
        self.language = 'jpn' # default : japanese

    def extract_text_from_image(self):
        path = os.getcwd() + '\\captureimg\\'
        filename = 'window_capture.png'
        image_path = path+filename
        img = Image.open(image_path)

        text = pytesseract.image_to_string(img, config='-l '+self.language)
        return text
    
    def setLanguage(self, language):
        self.language = tesseract_lang[language]
