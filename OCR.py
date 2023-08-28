import numpy as np
from pytesseract import Output
import pytesseract
import cv2
from PIL import Image
import os

path = os.getcwd()+'\\unuploadtogithub\\testimg\\'
filename = 'testimg2.png'

print(path+filename)
img = Image.open(path+filename)
img.show()

img1 = np.array(Image.open(path+filename))

text = pytesseract.image_to_string(img, config='-l jpn')
print(text)