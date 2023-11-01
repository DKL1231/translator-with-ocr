import easyocr
import os
from PIL import Image
import numpy as np
import imageprocessing

class TextExtractionApp:
    def __init__(self):
        self.language = ['en']
        #self.language = ['ja'] # default : japanese
        self.reader = easyocr.Reader(lang_list=self.language, gpu=True)

    def extract_text_from_image(self):
        path = os.getcwd() + '\\captureimg\\'
        filename = 'window_capture.png'
        
        #path = os.getcwd() + '\\unuploadtogithub\\testimg\\'
        #filename = 'testimg1.png'
        image_path = path+filename
        #img = Image.open(image_path)
        #img = np.array(img)
        
        img = imageprocessing.preprocess(image_path)
        
        text = self.reader.readtext(img, detail=0)
        return text
    
    def setLanguage(self, language):
        self.language = [language]
        self.reader = easyocr.Reader(lang_list=self.language, gpu=True)

if __name__ == '__main__':
    tmp = TextExtractionApp()
    print(tmp.extract_text_from_image())