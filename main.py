import pyautogui
import ezOCR
import tkinter as tk
import selectwindowsEx
import resultwindows
import googletranslator
import time
import threading

global x, y, width, height, root
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

def main_window_thread():
    global root
    root = resultwindows.resultwindows()
    root.start()

# Start the thread for the window selection
window_selection_thread = threading.Thread(target=select_window_thread)
window_selection_thread.start()

# Wait for the window selection thread to finish
#window_selection_thread.join()
time.sleep(3)

window_trans_thread = threading.Thread(target=main_window_thread)
window_trans_thread.start()

# Create an instance of TextExtractionApp
text_extractor = ezOCR.TextExtractionApp()
translator = googletranslator.googletranslator()

before_text = ""
trans_from, trans_to = translator.src, translator.dest
while True:
    # Capture the window screenshot in memory
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot.save("captureimg/window_capture.png")

    if (trans_from, trans_to) != root.return_combobox():
        trans_from, trans_to = root.return_combobox()
        translator.setLanguage(trans_from, trans_to)
        text_extractor.setLanguage(trans_from)
        before_text = ""
        print(trans_from, trans_to)
    
    
    
    # Call the extract_text_from_image method to extract text from the saved image
    origin_text = text_extractor.extract_text_from_image()
    if origin_text == []:
        origin_text = [""]
    if len(origin_text[0])<10:
        if len(origin_text) > 1:
            origin_text = origin_text[0]+"\n"+" ".join(origin_text[1:])
        else:
            origin_text = origin_text[0]
    else:
        origin_text = " ".join(origin_text)
    
    # Display the extracted text in the Tkinter window
    if before_text != origin_text:
        before_text = origin_text
        root.input_origin(origin_text)

        trans_text = translator.translate(origin_text)
        root.input_trans(trans_text)
    
    # Adjust the sleep time to control the capture frequency
    time.sleep(0.3)
