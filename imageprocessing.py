import cv2
import easyocr
import numpy as np


def preprocess(imgpath):
    # Read the input image
    if __name__ == "__main__":
        input_image_path = './unuploadtogithub/testimg/testimg2.png'
    else:
        input_image_path = imgpath
    input_image_path = imgpath
    image = cv2.imread(input_image_path)
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Sharpen the image (optional)
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(gray, -1, kernel)
    
    if __name__ != "__main__":
        return sharpened
    
    # Perform OCR on the preprocessed image using Tesseract
    reader = easyocr.Reader(lang_list=['ja'], gpu=True)
    extracted_text = reader.readtext(sharpened, detail=0)

    # Print the extracted text
    print("Extracted Text:")
    print(extracted_text)

    # Save the preprocessed image (optional)
    cv2.imwrite('./unuploadtogithub/testimg/gray.png', gray)
    cv2.imwrite('./unuploadtogithub/testimg/sharpened.png', sharpened)

if __name__ == "__main__":
    input_image_path = './captureimg/window_capture.png'
    preprocess(input_image_path)