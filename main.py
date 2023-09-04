import pyautogui
import selectwindows
from OCR import TextExtractionApp
import tkinter as tk
import selectwindowsEx
import time
import threading
global x, y, width, height
x, y, width, height = None, None, None, None

def select_window_thread():
    global x, y, width, height
    while x is None or y is None or width is None or height is None:
        area_selector = selectwindowsEx.ResizableWindow()
        x, y, width, height = area_selector.get_window_position_and_size()
        area_selector.start()
    while True:
        x, y, width, height = area_selector.get_window_position_and_size()
        area_selector.start()
        time.sleep(0.3)

# Start the thread for the window selection
window_selection_thread = threading.Thread(target=select_window_thread)
window_selection_thread.start()

# Wait for the window selection thread to finish
#window_selection_thread.join()
time.sleep(3)

# Create an instance of TextExtractionApp
text_extractor = TextExtractionApp()

# Create a Tkinter window for displaying the text
root = tk.Tk()
root.title("Text Extraction")
root.geometry("600x400+50+50")
result_label = tk.Label(root, text="", wraplength=400)
result_label.pack(padx=10, pady=10)

while True:
    # Capture the window screenshot in memory
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot.save("captureimg/window_capture.png")

    # Call the extract_text_from_image method to extract text from the saved image
    extracted_text = "Original text : " + text_extractor.extract_text_from_image()

    # Display the extracted text in the Tkinter window
    result_label.config(text=extracted_text)

    # Update the Tkinter window
    root.update()
    
    # Adjust the sleep time to control the capture frequency
    time.sleep(0.3)
