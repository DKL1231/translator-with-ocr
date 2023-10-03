import tkinter as tk
import clipboard

class studywindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Study window")
        self.root.geometry("200x150")
        
        addwordbutton = tk.Button(self.root, text="Add word", command=self.openaddwordwindow)
        addwordbutton.pack()
        
    
    def openaddwordwindow(self):
        self.addwordwindow = tk.Tk()
        
        origin_info = tk.Label(self.addwordwindow, text="Original Text")
        origin_info.pack()
        self.origintext = tk.Text(self.addwordwindow, width=51, height=5)
        self.origintext.config(font=('TkDefaultFont', 16))
        self.origintext.pack()
        
        cliptext = clipboard.paste()
        if "Unhandled Exception: EXCEPTION_ACCESS_VIOLATION" in cliptext:
            cliptext = ""
        
        self.origintext.delete("1.0", tk.END)
        self.origintext.insert(tk.END, cliptext)
        
        self.trans_info = tk.Label(self.addwordwindow, text="Translated Text")
        self.trans_info.pack()
        
        self.transtext = tk.Text(self.addwordwindow, width=51, height=5)
        self.transtext.config(font=('TkDefaultFont', 16))
        self.transtext.pack()
        
        admitbutton = tk.Button(self.addwordwindow, text="admit", command=self.saveword)
        admitbutton.pack()
    
    def saveword(self):
        filename_origin = "study/origindata.txt"
        filename_trans = "study/transdata.txt"
        encoding = 'UTF-8'
        originfile = open(filename_origin, "a", encoding=encoding)
        transfile = open(filename_trans, "a", encoding=encoding)
        
        originfile.write(self.origintext.get("1.0", tk.END)+"\n\n")
        transfile.write(self.transtext.get("1.0", tk.END)+"\n\n")
        
        originfile.close()
        transfile.close()
    
    def start(self):
        self.root.mainloop()

if __name__ == "__main__":
    sw = studywindow()
    sw.start()