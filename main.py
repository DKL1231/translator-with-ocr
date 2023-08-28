import pyautogui
import selectwindows
from PIL import Image

x, y, width, height = None, None, None, None

while x is None or y is None or width is None or height is None:
    area_selector = selectwindows.AreaSelector()
    area_selector.start()
    x, y, width, height = area_selector.return_point()  # Adjust these values to match your target window

print(x, y, width, height)
while True:
    # Capture the window screenshot in memory
    screenshot = pyautogui.screenshot(region=(x, y, width, height))

    screenshot.save("captureimg/window_capture.png")
    '''
    # Perform OCR on the in-memory image
    import pytesseract
    captured_text = pytesseract.image_to_string(screenshot)

    # Translate the text (use your preferred translation method)
    from translate import Translator
    translator = Translator(to_lang="your_target_language")
    translated_text = translator.translate(captured_text)

    # Output or use the translated text as needed
    print(translated_text)
    '''
    # Adjust the sleep time to control the capture frequency
    import time
    time.sleep(1)
