import tkinter as tk
from tkinter import Menu, Toplevel
from tkinter import ttk
from tkinter.colorchooser import askcolor

def get_window_position_and_size():
    root.update_idletasks()  # Ensure that window info is up to date
    geometry_str = root.geometry()
    try:
        widhei, x, y = geometry_str.split('+')
        width, height = widhei.split('x')
        return x, y, width, height
    except ValueError:
        return None

def on_left_click(event):
    global prev_x, prev_y
    prev_x = event.x
    prev_y = event.y

def on_left_drag(event):
    x, y = event.x_root - prev_x, event.y_root - prev_y
    root.geometry(f"+{x}+{y}")

def on_right_click(event):
    context_menu.post(event.x_root, event.y_root)

def close_window():
    root.destroy()

def set_alpha(alpha):
    root.attributes("-alpha", alpha)
'''
def set_borderColor(rgb):
    border_color = rgb
'''
def open_settings_window():
    settings_window = Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("300x150+100+100")
    padding_y = 5
    
    # alpha level set
    alpha_label = tk.Label(settings_window, text="Alpha Level (0.0 - 1.0):")
    alpha_label.pack()
    alpha_entry = tk.Entry(settings_window)
    alpha_entry.pack()
    
    def apply_Alpha():
        try:
            alpha = float(alpha_entry.get())
            if 0 <= alpha <= 1:
                set_alpha(alpha)
            else:
                tk.messagebox.showerror("Invalid Value", "Alpha must be between 0.0 and 1.0")
        except ValueError:
            tk.messagebox.showerror("Invalid Value", "Please enter a valid number for Alpha")

    apply_button = tk.Button(settings_window, text="Apply Alpha", command=apply_Alpha)
    apply_button.pack(pady=padding_y)
    ''' # border의 설정방법을 모르겠음
    # borderColor set
    borderColor_label = tk.Label(settings_window, text="Change color of border")
    borderColor_label.pack()
    
    def change_color():
        global colors
        colors = askcolor(title="Color Chooser")
    
    borderColor_button = ttk.Button(settings_window, text='Open Color Chooser', command=change_color)
    borderColor_button['padding'] = (5, 5)
    borderColor_button.pack(pady=padding_y)
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
                root.geometry(f"{width}x{height}")
            else:
                tk.messagebox.showerror("Invalid Value", "Width and height must be greater than 0")
        except ValueError:
            tk.messagebox.showerror("Invalid Value", "Please enter a valid size in WxH format")

    size_apply_button = tk.Button(settings_window, text="Apply Size", command=apply_size)
    size_apply_button.pack()

    
root = tk.Tk()
root.wm_attributes("-topmost", 1)
root.overrideredirect(True)  # Remove window decorations (top bar)

# Set the initial alpha level
alpha = 0.4
root.attributes("-alpha", alpha)

# Create a canvas to capture mouse events
canvas = tk.Canvas(root, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)
canvas.bind("<ButtonPress-1>", on_left_click)
canvas.bind("<B1-Motion>", on_left_drag)
canvas.bind("<Button-3>", on_right_click)

# Create a context menu
context_menu = Menu(root, tearoff=0)
context_menu.add_command(label="Close", command=close_window)
context_menu.add_command(label="Settings", command=open_settings_window)

# Set the window size and position
window_width = 400
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Allow the window to be resizable
root.resizable(True, True)

# Start the Tkinter main loop
root.mainloop()

