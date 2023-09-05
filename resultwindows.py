import tkinter as tk
from tkinter import ttk
from PIL import ImageTk

class resultwindows:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Translated text")
        self.root.geometry("600x400+50+50")
        # 여기서 실행할땐 잘 되는데 main에서 하면 런타임에러남;
        #icon = ImageTk.PhotoImage(file="icon\\icon1.jpg")
        #self.root.iconphoto(False, icon)
        pad_x = 15
        pad_y = 30
        
        self.origin_info = tk.Label(self.root, text="Original Text")
        self.origin_info.grid(row=0, padx=(pad_x, pad_x))
        
        self.origintext = tk.Text(self.root, width=80, height=8)
        self.origintext.config(state="disabled")
        self.origintext.grid(row=1, padx=(pad_x, pad_x), pady=(0, pad_y))
        
        self.trans_info = tk.Label(self.root, text="Translated Text")
        self.trans_info.grid(row=2, padx=(pad_x, pad_x))
        
        self.transtext = tk.Text(self.root, width=80, height=8)
        self.transtext.config(state="disabled")
        self.transtext.grid(row=3, padx=(pad_x, pad_x), pady=(0, pad_y))
        
        self.disableValue = True
        self.disablebutton = tk.Checkbutton(self.root, text="Disable Original Text", variable=self.disableValue,command=self.disable_origin)
        self.disablebutton.grid(row=4, padx=(pad_x, pad_x), pady=(pad_y, pad_y))
        
    
    def input_trans(self, text):
        self.transtext.config(state="normal")
        self.transtext.delete("1.0", tk.END)
        self.transtext.insert(tk.END, text)
        self.transtext.config(state="disabled")
    
    def input_origin(self, text):
        self.origintext.config(state="normal")
        self.origintext.delete("1.0", tk.END)
        self.origintext.insert(tk.END, text)
        self.origintext.config(state="disabled")
    
    def disable_origin(self):
        if self.disableValue:
            self.origin_info.grid_forget()
            self.origintext.grid_forget()
            self.disableValue = False
            self.root.geometry("600x250")
        else:
            self.origin_info.grid(row=0)
            self.origintext.grid(row=1)
            self.disableValue = True
            self.root.geometry("600x400")
    
    def start(self):
        self.root.mainloop()

if __name__ == "__main__":
    window = resultwindows()
    
    window.start()