import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
import googletrans

class resultwindows:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Translated text")
        self.root.geometry("600x700")
        # 여기서 실행할땐 잘 되는데 main에서 하면 런타임에러남;
        #icon = ImageTk.PhotoImage(file="icon\\icon1.jpg")
        #self.root.iconphoto(False, icon)
        self.pad_x = 15
        self.pad_y = 30
        self.isStopped = False
        
        # OriginText Output
        self.origin_info = tk.Label(self.root, text="Original Text")
        self.origin_info.grid(row=0, padx=(self.pad_x, self.pad_x), pady=(self.pad_y, 0))
        
        self.origintext = tk.Text(self.root, width=80, height=8)
        self.origintext.config(state="disabled")
        self.origintext.grid(row=1, padx=(self.pad_x, self.pad_x))
        
        # TransText Output
        self.trans_info = tk.Label(self.root, text="Translated Text")
        self.trans_info.grid(row=2, padx=(self.pad_x, self.pad_x), pady=(self.pad_y, 0))
        
        self.transtext = tk.Text(self.root, width=80, height=8)
        self.transtext.config(state="disabled")
        self.transtext.grid(row=3, padx=(self.pad_x, self.pad_x), pady=(0, self.pad_y))
        
        # OriginText Disable Checkbutton
        self.disableValue = True
        self.disablebutton = tk.Checkbutton(self.root, text="Disable Original Text", variable=self.disableValue,command=self.disable_origin)
        self.disablebutton.grid(row=4, padx=(self.pad_x, self.pad_x), pady=(0, self.pad_y))
        
        # LanguageSelect Combobox
        self.combobox_frame = tk.LabelFrame(self.root, text="select language")
        self.combobox_frame.grid(row=5, pady=(0, self.pad_y))
             
        self.from_lang_list = ['korean', 'japanese', 'english']
        to_lang_list = list(googletrans.LANGUAGES.values())
        self.combobox_from = ttk.Combobox(self.combobox_frame, height=5, values=self.from_lang_list, state="readonly")
        self.combobox_from.current(self.from_lang_list.index('japanese'))
        self.combobox_from.grid(row=1, column=1, padx=(self.pad_x, self.pad_x), pady=(self.pad_y, self.pad_y))
        
        comboboxtext = tk.Label(self.combobox_frame, text="→")
        comboboxtext.grid(row=1, column=2)
        
        self.combobox_to = ttk.Combobox(self.combobox_frame, height=5, values=to_lang_list, state="readonly")
        self.combobox_to.current(to_lang_list.index('korean'))
        self.combobox_to.grid(row=1, column=3, padx=(self.pad_x, self.pad_x), pady=(self.pad_y, self.pad_y))
        
        # FontSelect frame
        self.font_frame = tk.LabelFrame(self.root, text="select Font")
        self.font_frame.grid(row=6)

        font_label = tk.Label(self.font_frame, text="Font Size")
        font_label.grid(row=1)
        
        self.font_size_list = ["10", "12", "14", "16", "18", "20"]
        self.font_window_size = {"10":(80, 8), "12":(70, 6), "14":(56, 5), "16":(51, 5), "18":(43, 4), "20":(35, 4)}
        self.combobox_font_size = ttk.Combobox(self.font_frame, height=5, values=self.font_size_list, state="readonly")
        self.combobox_font_size.current(0)
        self.combobox_font_size.grid(row=2, padx=(self.pad_x, self.pad_x), pady=(0, self.pad_y))
        self.combobox_font_size.bind("<<ComboboxSelected>>", self.font_change)
    
    def font_change(self, event):
        font_size = event.widget.get()
        window_size = self.font_window_size[font_size]
        
        self.origintext.config(width = window_size[0], height = window_size[1] ,font=('TkDefaultFont', int(font_size)))
        self.transtext.config(width = window_size[0], height = window_size[1] ,font=('TkDefaultFont', int(font_size)))
    
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
            self.root.geometry("600x550")
        else:
            self.origin_info.grid(row=0, padx=(self.pad_x, self.pad_x), pady=(self.pad_y, 0))
            self.origintext.grid(row=1, padx=(self.pad_x, self.pad_x))
            self.disableValue = True
            self.root.geometry("600x700")
    
    def return_combobox(self):
        lang_from, lang_to = None, None
        selected_from, selected_to = self.combobox_from.get(), self.combobox_to.get()
        for key, value in googletrans.LANGUAGES.items():
            if lang_from is not None and lang_to is not None:
                break
            if selected_from == value:
                lang_from = key
            if selected_to == value:
                lang_to = key
        return lang_from, lang_to
    
    def start(self):
        self.root.mainloop()
    
    def __del__(self):
        try:
            self.isStopped = True
            self.root.destroy()
        except:
            pass

if __name__ == "__main__":
    window = resultwindows()
    print(window.return_combobox())
    window.input_origin("abcd")
    window.input_trans("ㅁㄴㅇㄹ")
    window.start()