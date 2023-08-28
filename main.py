import pyautogui
import selectwindows
from OCR import TextExtractionApp  # Import the TextExtractionApp class from OCR.py
import tkinter as tk
import time

x, y, width, height = None, None, None, None

while x is None or y is None or width is None or height is None:
    area_selector = selectwindows.AreaSelector()
    area_selector.start()
    x, y, width, height = area_selector.return_point()  # Adjust these values to match your target window
selecting_area = False
print(x, y, width, height)

# Create an instance of TextExtractionApp
text_extractor = TextExtractionApp()

# Create a Tkinter window for displaying the text
root = tk.Tk()
root.title("Text Extraction")
root.geometry("600x400+50+50")
result_label = tk.Label(root, text="", wraplength=400)
result_label.pack(padx=10, pady=10)


while True:
    if not selecting_area:
        # Capture the window screenshot in memory
        screenshot = pyautogui.screenshot(region=(x, y, width-x, height-y))

        screenshot.save("captureimg/window_capture.png")

        # Call the extract_text_from_image method to extract text from the saved image
        extracted_text = "Original text : " + text_extractor.extract_text_from_image()

        # Display the extracted text in the Tkinter window
        result_label.config(text=extracted_text)

    # Update the Tkinter window
    root.update()
    
    # Adjust the sleep time to control the capture frequency
    time.sleep(0.3)
