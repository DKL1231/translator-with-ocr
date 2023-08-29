import tkinter as tk
from PIL import ImageGrab

class AreaSelector:
    def __init__(self):
        self.start_x, self.start_y = None, None
        self.end_x, self.end_y = None, None
        self.selected_area_rectangle = None

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Select Area to Capture")

        # Get the screen width and height
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Set the root window to be always on top
        self.root.wm_attributes("-topmost", 1)

        # Create a transparent top-level window for area selection
        self.selection_window = tk.Toplevel(self.root)
        self.selection_window.overrideredirect(1)  # Remove window decorations
        self.selection_window.attributes("-alpha", 0.8)  # Set transparency level (0.0 to 1.0)
        self.selection_window.geometry(f"{self.screen_width}x{self.screen_height}")  # Set window size to full screen

        # Create a canvas for mouse interaction on the selection window
        self.canvas = tk.Canvas(self.selection_window, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        # Create a label to display information on the main window
        self.info_label = tk.Label(self.root, text="Click to select a start point of rectangular area.")
        self.info_label.pack()

        # Create the capture button on the main window
        #self.capture_button = tk.Button(self.root, text="Capture", command=self.capture_area)
        #self.capture_button.pack()

        # Create the reselect button on the main window
        self.reselect_button = tk.Button(self.root, text="Reselect", command=self.reselect_area)
        self.reselect_button.pack()

        ''' # 왠지 모르겠는데 무한로딩 떠서 삭제
        # Create the OK button on the main window
        self.ok_button = tk.Button(self.root, text="OK", command=self.confirm_selection)
        self.ok_button.pack()
        '''
        # Bind mouse click events to the canvas
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_click)

    def capture_area(self):
        if self.start_x is not None and self.start_y is not None and self.end_x is not None and self.end_y is not None:
            x1, y1 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
            x2, y2 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)

            if x1 < x2 and y1 < y2:
                screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
                screenshot.save("captured_area.png")  # Save the screenshot to a file
                self.info_label.config(text="The selected area has been captured.")
            else:
                self.info_label.config(text="Invalid coordinates. Please make sure x1 < x2 and y1 < y2.")
        else:
            self.info_label.config(text="Please select an area first.")

    def on_mouse_click(self, event):
        if self.start_x is None or self.start_y is None:
            self.start_x, self.start_y = event.x, event.y
            self.info_label.config(text="Click to select a end point of rectangular area.")
        elif self.end_x is None or self.end_y is None:
            self.end_x, self.end_y = event.x, event.y
            #self.capture_area()
            self.info_label.config(text="If you selected area, close this window.")

        # Draw a rectangle on the canvas
        if self.selected_area_rectangle:
            self.canvas.delete(self.selected_area_rectangle)
        if not (self.start_x is None or self.start_y is None or self.end_x is None or self.end_y is None):
            self.selected_area_rectangle = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.end_x, self.end_y, outline="red")

    def reselect_area(self):
        self.start_x, self.start_y, self.end_x, self.end_y = None, None, None, None
        self.info_label.config(text="Click to select a start point of rectangular area.")
        if self.selected_area_rectangle:
            self.canvas.delete(self.selected_area_rectangle)

    def start(self):
        # Start the GUI main loop
        self.root.mainloop()
    
    def confirm_selection(self):
        self.root.quit()  # Close the main window and end the selection process
    
    def return_point(self):
        return self.start_x, self.start_y, self.end_x, self.end_y

# Usage
if __name__ == "__main__":
    area_selector = AreaSelector()
    area_selector.start()