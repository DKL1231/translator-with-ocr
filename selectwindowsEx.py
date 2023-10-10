import tkinter as tk
from tkinter import Menu, Toplevel, messagebox
from tkinter.colorchooser import askcolor
from PIL import ImageTk
from tkinter import ttk
from pynput import keyboard

class ResizableWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_attributes("-topmost", 1)
        self.root.overrideredirect(True)  # Remove window decorations (top bar)
        self.alpha = 1
        self.root.attributes("-alpha", self.alpha)
        self.prev_x, self.prev_y = None, None
        self.isStopped = False

        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

        # Create a frame to act as the outline
        self.outline_frame = tk.Frame(self.root, bg="black", borderwidth=3, relief="solid", highlightthickness=0)
        self.outline_frame.pack(fill=tk.BOTH, expand=True)
        self.outline_frame.bind("<ButtonPress-1>", self.on_left_click)
        self.outline_frame.bind("<B1-Motion>", self.on_left_drag)
        self.outline_frame.bind("<Button-3>", self.on_right_click)

        # Create a canvas to capture mouse events
        self.canvas = tk.Canvas(self.outline_frame, bg='white')
        self.root.wm_attributes("-transparentcolor", 'white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_left_click)
        self.canvas.bind("<B1-Motion>", self.on_left_drag)
        self.canvas.bind("<Button-3>", self.on_right_click)

        # Create a context menu
        self.context_menu = Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Close", command=self.close_window)
        self.context_menu.add_command(label="Settings", command=self.open_settings_window)

        # Set the window size and position
        window_width, window_height = 900, 200
        screen_width, screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x, y = (screen_width - window_width) // 2, (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.x, self.y, self.width, self.height = x, y, window_width, window_height

        # Allow the window to be resizable
        self.root.resizable(True, True)

    def get_window_position_and_size(self):
        self.root.update_idletasks()  # Ensure that window info is up to date
        try:
            return self.x, self.y, self.width, self.height
        except ValueError:
            return None

    def on_left_click(self, event):
        self.prev_x, self.prev_y = event.x, event.y

    def on_left_drag(self, event):
        x, y = event.x_root - self.prev_x, event.y_root - self.prev_y
        self.root.geometry(f"+{x}+{y}")
        
        self.x = x
        self.y = y

    def on_right_click(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def close_window(self):
        self.root.destroy()
        self.isStopped = True

    def set_alpha(self, alpha):
        self.root.attributes("-alpha", alpha)
        self.alpha = alpha
        self.root.update_idletasks()

    def on_press(self, key):
        try:
            if key.char == 's':
                self.alpha = 1
                self.set_alpha(1)
        except:
            pass

    def open_settings_window(self):
        settings_window = Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("300x150+100+100")
        #icon = ImageTk.PhotoImage(file="icon\\icon1.jpg")
        #settings_window.iconphoto(False, icon)
        padding_y = 5
        '''
        alpha_label = tk.Label(settings_window, text="Alpha Level (0.0 - 1.0):")
        alpha_label.pack()
        alpha_emergency = tk.Label(settings_window, text="When you cannot find window, press s")
        alpha_emergency.pack()
        def apply_alpha(event):
            alpha = alpha_slider.get()
            self.set_alpha(alpha)

        alpha_slider = ttk.Scale(
            settings_window,
            from_ = 0,
            to = 1,
            orient = 'horizontal',
            command=apply_alpha
        )
        alpha_slider.pack(pady=padding_y)
        alpha_slider.set(self.alpha)
        '''
        size_label = tk.Label(settings_window, text="Window Size (WxH):")
        size_label.pack()

        size_entry = tk.Entry(settings_window)
        size_entry.pack()

        def apply_size():
            size_str = size_entry.get()
            try:
                width, height = map(int, size_str.split('x'))
                if width > 0 and height > 0:
                    self.root.geometry(f"{width}x{height}")
                    self.root.update_idletasks()  # Ensure that window info is up to date
                    widhei, x, y = self.root.geometry().split('+')
                    width, height = widhei.split('x')
                    self.x, self.y, self.width, self.height = int(x), int(y), int(width), int(height)
                else:
                    messagebox.showerror("Invalid Value", "Width and height must be greater than 0")
            except ValueError:
                messagebox.showerror("Invalid Value", "Please enter a valid size in WxH format")

        size_apply_button = tk.Button(settings_window, text="Apply Size", command=apply_size)
        size_apply_button.pack()

        # Add border-related settings here if needed
        '''
        borderColor_label = tk.Label(settings_window, text="Change color of border")
        borderColor_label.pack()
        
        def change_color():
            global colors
            colors = askcolor(title="Color Chooser")
        
        borderColor_button = ttk.Button(settings_window, text='Open Color Chooser', command=change_color)
        borderColor_button['padding'] = (5, 5)
        borderColor_button.pack(pady=padding_y)
        '''

    def start(self):
        # Start the Tkinter main loop
        #self.root.update_idletasks()
        #self.root.update()
        self.root.mainloop()
    
    def __del__(self):
        try:
            self.root.destroy()
        except:
            pass

if __name__ == "__main__":
    window = ResizableWindow()
    window.start()
